import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getCourse, chapterLabel } from '../data/courses.js';
import { NOTES_INDEX } from '../data/notes/index.js';
import { chapterProgress } from '../lib/progress.js';
import Icon from '../components/Icon.jsx';
import NotFound from './NotFound.jsx';

const TABS = [
  { key: 'content', label: 'Content', icon: 'menu_book' },
  { key: 'tests', label: 'Tests', icon: 'quiz' },
];

export default function Course() {
  const { courseId } = useParams();
  const course = getCourse(courseId);
  const [tab, setTab] = useState('content');
  const [openSubject, setOpenSubject] = useState(course?.subjects[0]?.id);
  const [query, setQuery] = useState('');

  const searchResults = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return null;
    const out = [];
    for (const s of course.subjects) {
      for (const c of s.chapters) {
        const idx = NOTES_INDEX[c.id];
        if (!idx) continue;
        if (idx.title.toLowerCase().includes(q)) {
          out.push({ chapter: c, subject: s, section: null, text: idx.title });
        }
        for (const sec of idx.sections) {
          if (sec.title.toLowerCase().includes(q)) {
            out.push({ chapter: c, subject: s, section: sec, text: sec.title });
          }
        }
      }
    }
    return out.slice(0, 30);
  }, [query, course]);

  if (!course) return <NotFound />;

  const liveChapters = course.subjects.flatMap((s) => s.chapters.filter((c) => c.status === 'live'));
  const totalSections = liveChapters.reduce((a, c) => a + (NOTES_INDEX[c.id]?.sections.length || 0), 0);

  return (
    <div className="gp-page">
      <nav className="gp-crumbs" aria-label="Breadcrumb">
        <Link to="/">Home</Link> <span>/</span> <Link to={`/course/${course.id}`}>Courses</Link> <span>/</span>
        <strong>{course.breadcrumb}</strong>
      </nav>

      <header className="gp-course-head">
        <div>
          <h1>{course.name}</h1>
          <p className="page-sub">{course.description}</p>
          <div className="gp-course-meta">
            <span className="pill pill-ok"><Icon name="check_circle" className="ic-xs" /> {liveChapters.length} chapters live</span>
            <span className="pill pill-mut"><Icon name="list" className="ic-xs" /> {totalSections} sections</span>
            <span className="pill pill-mut"><Icon name="lock_open" className="ic-xs" /> free access</span>
          </div>
        </div>
      </header>

      <div className="gp-tabs">
        {TABS.map((t) => (
          <button
            key={t.key}
            type="button"
            className={`gp-tab${tab === t.key ? ' active' : ''}`}
            onClick={() => (t.key === 'tests' ? setTab('tests') : setTab('content'))}
          >
            <Icon name={t.icon} className="ic-sm" /> {t.label}
          </button>
        ))}
      </div>

      {tab === 'tests' ? (
        <div className="card gp-tests-teaser">
          <Icon name="quiz" className="ic-sm" />
          <div>
            <h3>Practice tests are coming soon</h3>
            <p>Chapter-wise GATE question banks with full solutions are being prepared. The reading notes below are complete and free.</p>
          </div>
          <button type="button" className="btn btn-surf" onClick={() => setTab('content')}>Back to Content</button>
        </div>
      ) : (
        <>
          <div className="input-shell gp-search">
            <Icon name="search" className="input-icon" />
            <input
              className="input with-icon"
              placeholder="Search chapters & sections… (e.g. K-map, De Morgan, hazards)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          {searchResults ? (
            <div className="gp-search-results">
              {searchResults.length === 0 && <div className="page-loading">No sections match “{query}”.</div>}
              {searchResults.map((r, i) => (
                <Link
                  key={i}
                  className="card gp-search-hit"
                  to={`/course/${course.id}/${r.subject.id}/${r.chapter.id}${r.section ? `#${r.section.id}` : ''}`}
                >
                  <span className="pill pill-mut">{r.subject.name} · {chapterLabel(r.chapter)}</span>
                  <span className="gp-search-hit-text">{r.text}</span>
                  <Icon name="arrow_outward" className="ic-sm" />
                </Link>
              ))}
            </div>
          ) : (
            <div className="gp-subjects">
              {course.subjects.map((s) => {
                const open = openSubject === s.id || query;
                return (
                  <div key={s.id} className="gp-subject-block">
                    <button type="button" className="gp-subject-row" onClick={() => setOpenSubject(openSubject === s.id ? null : s.id)}>
                      <Icon name={s.icon} className="ic-sm" />
                      <h2>{s.name}</h2>
                      <span className="code-sm muted">{s.chapters.filter((c) => c.status === 'live').length} live</span>
                      <Icon name={open ? 'expand_less' : 'expand_more'} className="ic-sm" />
                    </button>
                    {open && (
                      <div className="gp-chapters">
                        {s.chapters.length === 0 && (
                          <div className="card gp-chapter-row soon">
                            <div className="gp-chapter-main">
                              <span className="gp-ch-num">—</span>
                              <div>
                                <h3>{s.name} notes</h3>
                                <p className="muted">In preparation — check back soon.</p>
                              </div>
                            </div>
                            <span className="pill pill-mut">coming soon</span>
                          </div>
                        )}
                        {s.chapters.map((c) => {
                          const idx = NOTES_INDEX[c.id];
                          const prog = idx ? chapterProgress(c.id, idx.sections.length) : null;
                          return (
                            <div key={c.id} className={`card gp-chapter-row${c.status !== 'live' ? ' soon' : ''}`}>
                              <div className="gp-chapter-main">
                                <span className="gp-ch-num">{chapterLabel(c).replace('Ch ', '')}</span>
                                <div style={{ flex: 1 }}>
                                  <h3>{c.title}</h3>
                                  {c.status === 'live' && idx ? (
                                    <>
                                      <p className="muted">
                                        {idx.sections.length} sections ·{' '}
                                        {prog.read > 0 ? `${prog.read} read · ${prog.pct}%` : 'not started'}
                                      </p>
                                      {prog.read > 0 && (
                                        <div className="progress gp-ch-progress"><div className="pbar" style={{ width: `${prog.pct}%` }} /></div>
                                      )}
                                    </>
                                  ) : (
                                    <p className="muted">Notes in preparation.</p>
                                  )}
                                </div>
                              </div>
                              {c.status === 'live' ? (
                                <Link className="btn btn-primary" to={`/course/${course.id}/${s.id}/${c.id}`}>
                                  <Icon name="play_arrow" className="ic-sm" /> Read
                                </Link>
                              ) : (
                                <span className="pill pill-mut">coming soon</span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
