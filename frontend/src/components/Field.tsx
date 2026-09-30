import type { InputHTMLAttributes } from "react";

type FieldProps = { label: string; id: string; error?: string; hint?: string } & InputHTMLAttributes<HTMLInputElement>;

export default function Field({ label, id, error, hint, ...props }: FieldProps) {
  const describedBy = error ? `${id}-error` : hint ? `${id}-hint` : undefined;
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-sm font-medium">
        {label}
      </label>
      <input
        id={id}
        name={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        className={`w-full rounded-lg border bg-ink px-3.5 py-2.5 text-text placeholder:text-muted/60 focus:border-gold focus:outline-none ${
          error ? "border-coral" : "border-line"
        }`}
        {...props}
      />
      {error ? (
        <p id={`${id}-error`} className="mt-1.5 text-sm text-coral">
          {error}
        </p>
      ) : hint ? (
        <p id={`${id}-hint`} className="mt-1.5 text-sm text-muted">
          {hint}
        </p>
      ) : null}
    </div>
  );
}
