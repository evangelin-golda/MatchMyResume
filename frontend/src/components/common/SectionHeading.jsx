import React from 'react';
import Badge from './Badge';

export default function SectionHeading({
  tag,
  title,
  description,
  align = 'center',
  titleAs: TitleTag = 'h2',
  className = '',
}) {
  const alignClass = {
    left: 'text-left items-start',
    center: 'text-center items-center mx-auto',
    right: 'text-right items-end ml-auto',
  }[align] || 'text-center items-center mx-auto';

  return (
    <div className={`flex flex-col max-w-3xl mb-8 md:mb-12 ${alignClass} ${className}`}>
      {tag && (
        <div className="mb-3">
          <Badge variant="mint" size="sm" dot>
            {tag}
          </Badge>
        </div>
      )}
      <TitleTag className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-forest-900 tracking-tight leading-tight">
        {title}
      </TitleTag>
      {description && (
        <p className="text-sm sm:text-base text-forest-800/75 mt-3 leading-relaxed max-w-2xl font-normal">
          {description}
        </p>
      )}
    </div>
  );
}
