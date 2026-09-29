// Comprehensive formatting/content audit for all generated note modules.
// Checks LaTeX health, mojibake leakage, stray markers, empty content, and
// structural consistency across every chapter + the registry/index.
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const { COURSE, liveChapterSequence } = await import(pathToFileURL(path.join(ROOT, 'src/data/courses.js')).href);
const { NOTES_INDEX } = await import(pathToFileURL(path.join(ROOT, 'src/data/notes/index.js')).href);

const issues = [];
const warn = (sev, m) => issues.push({ sev, m });

const MOJIBAKE = /[\u0900-\u097F\u0100-\u024F\u0370-\u0383]/;
const CTRL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F]/;
const DOLLARS = (s) => (s.match(/\$/g) || []).length;
const DD = (s) => (s.match(/\$\$/g) || []).length;

function leafIssues(ctx, blockType, s) {
  if (CTRL.test(s)) warn('high', `${ctx}: control char in ${blockType}: ${JSON.stringify(s.slice(0, 70))}`);
  if (MOJIBAKE.test(s)) warn('high', `${ctx}: mojibake/Devanagari leakage in ${blockType}: ${JSON.stringify(s.slice(0, 70))}`);
  if (DD(s) % 2 === 1 && DOLLARS(s) % 2 === 1) warn('med', `${ctx}: odd $$ count in ${blockType}: ${JSON.stringify(s.slice(0, 70))}`);
  else if (DOLLARS(s) % 2 === 1) warn('med', `${ctx}: odd $ count in ${blockType}: ${JSON.stringify(s.slice(0, 70))}`);
  // unbalanced \( \)
  if ((s.match(/\\\(/g) || []).length !== (s.match(/\\\)/g) || []).length)
    warn('med', `${ctx}: unbalanced \\( \\) in ${blockType}: ${JSON.stringify(s.slice(0, 70))}`);
  // stray markdown that will render literally
  if (/^#{1,6}\s/.test(s) && blockType === 'p') warn('low', `${ctx}: paragraph starts with # heading marker`);
  if (s.includes('**') && (s.match(/\*\*/g) || []).length % 2 === 1)
    warn('low', `${ctx}: odd ** count (bold may leak) in ${blockType}: ${JSON.stringify(s.slice(0, 60))}`);
  if (s.includes('`' + '`' + '`')) warn('low', `${ctx}: stray fence markers inside ${blockType}`);
  if (/!\[[^\]]*\]\(http/.test(s) && blockType !== 'img') warn('med', `${ctx}: remote image URL in ${blockType}`);
  if (/\bTBD\b|\bTODO\b|lorem ipsum/i.test(s)) warn('low', `${ctx}: placeholder text`);
}

let blocks = 0, leaves = 0;
for (const { subject, chapter } of liveChapterSequence(COURSE.id)) {
  const sub = subject.id;
  const mod = (await import(pathToFileURL(path.join(ROOT, 'src/data/notes', sub, `${chapter.file}.js`)).href)).default;
  const meta = NOTES_INDEX[chapter.id];
  if (!meta) warn('high', `${chapter.id}: missing from NOTES_INDEX`);
  else {
    if (meta.sections.length !== mod.sections.length) warn('high', `${chapter.id}: index/module section count mismatch`);
    if (meta.title !== mod.title) warn('med', `${chapter.id}: title mismatch vs index`);
  }
  // duplicate slugs
  const sids = mod.sections.map((s) => s.id);
  if (new Set(sids).size !== sids.length) warn('high', `${chapter.id}: duplicate section slugs`);
  // section count sanity vs source size
  for (const sec of mod.sections) {
    if (!sec.blocks.length) warn('high', `${chapter.id}#${sec.id}: EMPTY section`);
    if (!sec.title.trim()) warn('high', `${chapter.id}#${sec.id}: empty section title`);
  }
  const walk = (b, ctx) => {
    blocks++;
    if (b.t === 'img') {
      const p = path.join(ROOT, 'public', b.src.replace(/^\//, ''));
      if (!fs.existsSync(p)) warn('high', `${ctx}: missing figure file ${b.src}`);
      else {
        const stat = fs.statSync(p);
        if (stat.size > 3_000_000) warn('low', `${ctx}: large figure ${b.src} (${Math.round(stat.size / 1024)} KB)`);
      }
      if (!b.alt) warn('low', `${ctx}: figure without alt text ${b.src}`);
    }
    if (b.t === 'table') {
      const cols = b.header.length;
      for (const r of b.rows) if (r.length !== cols) warn('med', `${ctx}: ragged table row (${r.length} vs ${cols} cols): ${JSON.stringify(r[0] || '').slice(0, 40)}`);
    }
    if (b.t === 'details' && !b.summary?.trim()) warn('low', `${ctx}: details without summary`);
    const leaves_ = [b.text, b.tex, b.title, b.summary, ...(b.items || []), ...(b.header || []), ...(b.rows || []).flat()].filter((x) => typeof x === 'string' && x);
    for (const s of leaves_) { leaves++; leafIssues(ctx, b.t, s); }
    if (b.blocks) for (const x of b.blocks) walk(x, ctx + '>details');
  };
  for (const sec of mod.sections) for (const b of sec.blocks) walk(b, `${chapter.id}#${sec.id}`);
}

// registry / courses sanity
const ids = liveChapterSequence(COURSE.id).map((x) => x.chapter.id);
if (new Set(ids).size !== ids.length) warn('high', 'duplicate live chapter ids in registry');
for (const s of COURSE.subjects) {
  for (const c of s.chapters) {
    if (c.status === 'live' && !NOTES_INDEX[c.id]) warn('high', `${c.id}: registered live but missing from NOTES_INDEX`);
  }
}

const high = issues.filter((i) => i.sev === 'high');
const med = issues.filter((i) => i.sev === 'med');
const low = issues.filter((i) => i.sev === 'low');
console.log(`audited ${blocks} blocks / ${leaves} text leaves across ${ids.length} chapters`);
console.log(`HIGH ${high.length} · MED ${med.length} · LOW ${low.length}`);
high.forEach((i) => console.log('  HIGH:', i.m));
med.slice(0, 40).forEach((i) => console.log('  med:', i.m));
low.slice(0, 20).forEach((i) => console.log('  low:', i.m));
fs.writeFileSync(path.join(ROOT, 'scratch', 'audit_content.json'), JSON.stringify(issues, null, 1));
process.exit(high.length ? 1 : 0);
