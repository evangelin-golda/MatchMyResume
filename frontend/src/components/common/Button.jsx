import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  isLoading = false,
  disabled = false,
  icon = null,
  iconPosition = 'left',
  className = '',
  onClick,
  type = 'button',
  ...props
}) {
  const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-forest-700/30 active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed disabled:active:scale-100 cursor-pointer';

  const variants = {
    primary: 'bg-forest-800 hover:bg-forest-900 text-cream-50 shadow-pill hover:shadow-soft-md border border-forest-700/20',
    secondary: 'bg-cream-100 hover:bg-botanical-100 text-forest-800 border border-forest-800/15 shadow-sm',
    outline: 'bg-transparent hover:bg-forest-800/8 text-forest-800 border border-forest-800/30',
    ghost: 'bg-transparent hover:bg-forest-800/8 text-forest-800',
    soft: 'bg-botanical-200/70 hover:bg-botanical-300/80 text-forest-900 border border-forest-800/10',
    danger: 'bg-status-missing-bg text-status-missing-text border border-status-missing-border hover:bg-red-100'
  };

  const sizes = {
    sm: 'text-xs px-3.5 py-1.5 rounded-full gap-1.5',
    md: 'text-sm px-5 py-2.5 rounded-full gap-2',
    lg: 'text-base px-6 py-3 rounded-full gap-2.5',
  };

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      className={`
        ${baseStyles}
        ${variants[variant] || variants.primary}
        ${sizes[size] || sizes.md}
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `}
      {...props}
    >
      {isLoading ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin text-current" />
          <span>Loading...</span>
        </>
      ) : (
        <>
          {icon && iconPosition === 'left' && <span className="shrink-0">{icon}</span>}
          {children}
          {icon && iconPosition === 'right' && <span className="shrink-0">{icon}</span>}
        </>
      )}
    </button>
  );
}
