// Shared number formatting for fractional marking schemes (e.g. CDS +1 / −⅓).

/** Format a score/marks value: integers stay plain, fractions get ≤2 decimals. */
export function fmtScore(n) {
  if (n === undefined || n === null || Number.isNaN(Number(n))) return '0';
  const num = Number(n);
  if (Number.isInteger(num)) return String(num);
  return String(Math.round(num * 100) / 100);
}

/** Format a per-question wrong-mark penalty label (−⅓ Mark / 0 Marks / −1 Mark). */
export function fmtWrongLabel(w) {
  if (!w || w === 0) return '0 Marks';
  if (Math.abs(w - 1 / 3) < 1e-9) return '−⅓ Mark';
  if (Math.abs(w + 1 / 3) < 1e-9) return '−⅓ Mark';
  if (Number.isInteger(w)) return `−${Math.abs(w)} Mark`;
  return `−${fmtScore(Math.abs(w))} Mark`;
}
