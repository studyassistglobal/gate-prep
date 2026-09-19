import { Link } from 'react-router-dom';
import { COURSE, chapterLabel } from '../data/courses.js';
import { NOTES_INDEX } from '../data/notes/index.js';
import { chapterProgress } from '../lib/progress.js';
import Icon from '../components/Icon.jsx';

export default function Home() {
  const liveChapters = COURSE.subjects.flatMap((s) => s.chapters.filter((c) => c.status === 'live'));
  const totalSections = liveChapters.reduce((a, c) => a + (NOTES_INDEX[c.id]?.sections.length || 0), 0);

  return (
    <div className="gp-page">
      <section className="gp-hero">
        <span className="pill pill-pri">Free · No sign-up</span>
        <h1>Master GATE 2027 with notes that <em>actually teach</em>.</h1>
        <p className="page-sub">
          Faculty-style chapter notes for GATE 2027 (ECE) — deep theory, worked solutions,
          faculty traps and exam strategy. Written for revision, not just reading.
        </p>
        <div className="gp-hero-actions">
          <Link className="btn btn-primary btn-lg" to={`/course/${COURSE.id}`}>
            <Icon name="menu_book" className="ic-sm" /> Open the GATE Course
          </Link>
          <Link className="btn btn-ghost btn-lg" to="/tests">
            <Icon name="quiz" className="ic-sm" /> Practice Tests
          </Link>
        </div>
        <div className="gp-hero-stats">
          <div><strong>{liveChapters.length}</strong><span>chapters live</span></div>
          <div><strong>{totalSections}</strong><span>sections of notes</span></div>
          <div><strong>100+</strong><span>worked examples</span></div>
        </div>
      </section>

      <section className="gp-home-subjects">
        <h2 className="gp-home-title">Subjects</h2>
        <div className="gp-subject-grid">
          {COURSE.subjects.map((s) => {
            const live = s.chapters.filter((c) => c.status === 'live');
            return (
              <Link key={s.id} to={`/course/${COURSE.id}`} className={`card gp-subject-card accent-${s.accent || 'phy'}`}>
                <div className="gp-subject-head">
                  <Icon name={s.icon} className="ic-sm" />
                  <h3>{s.name}</h3>
                  {s.status === 'soon' && <span className="pill pill-mut">coming soon</span>}
                </div>
                <p>
                  {live.length > 0
                    ? `${live.length} chapters live · ${live.map((c) => chapterLabel(c)).join(', ')}`
                    : 'Notes in preparation'}
                </p>
                {live.length > 0 && (
                  <div className="gp-home-progress">
                    {live.map((c) => {
                      const p = chapterProgress(c.id, NOTES_INDEX[c.id]?.sections.length || 0);
                      return (
                        <div key={c.id} className="gp-mini-progress" title={`Your progress in ${chapterLabel(c)}: ${p.pct}%`}>
                          <span>{chapterLabel(c)}</span>
                          <div className="progress"><div className="pbar" style={{ width: `${p.pct}%` }} /></div>
                          <span className="code-sm">{p.pct}%</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </section>

      <section className="gp-home-features">
        <h2 className="gp-home-title">Why these notes work</h2>
        <div className="gp-feature-grid">
          <div className="card gp-feature"><Icon name="auto_stories" className="ic-sm" /><h3>Deep, not shallow</h3><p>Every module builds from fundamentals to GATE-level twists — the way a good faculty teaches, not a cheatsheet.</p></div>
          <div className="card gp-feature"><Icon name="task_alt" className="ic-sm" /><h3>Solved everywhere</h3><p>Collapsible worked solutions with faculty insights under every practice problem — attempt first, then peek.</p></div>
          <div className="card gp-feature"><Icon name="my_location" className="ic-sm" /><h3>Track your progress</h3><p>Mark sections as read as you go. Your progress stays on this device, no account needed.</p></div>
          <div className="card gp-feature"><Icon name="dark_mode" className="ic-sm" /><h3>Light & dark</h3><p>Study late without burning your eyes — full dark mode across every page.</p></div>
        </div>
      </section>
    </div>
  );
}
