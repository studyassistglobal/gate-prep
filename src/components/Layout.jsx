import { useEffect, useState } from 'react';
import { NavLink, Outlet, Link, useLocation } from 'react-router-dom';
import { useTheme } from '../lib/theme.js';
import Icon from './Icon.jsx';

const NAV = [
  { to: '/', label: 'Home', end: true },
  { to: '/course/gate-2027-ece', label: 'GATE Course' },
  { to: '/tests', label: 'Tests' },
];

export default function Layout() {
  const { isDark, toggle } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  // close the mobile nav whenever the route changes
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!menuOpen) return;
    const onKey = (e) => { if (e.key === 'Escape') setMenuOpen(false); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [menuOpen]);

  return (
    <div>
      <header className="app-header">
        <div className="header-inner">
          <NavLink to="/" className="brand">
            <Icon name="school" className="brand-icon" />
            <span className="brand-name">GATE Prep</span>
          </NavLink>

          <nav className="nav-links">
            {NAV.map((n) => (
              <NavLink key={n.to} to={n.to} end={n.end} className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
                {n.label}
              </NavLink>
            ))}
          </nav>

          <div className="header-actions">
            <button className="btn-icon" onClick={toggle} title={isDark ? 'Switch to light mode' : 'Switch to dark mode'} aria-label="Toggle theme">
              <Icon name={isDark ? 'light_mode' : 'dark_mode'} className="ic-sm" />
            </button>
            <button className="btn-icon menu-btn" onClick={() => setMenuOpen((o) => !o)} title="Menu" aria-label="Menu" aria-expanded={menuOpen}>
              <Icon name={menuOpen ? 'close' : 'menu'} className="ic-sm" />
            </button>
          </div>
        </div>

        {menuOpen && (
          <div className="nav-backdrop" onClick={() => setMenuOpen(false)} aria-hidden="true" />
        )}
        {menuOpen && (
          <nav className="mobile-nav" aria-label="Mobile navigation">
            {NAV.map((n) => (
              <NavLink
                key={n.to}
                to={n.to}
                end={n.end}
                className={({ isActive }) => `mobile-nav-link${isActive ? ' active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                {n.label}
                <Icon name="chevron_right" className="ic-sm" />
              </NavLink>
            ))}
          </nav>
        )}
      </header>

      <main className="app-main">
        <Outlet />
      </main>

      <footer className="gp-footer">
        <div className="gp-footer-inner">
          <div className="gp-footer-brand">
            <Icon name="school" className="ic-sm" /> <strong>GATE Prep</strong>
            <span className="gp-footer-tag">Free chapter-wise notes for GATE 2027 aspirants.</span>
          </div>
          <div className="gp-footer-links">
            <Link to="/course/gate-2027-ece">GATE 2027 (ECE)</Link>
            <Link to="/tests">Practice Tests</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
