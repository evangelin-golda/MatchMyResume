import React from 'react';

export default function Input({
  label,
  id,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  helperText,
  icon = null,
  disabled = false,
  required = false,
  className = '',
  ...props
}) {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label
          htmlFor={inputId}
          className="block text-xs font-semibold text-forest-900 mb-1.5 tracking-wide"
        >
          {label} {required && <span className="text-status-missing-text">*</span>}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-sage-600">
            {icon}
          </div>
        )}
        <input
          id={inputId}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          className={`
            w-full rounded-xl bg-cream-50/90 text-forest-900 text-sm placeholder:text-sage-500
            border transition-all duration-200 outline-none
            ${icon ? 'pl-10' : 'pl-3.5'} pr-3.5 py-2.5
            ${error
              ? 'border-status-missing-border focus:border-status-missing-text focus:ring-2 focus:ring-status-missing-border/40'
              : 'border-forest-800/15 focus:border-forest-700 focus:ring-2 focus:ring-forest-700/20'}
            disabled:bg-sage-100/50 disabled:cursor-not-allowed
          `}
          {...props}
        />
      </div>
      {error ? (
        <p className="text-xs text-status-missing-text mt-1.5 font-medium">{error}</p>
      ) : helperText ? (
        <p className="text-xs text-sage-600 mt-1.5">{helperText}</p>
      ) : null}
    </div>
  );
}
