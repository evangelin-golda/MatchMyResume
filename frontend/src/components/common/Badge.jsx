import React from 'react';

export default function Badge({
  children,
  variant = 'neutral',
  size = 'md',
  dot = false,
  icon = null,
  className = '',
  ...props
}) {
  const variants = {
    matched: 'bg-[#D6ECD4] text-[#16431D] border-[#B2DCB0]',
    missing: 'bg-[#FCE8E4] text-[#8C291C] border-[#F5C2BA]',
    warning: 'bg-[#FEF2D6] text-[#7A520E] border-[#F9DC9B]',
    forest: 'bg-forest-800 text-cream-50 border-forest-700',
    neutral: 'bg-cream-100 text-forest-800 border-forest-800/15',
    sage: 'bg-sage-200/70 text-sage-800 border-sage-300',
    mint: 'bg-mint-100 text-forest-800 border-mint-200',
  };

  const dotColors = {
    matched: 'bg-[#16431D]',
    missing: 'bg-[#8C291C]',
    warning: 'bg-[#7A520E]',
    forest: 'bg-cream-50',
    neutral: 'bg-forest-700',
    sage: 'bg-sage-700',
    mint: 'bg-forest-600',
  };

  const sizes = {
    sm: 'text-[11px] px-2.5 py-0.5 font-medium gap-1.5',
    md: 'text-xs px-3 py-1 font-semibold gap-1.5',
    lg: 'text-sm px-3.5 py-1.5 font-semibold gap-2',
  };

  return (
    <span
      className={`
        inline-flex items-center rounded-full border tracking-wide transition-colors
        ${variants[variant] || variants.neutral}
        ${sizes[size] || sizes.md}
        ${className}
      `}
      {...props}
    >
      {dot && (
        <span
          className={`w-1.5 h-1.5 rounded-full shrink-0 ${dotColors[variant] || dotColors.neutral}`}
        />
      )}
      {icon && <span className="shrink-0">{icon}</span>}
      <span>{children}</span>
    </span>
  );
}
