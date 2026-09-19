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
        { id: 'de-ch3', num: 3, title: 'Number Systems', status: 'soon' },
        { id: 'de-ch4', num: 4, title: 'Combinational Circuits', status: 'soon' },
      ],
    },
    {
      id: 'nt',
      name: 'Network Theory',
      icon: 'bolt',
      accent: 'chem',
      chapters: [],
      status: 'soon',
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
