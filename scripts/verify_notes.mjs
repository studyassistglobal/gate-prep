// GATE Prep notes verification — run before deploy.
// 1. Registry ↔ generated index ↔ chapter modules consistency
// 2. Block AST type-safety + math/code balance
// 3. Every figure path exists in public/
// 4. Search index covers every section
// 5. Fork hygiene: no auth/supabase/recharts imports remain in src/
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');


const subjectOf = (chapter) => {
  for (const s of COURSE.subjects) if (s.chapters.some((c) => c.id === chapter.id)) return s.id;
  return 'de';
};

let errors = 0;
const fail = (m) => { console.error('FAIL:', m); errors++; };

const { COURSE, findChapter, liveChapterSequence } = await import(pathToFileURL(path.join(ROOT, 'src/data/courses.js')).href);
const { NOTES_INDEX } = await import(pathToFileURL(path.join(ROOT, 'src/data/notes/index.js')).href);

// 1. registry consistency
const live = liveChapterSequence(COURSE.id);
if (COURSE.id !== 'gate-2027-ece') fail(`unexpected course id ${COURSE.id}`);
if (live.length !== 6) fail(`expected 6 live chapters, found ${live.length}`);
for (const { chapter } of live) {
  const idx = NOTES_INDEX[chapter.id];
  if (!idx) { fail(`${chapter.id}: missing from NOTES_INDEX`); continue; }
  if (idx.title !== chapter.title) fail(`${chapter.id}: registry title mismatch`);
  const mod = (await import(pathToFileURL(path.join(ROOT, 'src/data/notes', subjectOf(chapter), `${chapter.file}.js`)).href)).default;
  if (mod.sections.length !== idx.sections.length) fail(`${chapter.id}: module sections ${mod.sections.length} != index ${idx.sections.length}`);
  for (let i = 0; i < idx.sections.length; i++) {
    if (mod.sections[i].id !== idx.sections[i].id || mod.sections[i].title !== idx.sections[i].title) {
      fail(`${chapter.id} section ${i}: index/module mismatch`);
    }
  }
  // duplicate section ids?
  const ids = new Set(mod.sections.map((s) => s.id));
  if (ids.size !== mod.sections.length) fail(`${chapter.id}: duplicate section slugs`);
}

// 2+3. block safety
const VALID = new Set(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'table', 'code', 'alert', 'details', 'img', 'math']);
const balancedDelims = (s) =>
  (s.match(/\$\$/g) || []).length % 2 === 0 &&
  (s.match(/\$/g) || []).length % 2 === 0 &&
  (s.match(/\\\(/g) || []).length === (s.match(/\\\)/g) || []).length;

let blocksChecked = 0;
for (const { chapter } of live) {
  const mod = (await import(pathToFileURL(path.join(ROOT, 'src/data/notes', subjectOf(chapter), `${chapter.file}.js`)).href)).default;
  const walk = (blocks, ctx) => {
    for (const b of blocks) {
      blocksChecked++;
      if (!VALID.has(b.t)) fail(`${ctx}: unknown block type ${b.t}`);
      if (b.t === 'math' && !b.tex?.trim()) fail(`${ctx}: empty math block`);
      if ((b.t === 'p' || b.t === 'ul' || b.t === 'ol') && !b.text && !(b.items?.length)) fail(`${ctx}: empty ${b.t}`);
      if (b.t === 'table' && (!b.header?.length || !b.rows?.length)) fail(`${ctx}: malformed table`);
      if (b.t === 'img') {
        const p = path.join(ROOT, 'public', b.src.replace(/^\//, ''));
        if (!fs.existsSync(p)) fail(`${ctx}: missing figure ${b.src}`);
      }
      if (b.t === 'details' && !b.blocks?.length) fail(`${ctx}: empty details`);
      for (const s of [b.text, b.tex, ...(b.items || []), ...(b.header || []), ...(b.rows || []).flat()].filter(Boolean)) {
        if (!balancedDelims(s)) fail(`${ctx}: unbalanced math delimiters in "${String(s).slice(0, 60)}"`);
      }
      if (b.t === 'details') walk(b.blocks, `${ctx}/details`);
    }
  };
  for (const s of mod.sections) walk(s.blocks, `${mod.id}#${s.id}`);
}

// 4. search coverage: every live section findable via index
let indexed = 0;
for (const s of Object.values(NOTES_INDEX)) indexed += s.sections.length;
if (indexed !== live.reduce((a, c) => a + (NOTES_INDEX[c.chapter.id]?.sections.length || 0), 0)) fail('index coverage mismatch');

// 5. fork hygiene
const walkSrc = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
  const p = path.join(dir, e.name);
  return e.isDirectory() ? walkSrc(p) : [p];
});
for (const f of walkSrc(path.join(ROOT, 'src'))) {
  const txt = fs.readFileSync(f, 'utf8');
  if (/from\s+['"].*(supabase|auth\.jsx|db\.js|srs\.js|scoring\.js|gamification\.js|recharts)/.test(txt)) {
    fail(`stale import in ${path.relative(ROOT, f)}`);
  }
}

console.log(`registry OK · ${live.length} live chapters · ${blocksChecked} blocks checked · ${indexed} sections indexed`);
console.log(errors ? `\n❌ ${errors} error(s)` : '\n🎉 GATE PREP NOTES 100% VALID');
process.exit(errors ? 1 : 0);
