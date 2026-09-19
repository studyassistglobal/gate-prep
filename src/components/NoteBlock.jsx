import { useState } from 'react';
import MathText from './MathText.jsx';
import Icon from './Icon.jsx';

const ALERT_META = {
  IMPORTANT: { icon: 'priority_high', cls: 'gp-alert-important', label: 'Important' },
  CAUTION: { icon: 'report', cls: 'gp-alert-caution', label: 'Caution' },
  WARNING: { icon: 'warning', cls: 'gp-alert-warning', label: 'Warning' },
  TIP: { icon: 'lightbulb', cls: 'gp-alert-tip', label: 'Tip' },
  NOTE: { icon: 'info', cls: 'gp-alert-note', label: 'Note' },
};

function Alert({ block }) {
  const meta = ALERT_META[block.type] || ALERT_META.NOTE;
  return (
    <div className={`gp-alert ${meta.cls}`}>
      <div className="gp-alert-title">
        <Icon name={meta.icon} className="ic-sm" /> {meta.label}
      </div>
      <div className="gp-alert-body">
        <MathText text={block.text} />
      </div>
    </div>
  );
}

function Details({ block }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`gp-details${open ? ' open' : ''}`}>
      <button type="button" className="gp-details-summary" onClick={() => setOpen((o) => !o)}>
        <Icon name={open ? 'expand_less' : 'expand_more'} className="ic-sm" />
        {block.summary || 'Solution'}
      </button>
      {open && (
        <div className="gp-details-body">
          {block.blocks.map((b, i) => (
            <NoteBlock key={i} block={b} />
          ))}
        </div>
      )}
    </div>
  );
}

function Table({ block }) {
  return (
    <div className="q-table-wrap gp-table-wrap">
      <table className="q-table gp-table">
        <thead>
          <tr>{block.header.map((h, i) => <th key={i}><MathText text={h} /></th>)}</tr>
        </thead>
        <tbody>
          {block.rows.map((row, r) => (
            <tr key={r}>{row.map((c, i) => <td key={i}><MathText text={c} /></td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** Renders one typed note block (see scripts/build_notes.py for the type contract). */
export default function NoteBlock({ block }) {
  switch (block.t) {
    case 'p':
      return <p className="gp-p"><MathText text={block.text} /></p>;
    case 'h3':
      return <h3 className="gp-h3"><MathText text={block.text} /></h3>;
    case 'h4':
      return <h4 className="gp-h4"><MathText text={block.text} /></h4>;
    case 'ul':
      return (
        <ul className="gp-ul">
          {block.items.map((it, i) => <li key={i}><MathText text={it} /></li>)}
        </ul>
      );
    case 'ol':
      return (
        <ol className="gp-ol">
          {block.items.map((it, i) => <li key={i}><MathText text={it} /></li>)}
        </ol>
      );
    case 'math':
      return <div className="gp-math"><MathText text={`$$${block.tex}$$`} /></div>;
    case 'code':
      return <pre className="gp-code"><code>{block.text}</code></pre>;
    case 'table':
      return <Table block={block} />;
    case 'alert':
      return <Alert block={block} />;
    case 'details':
      return <Details block={block} />;
    case 'img':
      return (
        <figure className="gp-figure">
          <img src={block.src} alt={block.alt || 'Figure'} loading="lazy" />
          {block.alt && <figcaption>{block.alt}</figcaption>}
        </figure>
      );
    default:
      return null;
  }
}
