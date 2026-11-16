import React from 'react';
import { motion } from 'framer-motion';
import { Leaf } from 'lucide-react';

export default function LoadingIndicator({
  title = 'Processing...',
  subtitle = null,
  fullScreen = false,
  size = 'md',
  className = '',
}) {
  const containerSize = {
    sm: 'w-10 h-10',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
  }[size] || 'w-16 h-16';

  const iconSize = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }[size] || 'w-8 h-8';

  const content = (
    <div className={`flex flex-col items-center justify-center text-center p-6 ${className}`}>
      <div className={`relative flex items-center justify-center ${containerSize} mb-4`}>
        {/* Pulsing botanical concentric rings */}
        <motion.div
          animate={{ scale: [1, 1.25, 1], opacity: [0.35, 0.15, 0.35] }}
          transition={{ repeat: Infinity, duration: 2.2, ease: "easeInOut" }}
          className="absolute inset-0 rounded-full bg-botanical-400"
        />
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 3.5, ease: "linear" }}
          className="absolute inset-0 rounded-full border-2 border-forest-800/20 border-t-forest-800"
        />
        {/* Central leaf emblem */}
        <div className="relative z-10 w-3/4 h-3/4 rounded-full bg-cream-50 flex items-center justify-center shadow-soft border border-forest-800/10">
          <motion.div
            animate={{ scale: [0.95, 1.08, 0.95] }}
            transition={{ repeat: Infinity, duration: 1.8, ease: "easeInOut" }}
          >
            <Leaf className={`${iconSize} text-forest-800`} />
          </motion.div>
        </div>
      </div>

      <h4 className="text-base font-bold text-forest-900 tracking-tight">{title}</h4>
      {subtitle && (
        <p className="text-xs text-sage-700 max-w-sm mt-1.5 leading-relaxed font-normal">
          {subtitle}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-botanical-100/60 backdrop-blur-sm">
        <div className="bg-cream-100/95 border border-forest-800/10 rounded-3xl p-8 shadow-soft-lg">
          {content}
        </div>
      </div>
    );
  }

  return content;
}
