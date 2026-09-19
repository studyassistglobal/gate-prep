// Reading progress, persisted in localStorage (no login needed on this site).
// Shape: { [chapterId]: [sectionId, ...] } under 'gp_progress_v1'.

const KEY = 'gp_progress_v1';

function read() {
  try {
    return JSON.parse(window.localStorage.getItem(KEY) || '{}');
  } catch {
    return {};
  }
}

function write(data) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(data));
  } catch {
    /* private mode — progress just won't persist */
  }
}

export function getReadSections(chapterId) {
  return new Set(read()[chapterId] || []);
}

export function isSectionRead(chapterId, sectionId) {
  return read()[chapterId]?.includes(sectionId) || false;
}

export function toggleSectionRead(chapterId, sectionId) {
  const data = read();
  const set = new Set(data[chapterId] || []);
  if (set.has(sectionId)) set.delete(sectionId);
  else set.add(sectionId);
  data[chapterId] = [...set];
  write(data);
  return set.has(sectionId);
}

export function markAllRead(chapterId, sectionIds) {
  const data = read();
  data[chapterId] = [...new Set(sectionIds)];
  write(data);
}

/** Read count + percentage for a chapter (used on course/home cards). */
export function chapterProgress(chapterId, totalSections) {
  const n = (read()[chapterId] || []).length;
  return { read: n, total: totalSections, pct: totalSections ? Math.round((n / totalSections) * 100) : 0 };
}
