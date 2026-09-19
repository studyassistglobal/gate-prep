import { Link } from 'react-router-dom';
import Icon from '../components/Icon.jsx';

export default function NotFound() {
  return (
    <div className="nf-screen">
      <div className="nf-blobs">
        <div className="nf-blob a" />
      </div>
      <div className="nf-404">404</div>
      <div className="nf-title">This page graduated!</div>
      <div className="nf-sub">The page you&apos;re looking for has moved or doesn&apos;t exist. The full GATE course is one click away.</div>
      <Link className="btn btn-primary btn-pill" to="/"><Icon name="arrow_back" className="ic-sm" /> Back to Home</Link>
      <div className="nf-foot">GATE Prep • Free GATE 2027 Notes</div>
    </div>
  );
}
