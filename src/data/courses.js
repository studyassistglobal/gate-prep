// Course registry — the single place to extend the site with new subjects,
// chapters and courses. Live chapters point at generated modules in
// src/data/notes/<subject>/<file>.js (built by scripts/build_notes.py).

export const COURSE = {
  id: 'gate-2027-ece',
  name: 'GATE 2027 Full Course (ECE)',
  breadcrumb: 'GATE 2027 FULL SUBSCRIPTION (ECE)',
  description:
    'The complete GATE 2027 ECE preparation course — deep, faculty-style chapter notes with solved examples, faculty insights and exam strategy. Free to read, no sign-up needed.',
  subjects: [
    {
      id: 'de',
      name: 'Digital Electronics',
      icon: 'memory',
      accent: 'phy',
      chapters: [
        { id: 'de-ch1', num: 1, title: 'Logic Gates & Boolean Algebra', status: 'live', file: 'ch1' },
        { id: 'de-ch2', num: 2, title: 'Representation of Boolean Expressions & K-Maps', status: 'live', file: 'ch2' },
        { id: 'de-ch3', num: 3, title: 'Number Systems & Digital Representation', status: 'live', file: 'ch3' },
        { id: 'de-ch4-p1', num: 4, part: 1, title: 'Combinational Circuits — Arithmetic Logic', status: 'live', file: 'ch4p1' },
        { id: 'de-ch4-p2', num: 4, part: 2, title: 'Combinational Circuits — Advanced Architectures', status: 'live', file: 'ch4p2' },
      ],
    },
    {
      id: 'ss',
      name: 'Signals & Systems',
      icon: 'graphic_eq',
      accent: 'math',
      chapters: [
        { id: 'ss-ch1', num: 1, title: 'Basics of Signals', status: 'live', file: 'ssch1' },
        { id: 'ss-ch2', num: 2, title: 'Basics of Systems', status: 'live', file: 'ssch2' },
        { id: 'ss-ch3', num: 3, title: 'Continuous-Time Fourier Series (CTFS)', status: 'live', file: 'ssch3' },
        { id: 'ss-ch4', num: 4, title: 'Fourier Transform & Sampling Theorem', status: 'live', file: 'ssch4' },
        { id: 'ss-ch5', num: 5, title: 'Continuous-Time Laplace Transform', status: 'live', file: 'ssch5' },
        { id: 'ss-ch6', num: 6, title: 'Discrete-Time Z-Transform', status: 'live', file: 'ssch6' },
        { id: 'ss-ch7', num: 7, title: 'DTFT, DTFS, DFT & FFT', status: 'live', file: 'ssch7' },
      ],
    },
    {
      id: 'ssf',
      kind: 'sheets',
      name: 'S&S Formula Sheets',
      icon: 'functions',
      accent: 'math',
      chapters: [
        { id: 'ssf-ch1', num: 1, title: 'Basics of Signals — Formula & Revision Sheet', status: 'live', file: 'ssfch1' },
        { id: 'ssf-ch2', num: 2, title: 'Basics of Systems — Formula & Revision Sheet', status: 'live', file: 'ssfch2' },
        { id: 'ssf-ch3', num: 3, title: 'Fourier Series (CTFS) — Formula & Revision Sheet', status: 'live', file: 'ssfch3' },
        { id: 'ssf-ch4', num: 4, title: 'Fourier Transform & Sampling — Formula & Revision Sheet', status: 'live', file: 'ssfch4' },
        { id: 'ssf-ch5', num: 5, title: 'Laplace Transform — Formula & Revision Sheet', status: 'live', file: 'ssfch5' },
        { id: 'ssf-ch6', num: 6, title: 'Z-Transform — Formula & Revision Sheet', status: 'live', file: 'ssfch6' },
        { id: 'ssf-ch7', num: 7, title: 'DTFT, DTFS, DFT & FFT — Formula & Revision Sheet', status: 'live', file: 'ssfch7' },
      ],
    },
    {
      id: 'nt',
      name: 'Network Theory',
      icon: 'bolt',
      accent: 'chem',
      chapters: [
        { id: 'nt-ch1', num: 1, title: 'Basics of Network Analysis', status: 'live', file: 'nt1' },
        { id: 'nt-ch2', num: 2, title: 'Network Theorems & Circuit Equivalence', status: 'live', file: 'nt2' },
        { id: 'nt-ch3', num: 3, title: 'Transient Analysis', status: 'live', file: 'nt3' },
      ],
    },
    {
      id: 'ntf',
      kind: 'sheets',
      name: 'NT Formula Sheets',
      icon: 'bolt',
      accent: 'chem',
      chapters: [
        { id: 'ntf-ch1', num: 1, title: 'Basics of Network — Formula & Revision Sheet', status: 'live', file: 'ntf1' },
        { id: 'ntf-ch2', num: 2, title: 'Network Theorems — Formula & Revision Sheet', status: 'live', file: 'ntf2' },
        { id: 'ntf-ch3', num: 3, title: 'Transient Analysis — Formula & Revision Sheet', status: 'live', file: 'ntf3' },
      ],
    },
    {
      id: 'em',
      name: 'Engineering Mathematics',
      icon: 'calculate',
      accent: 'math',
      chapters: [
        { id: 'em-ch1', num: 1, title: 'Linear Algebra', status: 'live', file: 'emch1' },
        { id: 'em-ch2', num: 2, title: 'Calculus', status: 'live', file: 'emch2' },
        { id: 'em-ch3', num: 3, title: 'Vector Calculus', status: 'live', file: 'emch3' },
        { id: 'em-ch4', num: 4, title: 'Complex Analysis', status: 'live', file: 'emch4' },
        { id: 'em-ch5', num: 5, title: 'Differential Equations', status: 'live', file: 'emch5' },
        { id: 'em-ch6', num: 6, title: 'Probability, Random Variables & Statistics', status: 'live', file: 'emch6' },
      ],
    },
    {
      id: 'emf',
      kind: 'sheets',
      name: 'EM Formula Sheets',
      icon: 'calculate',
      accent: 'math',
      chapters: [
        { id: 'emf-ch1', num: 1, title: 'Linear Algebra — Formula & Revision Sheet', status: 'live', file: 'emfch1' },
        { id: 'emf-ch2', num: 2, title: 'Calculus — Formula & Revision Sheet', status: 'live', file: 'emfch2' },
        { id: 'emf-ch3', num: 3, title: 'Vector Calculus — Formula & Revision Sheet', status: 'live', file: 'emfch3' },
        { id: 'emf-ch4', num: 4, title: 'Complex Analysis — Formula & Revision Sheet', status: 'live', file: 'emfch4' },
        { id: 'emf-ch5', num: 5, title: 'Differential Equations — Formula & Revision Sheet', status: 'live', file: 'emfch5' },
        { id: 'emf-ch6', num: 6, title: 'Probability & Statistics — Formula & Revision Sheet', status: 'live', file: 'emfch6' },
      ],
    },
    {
      id: 'edc',
      name: 'Electronic Devices & Circuits',
      icon: 'developer_board',
      accent: 'chem',
      chapters: [
        { id: 'edc-ch1', num: 1, title: 'Electronic Devices & Circuits (EDC)', status: 'live', file: 'edcch1' },
      ],
    },
    {
      id: 'edcf',
      kind: 'sheets',
      name: 'EDC Formula Sheets',
      icon: 'developer_board',
      accent: 'chem',
      chapters: [
        { id: 'edcf-ch1', num: 1, title: 'EDC — Formula & Revision Sheet', status: 'live', file: 'edcfch1' },
      ],
    },
    {
      id: 'ae',
      name: 'Analog Electronics',
      icon: 'tune',
      accent: 'chem',
      chapters: [
        { id: 'ae-ch1', num: 1, title: 'Diode Circuits & Wave Shaping', status: 'live', file: 'ae1' },
        { id: 'ae-ch2', num: 2, title: 'Rectifiers & Filters', status: 'live', file: 'ae2' },
      ],
    },
    {
      id: 'aef',
      kind: 'sheets',
      name: 'Analog Electronics Formula Sheets',
      icon: 'tune',
      accent: 'chem',
      chapters: [
        { id: 'aef-ch1', num: 1, title: 'Diode Circuits & Rectifiers — Formula & Revision Sheet', status: 'live', file: 'aef1' },
      ],
    },
  ],
};

export function getCourse(courseId) {
  return COURSE.id === courseId ? COURSE : null;
}

export function findChapter(courseId, chapterId) {
  if (COURSE.id !== courseId) return null;
  for (const s of COURSE.subjects) {
    const ch = s.chapters.find((c) => c.id === chapterId);
    if (ch) return { subject: s, chapter: ch };
  }
  return null;
}

/** Flat list of {chapter, subject} for prev/next navigation. */
export function liveChapterSequence(courseId) {
  if (COURSE.id !== courseId) return [];
  return COURSE.subjects.flatMap((s) => s.chapters.filter((c) => c.status === 'live').map((c) => ({ subject: s, chapter: c })));
}

/** "Ch 3" or "Ch 4.2" for part-split chapters. */
export function chapterLabel(chapter) {
  return `Ch ${chapter.num}${chapter.part ? `.${chapter.part}` : ''}`;
}
