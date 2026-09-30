export default function Logo({ className = "" }: { className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <svg width="30" height="30" viewBox="0 0 32 32" fill="none" strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M14 7 L5 16 L14 25" stroke="var(--blue)" />
        <path d="M18 7 L27 16 L18 25" stroke="var(--coral)" />
        <circle cx="16" cy="16" r="2" fill="var(--gold)" stroke="none" />
      </svg>
      <span className="font-display text-lg font-bold tracking-tight">CodeArena</span>
    </span>
  );
}
