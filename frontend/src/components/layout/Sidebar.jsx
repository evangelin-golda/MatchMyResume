import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  Sparkles,
  BarChart3,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({ className = '' }) {
  const primaryNav = [
    { name: 'Overview', path: '/', icon: <LayoutDashboard className="w-4 h-4" /> },
    { name: 'Analyze Resume', path: '/analyze', icon: <FileText className="w-4 h-4" /> },
    { name: 'Results Dashboard', path: '/dashboard', icon: <BarChart3 className="w-4 h-4" /> },
    { name: 'AI Recommendations', path: '/insights', icon: <Sparkles className="w-4 h-4" /> },
  ];

  return (
    <aside className={`w-64 shrink-0 flex flex-col justify-between botanical-card p-4 h-full ${className}`}>
      <div>
        {/* Workspace Title */}
        <div className="px-3 py-2 mb-4 border-b border-forest-800/8">
          <p className="text-[10px] font-bold uppercase tracking-wider text-sage-600">Workspace</p>
          <h4 className="text-sm font-bold text-forest-900 mt-0.5">Resume Lab</h4>
        </div>

        {/* Primary Navigation */}
        <div className="space-y-1">
          <p className="text-[10px] font-bold uppercase tracking-wider text-sage-600 px-3 mb-2">
            Main Menu
          </p>
          {primaryNav.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) => `
                flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all
                ${isActive
                  ? 'bg-forest-800 text-cream-50 shadow-sm'
                  : 'text-forest-900/80 hover:bg-forest-800/8 hover:text-forest-900'}
              `}
            >
              <div className="flex items-center gap-2.5">
                {item.icon}
                <span>{item.name}</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 opacity-60" />
            </NavLink>
          ))}
        </div>
      </div>

      {/* Footer info badge */}
      <div className="mt-6 p-3 rounded-xl bg-botanical-100/70 border border-forest-800/10">
        <p className="text-[11px] font-bold text-forest-900">Match Engine v1.0</p>
        <p className="text-[10px] text-sage-600 mt-0.5">TF-IDF + Cosine Similarity + Gemini</p>
      </div>
    </aside>
  );
}
