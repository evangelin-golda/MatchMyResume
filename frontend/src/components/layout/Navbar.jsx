import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Leaf, Menu, X, ArrowRight } from 'lucide-react';
import Button from '../common/Button';
import { useAnalysis } from '../../context/AnalysisContext';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { hasAnalysis } = useAnalysis();

  const navLinks = [
    { name: 'Overview', path: '/' },
    { name: 'Analyze Resume', path: '/analyze' },
    { name: 'Dashboard', path: '/dashboard', requiresAnalysis: true },
    { name: 'AI Insights', path: '/insights', requiresAnalysis: true },
  ];

  return (
    <header className="sticky top-4 z-40 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
      <nav className="botanical-navbar px-4 sm:px-6 py-2.5 flex items-center justify-between transition-all">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-full bg-forest-800 text-cream-50 flex items-center justify-center shadow-pill group-hover:bg-forest-900 transition-colors">
            <Leaf className="w-4 h-4 text-cream-50" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-base tracking-tight text-forest-900 leading-tight">
              MatchMyResume
            </span>
            <span className="text-[10px] font-semibold text-sage-600 tracking-wider uppercase">
              AI Job Alignment
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <div className="hidden md:flex items-center gap-1.5 lg:gap-2">
          {navLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              end={link.path === '/'}
              className={({ isActive }) => `
                text-xs font-semibold px-3.5 py-1.5 rounded-full transition-all duration-200 relative
                ${isActive
                  ? 'bg-forest-800 text-cream-50 shadow-sm'
                  : 'text-forest-900/80 hover:text-forest-900 hover:bg-forest-800/8'}
              `}
            >
              <span className="flex items-center gap-1.5">
                {link.name}
                {link.requiresAnalysis && hasAnalysis && (
                  <span className="w-1.5 h-1.5 rounded-full bg-mint-400" />
                )}
              </span>
            </NavLink>
          ))}
        </div>

        {/* CTA & Mobile Toggle */}
        <div className="flex items-center gap-2.5">
          <Link to="/analyze" className="hidden sm:inline-flex">
            <Button
              variant="primary"
              size="sm"
              icon={<ArrowRight className="w-3.5 h-3.5" />}
              iconPosition="right"
            >
              Start Analysis
            </Button>
          </Link>

          {/* Mobile Menu Button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-full text-forest-900 hover:bg-forest-800/10 focus:outline-none"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-2 botanical-card p-4 space-y-1.5 animate-in fade-in slide-in-from-top-2 duration-200">
          {navLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              end={link.path === '/'}
              onClick={() => setMobileMenuOpen(false)}
              className={({ isActive }) => `
                block text-sm font-semibold px-4 py-2 rounded-xl transition-all
                ${isActive
                  ? 'bg-forest-800 text-cream-50'
                  : 'text-forest-900 hover:bg-forest-800/8'}
              `}
            >
              {link.name}
            </NavLink>
          ))}
          <div className="pt-2 border-t border-forest-800/10">
            <Link to="/analyze" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="primary" size="md" fullWidth>
                Start Analysis
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
