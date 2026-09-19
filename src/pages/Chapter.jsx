import { useEffect, useMemo, useState } from 'react';
import { Link, useParams, useLocation } from 'react-router-dom';
import { findChapter, liveChapterSequence } from '../data/courses.js';
import { getReadSections, toggleSectionRead } from '../lib/progress.js';
import Icon from '../components/Icon.jsx';
import NoteBlock from '../components/NoteBlock.jsx';
import NotFound from './NotFound.jsx';

export default function Chapter() {
  const { courseId, subjectId, chapterId } = useParams();
  const location = useLocation();
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

  // deep-link: /course/.../de-ch1#section-id — react-router parses the trailing
  // hash into location.hash even under HashRouter.
  useEffect(() => {
    if (module && location.hash) {
      const anchor = location.hash.slice(1);
      setTimeout(() => {
        document.getElementById(anchor)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 60);
    }
  }, [module, location.hash]);

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

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const truncate = (t) => (t.length > 34 ? `${t.slice(0, 34)}…` : t);

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
                <a
                  key={s.id}
                  href={`#/course/${courseId}/${subjectId}/${chapterId}#${s.id}`}
                  className={`gp-toc-link${readSet.has(s.id) ? ' read' : ''}`}
                  onClick={(e) => {
                    e.preventDefault();
                    document.getElementById(s.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }}
                  title={s.title}
                >
                  <span className="gp-toc-num">{readSet.has(s.id) ? <Icon name="check_circle" className="ic-sm" /> : i + 1}</span>
                  <span className="gp-toc-text">{s.title}</span>
                </a>
              ))}
            </nav>
          </aside>

          <article className="gp-chapter-content">
            <header className="gp-chapter-head">
              <span className="pill pill-mut">{subject.name}</span>
              <h1>Chapter {module.num}: {module.title}</h1>
              <p className="page-sub">
                {module.sections.length} sections · {readSet.size} marked read · progress saved on this device
              </p>
            </header>

            {module.sections.map((s, i) => {
              const prevSec = i > 0 ? module.sections[i - 1] : null;
              const nextSec = i < module.sections.length - 1 ? module.sections[i + 1] : null;
              return (
                <section key={s.id} id={s.id} className={`gp-section${readSet.has(s.id) ? ' is-read' : ''}`}>
                  <div className="gp-section-head">
                    <h2>
                      <span className="gp-sec-num">{i + 1}</span>
                      {s.title}
                    </h2>
                    <button
                      type="button"
                      className={`btn btn-sm ${readSet.has(s.id) ? 'btn-ghost' : 'btn-surf'}`}
                      onClick={() => handleToggle(s.id)}
                      title={readSet.has(s.id) ? 'Mark as unread' : 'Mark this section as read'}
                    >
                      <Icon name={readSet.has(s.id) ? 'check_circle' : 'radio_button_unchecked'} className="ic-sm" />
                      {readSet.has(s.id) ? 'Read' : 'Mark read'}
                    </button>
                  </div>
                  {s.blocks.map((b, bi) => <NoteBlock key={bi} block={b} />)}
                  <div className="gp-section-nav">
                    {prevSec ? (
                      <button type="button" className="btn btn-surf" onClick={() => scrollToSection(prevSec.id)} title={prevSec.title}>
                        <Icon name="arrow_back" className="ic-sm" /> {truncate(prevSec.title)}
                      </button>
                    ) : prev ? (
                      <Link className="btn btn-surf" to={`/course/${courseId}/${prev.subject.id}/${prev.chapter.id}`} title={`Chapter ${prev.chapter.num}: ${prev.chapter.title}`}>
                        <Icon name="arrow_back" className="ic-sm" /> Ch {prev.chapter.num}: {truncate(prev.chapter.title)}
                      </Link>
                    ) : <span />}
                    {nextSec ? (
                      <button type="button" className="btn btn-primary" onClick={() => scrollToSection(nextSec.id)} title={nextSec.title}>
                        {truncate(nextSec.title)} <Icon name="arrow_forward" className="ic-sm" />
                      </button>
                    ) : next ? (
                      <Link className="btn btn-primary" to={`/course/${courseId}/${next.subject.id}/${next.chapter.id}`} title={`Chapter ${next.chapter.num}: ${next.chapter.title}`}>
                        Ch {next.chapter.num}: {truncate(next.chapter.title)} <Icon name="arrow_forward" className="ic-sm" />
                      </Link>
                    ) : (
                      <Link className="btn btn-primary" to={`/course/${courseId}`}>
                        Back to course <Icon name="arrow_forward" className="ic-sm" />
                      </Link>
                    )}
                  </div>
                </section>
              );
            })}
          </article>
        </div>
      )}
    </div>
  );
}
