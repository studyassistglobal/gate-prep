import { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

/**
 * Render one line's inline content. Bold/code spans are tokenized OUTERMOST so
 * markdown emphasis can wrap math (`**Rise Time ($t_r$)**`), which the notes
 * use constantly; math/img tokens inside get rendered recursively.
 */
function renderLine(line, container) {
  const tokenRegex = /(\*\*[\s\S]+?\*\*|`[^`]+`|\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\$[^$]+?\$|\\\([\s\S]+?\\\)|\!\[.*?\]\(.*?\))/g;
  const parts = line.split(tokenRegex);

  for (const part of parts) {
    if (!part) continue;

    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      const strong = document.createElement('strong');
      renderInlineContent(part.slice(2, -2), strong);
      container.appendChild(strong);
      continue;
    }
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      const code = document.createElement('code');
      code.textContent = part.slice(1, -1);
      container.appendChild(code);
      continue;
    }

    // Display math $$...$$ or \[...\]
    if ((part.startsWith('$$') && part.endsWith('$$')) || (part.startsWith('\\[') && part.endsWith('\\]'))) {
      const math = part.startsWith('$$') ? part.slice(2, -2) : part.slice(2, -2);
      try {
        const span = document.createElement('span');
        span.className = 'math-display-wrap';
        katex.render(math.trim(), span, { displayMode: true, throwOnError: false });
        container.appendChild(span);
      } catch {
        container.appendChild(document.createTextNode(part));
      }
      continue;
    }
    // Inline math $...$ or \(...\)
    if ((part.startsWith('$') && part.endsWith('$')) || (part.startsWith('\\(') && part.endsWith('\\)'))) {
      const math = part.startsWith('$') ? part.slice(1, -1) : part.slice(2, -2);
      try {
        const span = document.createElement('span');
        span.className = 'math-inline-wrap';
        katex.render(math.trim(), span, { displayMode: false, throwOnError: false });
        container.appendChild(span);
      } catch {
        container.appendChild(document.createTextNode(part));
      }
      continue;
    }
    // Markdown image ![alt](url)
    if (part.startsWith('![') && part.includes('](') && part.endsWith(')')) {
      const imgMatch = part.match(/\!\[(.*?)\]\((.*?)\)/);
      if (imgMatch) {
        const altText = imgMatch[1] || 'Figure';
        let imgSrc = imgMatch[2] || '';
        // Ensure root-relative path for SPAs so nested routes don't 404
        if (!imgSrc.startsWith('http') && !imgSrc.startsWith('data:') && !imgSrc.startsWith('/')) {
          imgSrc = `/${imgSrc}`;
        }
        const img = document.createElement('img');
        img.src = imgSrc;
        img.alt = altText;
        img.className = 'q-inline-img';
        img.loading = 'lazy';
        container.appendChild(img);
      } else {
        container.appendChild(document.createTextNode(part));
      }
      continue;
    }

    container.appendChild(document.createTextNode(part));
  }
}

/**
 * Helper to render inline rich text (KaTeX math, images, bold, code, line breaks) into a DOM node.
 * Display-math blocks and images are split out first (they may span lines);
 * remaining segments are rendered line-by-line with bold-aware tokenizing.
 */
function renderInlineContent(text, container) {
  if (!text) return;

  const blockRegex = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\!\[.*?\]\(.*?\))/g;
  const segments = text.split(blockRegex);

  for (const seg of segments) {
    if (!seg) continue;

    if ((seg.startsWith('$$') && seg.endsWith('$$')) || (seg.startsWith('\\[') && seg.endsWith('\\]'))) {
      const math = seg.startsWith('$$') ? seg.slice(2, -2) : seg.slice(2, -2);
      try {
        const span = document.createElement('span');
        span.className = 'math-display-wrap';
        katex.render(math.trim(), span, { displayMode: true, throwOnError: false });
        container.appendChild(span);
      } catch {
        container.appendChild(document.createTextNode(seg));
      }
      continue;
    }
    if (seg.startsWith('![') && seg.includes('](') && seg.endsWith(')')) {
      const imgMatch = seg.match(/\!\[(.*?)\]\((.*?)\)/);
      if (imgMatch) {
        const altText = imgMatch[1] || 'Figure';
        let imgSrc = imgMatch[2] || '';
        if (!imgSrc.startsWith('http') && !imgSrc.startsWith('data:') && !imgSrc.startsWith('/')) {
          imgSrc = `/${imgSrc}`;
        }
        const img = document.createElement('img');
        img.src = imgSrc;
        img.alt = altText;
        img.className = 'q-inline-img';
        img.loading = 'lazy';
        container.appendChild(img);
      } else {
        container.appendChild(document.createTextNode(seg));
      }
      continue;
    }

    // plain segment: line breaks + bold/code/math inline tokens
    const lines = seg.split('\n');
    lines.forEach((line, lineIdx) => {
      if (lineIdx > 0) container.appendChild(document.createElement('br'));
      if (line) renderLine(line, container);
    });
  }
}

/**
 * Parses markdown tables from text and renders full structured HTML tables.
 */
export default function MathText({ text }) {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current || !text) return;
    const node = ref.current;
    node.innerHTML = '';

    // Regex for markdown tables (header + separator + 1 or more body rows)
    const tableRegex = /(?:^|\n)([ \t]*\|[^\n]+\|[ \t]*\n[ \t]*\|(?:\s*:?-+:?\s*\|)+\s*(?:\n[ \t]*\|[^\n]+\|[ \t]*)+)/g;

    let lastIndex = 0;
    let match;

    while ((match = tableRegex.exec(text)) !== null) {
      // Render text prior to the table
      const textBefore = text.slice(lastIndex, match.index);
      if (textBefore) {
        renderInlineContent(textBefore, node);
      }

      // Parse the table block
      const tableString = match[1].trim();
      const rawRows = tableString.split('\n').map((r) => r.trim()).filter(Boolean);

      if (rawRows.length >= 2) {
        const headerCells = rawRows[0]
          .replace(/^\|/, '')
          .replace(/\|$/, '')
          .split('|')
          .map((c) => c.trim());

        const bodyRows = rawRows.slice(2).map((r) =>
          r
            .replace(/^\|/, '')
            .replace(/\|$/, '')
            .split('|')
            .map((c) => c.trim())
        );

        const wrap = document.createElement('div');
        wrap.className = 'q-table-wrap';

        const table = document.createElement('table');
        table.className = 'q-table';

        // <thead>
        const thead = document.createElement('thead');
        const trHead = document.createElement('tr');
        headerCells.forEach((h) => {
          const th = document.createElement('th');
          renderInlineContent(h, th);
          trHead.appendChild(th);
        });
        thead.appendChild(trHead);
        table.appendChild(thead);

        // <tbody>
        const tbody = document.createElement('tbody');
        bodyRows.forEach((row) => {
          const tr = document.createElement('tr');
          row.forEach((cell) => {
            const td = document.createElement('td');
            renderInlineContent(cell, td);
            tr.appendChild(td);
          });
          tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        wrap.appendChild(table);
        node.appendChild(wrap);
      }

      lastIndex = match.index + match[0].length;
    }

    // Render remaining text after last table
    const remainingText = text.slice(lastIndex);
    if (remainingText) {
      renderInlineContent(remainingText, node);
    }
  }, [text]);

  return <span ref={ref} className="mathtext-container" />;
}
