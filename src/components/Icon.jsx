/**
 * Material Symbols icon wrapper. Usage:
 *   <Icon name="school" filled />
 *   <Icon name="timer" className="ic-sm" />
 * The `filled` prop sets font-variation FILL=1.
 */
export default function Icon({ name, filled = false, className = '', style }) {
  return (
    <span
      className={`material-symbols-outlined ${className}`}
      style={{
        fontVariationSettings: `'FILL' ${filled ? 1 : 0}, 'wght' 400, 'GRAD' 0, 'opsz' 24`,
        ...style,
      }}
      aria-hidden="true"
    >
      {name}
    </span>
  );
}