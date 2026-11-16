import React from 'react';

export default function Card({
  children,
  className = '',
  hoverEffect = false,
  variant = 'default',
  onClick,
  ...props
}) {
  const variants = {
    default: 'bg-cream-100/90 border-forest-800/10 text-forest-900',
    cream: 'bg-cream-50/95 border-forest-800/10 text-forest-900',
    mint: 'bg-mint-100/70 border-forest-800/10 text-forest-900',
    glass: 'bg-cream-50/70 backdrop-blur-md border-forest-800/12 text-forest-900',
    flat: 'bg-botanical-100/80 border-forest-800/8 text-forest-900',
  };

  return (
    <div
      onClick={onClick}
      className={`
        rounded-2xl border shadow-soft p-6 transition-all duration-300
        ${variants[variant] || variants.default}
        ${hoverEffect ? 'hover:shadow-soft-lg hover:-translate-y-0.5 cursor-pointer' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, className = '' }) {
  return (
    <div className={`flex items-start justify-between pb-4 border-b border-forest-800/8 mb-4 ${className}`}>
      <div>
        <h3 className="text-lg font-bold text-forest-900 tracking-tight">{title}</h3>
        {subtitle && <p className="text-xs text-sage-600 mt-0.5">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
