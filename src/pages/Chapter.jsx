import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams, useLocation } from 'react-router-dom';
import { findChapter, liveChapterSequence } from '../data/courses.js';
import { getReadSections, toggleSectionRead } from '../lib/progress.js';
import Icon from '../components/Icon.jsx';
import NoteBlock from '../components/NoteBlock.jsx';
import NotFound from './NotFound.jsx';

export default function Chapter() {
  const { courseId, subjectId, chapterId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const found = findChapter(courseId, chapterId);
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [readSet, setReadSet] = useState(() => new Set());

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setModule(null);
    if (!found) { setLoading(false); return; }
    import(`../data/notes/de/${found.chapter.file}.js`)
      .then((m) => { if (alive) setModule(m.default); })
      .catch(() => { if (alive) setModule(null); })
      .finally(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
  }, [chapterId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (module) setReadSet(getReadSections(module.id));
  }, [module]);

  // Paginated reader: the URL hash picks the visible module. No hash = first
  // module. Modules are NEVER stacked, so scrolling can't skip ahead — the only
  // way forward is the nav buttons (or the TOC).
  const basePath = `/course/${courseId}/${subjectId}/${chapterId}`;
  const activeIdx = useMemo(() => {
    if (!module) return 0;
    const anchor = location.hash ? location.hash.slice(1) : null;
    if (!anchor) return 0;
    const idx = module.sections.findIndex((s) => s.id === anchor);
    return idx >= 0 ? idx : 0;
  }, [module, location.hash]);

  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [activeIdx, chapterId]);

  const goToSection = (sectionId) => {
    navigate(`${basePath}#${sectionId}`);
  };

  const readPct = useMemo(() => {
    if (!module) return 0;
    return module.sections.length ? Math.round((readSet.size / module.sections.length) * 100) : 0;
  }, [readSet, module]);

  if (!found) return <NotFound />;
  const { subject, chapter } = found;
  const seq = liveChapterSequence(courseId);
  const seqIdx = seq.findIndex((x) => x.chapter.id === chapterId);
  const prev = seqIdx > 0 ? seq[seqIdx - 1] : null;
  const next = seqIdx >= 0 && seqIdx < seq.length - 1 ? seq[seqIdx + 1] : null;

  const handleToggle = (sectionId) => {
    toggleSectionRead(module.id, sectionId);
    setReadSet(getReadSections(module.id));
  };

  const truncate = (t) => (t.length > 34 ? `${t.slice(0, 34)}…` : t);

  const goPrevChapter = () => {
    if (prev) navigate(`/course/${courseId}/${prev.subject.id}/${prev.chapter.id}`);
  };
  const goNextChapter = () => {
    if (next) navigate(`/course/${courseId}/${next.subject.id}/${next.chapter.id}`);
  };

  const loadingView = loading || !module;
  const section = !loadingView ? module.sections[activeIdx] : null;
  const prevSec = section && activeIdx > 0 ? module.sections[activeIdx - 1] : null;
  const nextSec = section && activeIdx < module.sections.length - 1 ? module.sections[activeIdx + 1] : null;

  return (
    <div className="gp-page gp-chapter-page">
      <nav className="gp-crumbs" aria-label="Breadcrumb">
        <Link to="/">Home</Link> <span>/</span>
        <Link to={`/course/${courseId}`}>Courses</Link> <span>/</span>
        <Link to={`/course/${courseId}`}>{subject.name}</Link> <span>/</span>
        <strong>Chapter {chapter.num}: {chapter.title}</strong>
      </nav>

      {loading && <div className="page-loading">Loading chapter notes…</div>}

      {!loading && !module && <NotFound />}

      {!loading && module && (
        <div className="gp-chapter-layout">
          <aside className="gp-toc">
            <div className="gp-toc-head">
              <span className="pill pill-pri">{readPct}% read</span>
              <div className="progress gp-toc-progress"><div className="pbar" style={{ width: `${readPct}%` }} /></div>
            </div>
            <nav>
              {module.sections.map((s, i) => (
                <button
                  key={s.id}
                  type="button"
                  className={`gp-toc-link${i === activeIdx ? ' active' : ''}${readSet.has(s.id) ? ' read' : ''}`}
                  onClick={() => goToSection(s.id)}
                  title={s.title}
                >
                  <span className="gp-toc-num">{readSet.has(s.id) ? <Icon name="check_circle" className="ic-sm" /> : i + 1}</span>
                  <span className="gp-toc-text">{s.title}</span>
                </button>
              ))}
            </nav>
          </aside>

          <article className="gp-chapter-content">
            <header className="gp-chapter-head">
              <span className="pill pill-mut">{subject.name}</span>
              <h1>Chapter {module.num}: {module.title}</h1>
              <p className="page-sub">
                Module {activeIdx + 1} of {module.sections.length} · {readSet.size} of {module.sections.length} marked read · progress saved on this device
              </p>
            </header>

            {section && (
              <section key={section.id} className={`gp-section${readSet.has(section.id) ? ' is-read' : ''}`}>
                <div className="gp-section-head">
                  <h2>
                    <span className="gp-sec-num">{activeIdx + 1}</span>
                    {section.title}
                  </h2>
                  <button
                    type="button"
                    className={`btn btn-sm ${readSet.has(section.id) ? 'btn-ghost' : 'btn-surf'}`}
                    onClick={() => handleToggle(section.id)}
                    title={readSet.has(section.id) ? 'Mark as unread' : 'Mark this section as read'}
                  >
                    <Icon name={readSet.has(section.id) ? 'check_circle' : 'radio_button_unchecked'} className="ic-sm" />
                    {readSet.has(section.id) ? 'Read' : 'Mark read'}
                  </button>
                </div>
                {section.blocks.map((b, bi) => <NoteBlock key={bi} block={b} />)}

                <div className="gp-section-nav">
                  {prevSec ? (
                    <button type="button" className="btn btn-surf" onClick={() => goToSection(prevSec.id)} title={prevSec.title}>
                      <Icon name="arrow_back" className="ic-sm" /> {truncate(prevSec.title)}
                    </button>
                  ) : prev ? (
                    <button type="button" className="btn btn-surf" onClick={goPrevChapter} title={`Chapter ${prev.chapter.num}: ${prev.chapter.title}`}>
                      <Icon name="arrow_back" className="ic-sm" /> Ch {prev.chapter.num}: {truncate(prev.chapter.title)}
                    </button>
                  ) : <span />}
                  {nextSec ? (
                    <button type="button" className="btn btn-primary" onClick={() => goToSection(nextSec.id)} title={nextSec.title}>
                      {truncate(nextSec.title)} <Icon name="arrow_forward" className="ic-sm" />
                    </button>
                  ) : next ? (
                    <button type="button" className="btn btn-primary" onClick={goNextChapter} title={`Chapter ${next.chapter.num}: ${next.chapter.title}`}>
                      Ch {next.chapter.num}: {truncate(next.chapter.title)} <Icon name="arrow_forward" className="ic-sm" />
                    </button>
                  ) : (
                    <Link className="btn btn-primary" to={`/course/${courseId}`}>
                      Back to course <Icon name="arrow_forward" className="ic-sm" />
                    </Link>
                  )}
                </div>
              </section>
            )}
          </article>
        </div>
      )}
    </div>
  );
}
