import React from 'react';

export default function Textarea({
  label,
  id,
  placeholder,
  value,
  onChange,
  rows = 5,
  error,
  helperText,
  maxLength,
  disabled = false,
  required = false,
  className = '',
  ...props
}) {
  const textareaId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);
  const currentLength = typeof value === 'string' ? value.length : 0;

  return (
    <div className={`w-full ${className}`}>
      <div className="flex justify-between items-center mb-1.5">
        {label && (
          <label
            htmlFor={textareaId}
            className="block text-xs font-semibold text-forest-900 tracking-wide"
          >
            {label} {required && <span className="text-status-missing-text">*</span>}
          </label>
        )}
        {maxLength && (
          <span className="text-[11px] text-sage-600 font-mono">
            {currentLength} / {maxLength}
          </span>
        )}
      </div>
      <textarea
        id={textareaId}
        rows={rows}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        maxLength={maxLength}
        required={required}
        className={`
          w-full rounded-xl bg-cream-50/90 text-forest-900 text-sm placeholder:text-sage-500
          border transition-all duration-200 outline-none p-3.5 leading-relaxed resize-y
          ${error
            ? 'border-status-missing-border focus:border-status-missing-text focus:ring-2 focus:ring-status-missing-border/40'
            : 'border-forest-800/15 focus:border-forest-700 focus:ring-2 focus:ring-forest-700/20'}
          disabled:bg-sage-100/50 disabled:cursor-not-allowed
        `}
        {...props}
      />
      {error ? (
        <p className="text-xs text-status-missing-text mt-1.5 font-medium">{error}</p>
      ) : helperText ? (
        <p className="text-xs text-sage-600 mt-1.5">{helperText}</p>
      ) : null}
    </div>
  );
}
