import { Link } from 'react-router-dom';
import { COURSE } from '../data/courses.js';
import Icon from '../components/Icon.jsx';

export default function Tests() {
  return (
    <div className="gp-page">
      <nav className="gp-crumbs" aria-label="Breadcrumb">
        <Link to="/">Home</Link> <span>/</span> <strong>Tests</strong>
      </nav>
      <div className="card gp-tests-teaser big">
        <Icon name="quiz" className="ic-lg" />
        <div>
          <h1>Practice Tests — coming soon</h1>
          <p>
            Chapter-wise GATE question banks with full solutions and negative-marking simulation
            are being prepared for this course. Meanwhile, the complete reading notes are free:
          </p>
          <Link className="btn btn-primary" to={`/course/${COURSE.id}`}>
            <Icon name="menu_book" className="ic-sm" /> Continue reading the GATE Course
          </Link>
        </div>
      </div>
    </div>
  );
}
