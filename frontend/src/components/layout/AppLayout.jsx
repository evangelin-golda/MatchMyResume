import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import Navbar from './Navbar';
import { Leaf, Heart, ShieldCheck } from 'lucide-react';

export default function AppLayout() {
  return (
    <div className="relative min-h-screen flex flex-col justify-between overflow-x-hidden">
      {/* Subtle nature ambient glow effects inspired by reference */}
      <div className="ambient-glow top-[-100px] left-[-150px] opacity-70" />
      <div className="ambient-glow bottom-[-100px] right-[-150px] opacity-60" />

      {/* Floating Pill Navbar */}
      <Navbar />

      {/* Main Page Content */}
      <main className="relative z-10 flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 md:py-8">
        <Outlet />
      </main>

      {/* Botanical Footer */}
      <footer className="relative z-10 border-t border-forest-800/10 bg-cream-100/60 backdrop-blur-md mt-16 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-forest-800/10">
            {/* Brand column */}
            <div className="md:col-span-2 space-y-3">
              <Link to="/" className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-full bg-forest-800 flex items-center justify-center text-cream-50 shadow-pill">
                  <Leaf className="w-3.5 h-3.5 text-cream-50" />
                </div>
                <div>
                  <span className="font-extrabold text-base tracking-tight text-forest-900 block leading-tight">
                    MatchMyResume
                  </span>
                  <span className="text-[10px] font-bold text-sage-600 tracking-wider uppercase">
                    AI-Powered Job Alignment
                  </span>
                </div>
              </Link>
              <p className="text-xs text-forest-800/75 max-w-sm leading-relaxed">
                Empowering job seekers, students, and professionals with transparent NLP skill matching, mathematical TF-IDF similarity scoring, and Gemini-powered resume refinement.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h5 className="text-xs font-bold uppercase tracking-wider text-forest-900 mb-3">
                Navigation
              </h5>
              <ul className="space-y-2 text-xs">
                <li>
                  <Link to="/" className="text-forest-800/80 hover:text-forest-900 transition-colors">
                    Overview
                  </Link>
                </li>
                <li>
                  <Link to="/analyze" className="text-forest-800/80 hover:text-forest-900 transition-colors">
                    Analyze Resume
                  </Link>
                </li>
                <li>
                  <Link to="/dashboard" className="text-forest-800/80 hover:text-forest-900 transition-colors">
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link to="/insights" className="text-forest-800/80 hover:text-forest-900 transition-colors">
                    AI Insights
                  </Link>
                </li>
              </ul>
            </div>

            {/* Platform Guarantee */}
            <div>
              <h5 className="text-xs font-bold uppercase tracking-wider text-forest-900 mb-3">
                Methodology
              </h5>
              <div className="p-3 rounded-xl bg-cream-50/80 border border-forest-800/8 text-[11px] text-forest-800/80 space-y-1.5">
                <span className="flex items-center gap-1.5 font-semibold text-forest-900">
                  <ShieldCheck className="w-3.5 h-3.5 text-forest-700" />
                  Honest AI Scoring
                </span>
                <p>
                  Objective skill matching and personalized career guidance—grounded strictly in your actual experience.
                </p>
              </div>
            </div>
          </div>

          {/* Bottom row */}
          <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-forest-800/70">
            <p>© {new Date().getFullYear()} MatchMyResume. All rights reserved. Nature-Inspired SaaS.</p>
            <p className="text-[11px] text-sage-600">Built for Portfolio, GitHub & LinkedIn Showcase.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
