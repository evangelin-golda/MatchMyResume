import React from 'react';
import { motion } from 'framer-motion';
import {
  CheckCircle2,
  XCircle,
  HelpCircle,
  Eye,
  Target,
  Search,
  Sparkles,
  TrendingUp,
  ShieldCheck
} from 'lucide-react';
import SectionHeading from '../common/SectionHeading';
import Card from '../common/Card';
import Badge from '../common/Badge';

export default function WhyMatchMyResume() {
  const valuePillars = [
    {
      title: 'Understand Your Resume Better',
      desc: 'Gain objective visibility into how your experience is parsed, eliminating recruiter blind spots.',
      icon: <Eye className="w-5 h-5 text-forest-800" />,
    },
    {
      title: 'Identify Missing Job Requirements',
      desc: 'Detect specific technical competencies that employers list but your resume currently omits.',
      icon: <Target className="w-5 h-5 text-forest-800" />,
    },
    {
      title: 'Discover Your Skill Gaps',
      desc: 'Separate what you already know from the critical skills needed to qualify for desired roles.',
      icon: <Search className="w-5 h-5 text-forest-800" />,
    },
    {
      title: 'Improve Resume Quality',
      desc: 'Transform passive duties into quantified accomplishment statements that catch recruiters’ eyes.',
      icon: <Sparkles className="w-5 h-5 text-forest-800" />,
    },
    {
      title: 'Make Informed Career Decisions',
      desc: 'Target roles where your match is highest, saving countless hours on misaligned applications.',
      icon: <TrendingUp className="w-5 h-5 text-forest-800" />,
    },
  ];

  return (
    <section className="max-w-6xl mx-auto px-4 py-12 sm:py-16">
      <SectionHeading
        tag="PROVEN VALUE"
        title="Why Choose MatchMyResume?"
        description="Stop submitting applications into the dark. Build resumes backed by objective skill alignment and intelligent feedback."
      />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center mt-12">
        {/* Left: 5 Value Pillars (7 cols) */}
        <div className="lg:col-span-7 space-y-3.5">
          {valuePillars.map((pillar, idx) => (
            <motion.div
              key={pillar.title}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: "-20px" }}
              transition={{ duration: 0.4, delay: idx * 0.08 }}
            >
              <div className="p-4 rounded-2xl bg-cream-100/90 border border-forest-800/10 hover:border-forest-800/25 transition-all flex items-start gap-4 group">
                <div className="w-9 h-9 rounded-xl bg-botanical-200/80 border border-forest-800/15 flex items-center justify-center shrink-0 text-forest-800 group-hover:bg-mint-100 group-hover:border-forest-800/30 transition-colors">
                  {pillar.icon}
                </div>
                <div>
                  <h4 className="text-sm sm:text-base font-bold text-forest-900 group-hover:text-forest-800 transition-colors">
                    {pillar.title}
                  </h4>
                  <p className="text-xs sm:text-sm text-forest-800/75 mt-0.5 leading-relaxed font-normal">
                    {pillar.desc}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Right: Comparison Matrix Card (5 cols) */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-20px" }}
          transition={{ duration: 0.6 }}
          className="lg:col-span-5"
        >
          <div className="botanical-card p-6 sm:p-7 shadow-soft border border-forest-800/12">
            <div className="flex items-center justify-between pb-4 border-b border-forest-800/8 mb-4">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-sage-600">Comparison</span>
                <h4 className="text-base font-bold text-forest-900">How We Stand Apart</h4>
              </div>
              <Badge variant="matched" dot>Honest AI</Badge>
            </div>

            <div className="space-y-4 text-xs">
              {/* Feature 1 */}
              <div className="p-3 rounded-xl bg-cream-50/90 border border-forest-800/8 space-y-1.5">
                <p className="font-bold text-forest-900">Score Transparency</p>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-sage-600">Manual / Guesswork:</span>
                  <span className="text-red-700 flex items-center gap-1 font-medium"><XCircle className="w-3 h-3" /> Blind Guessing</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-forest-900 font-semibold">MatchMyResume:</span>
                  <span className="text-forest-800 flex items-center gap-1 font-bold"><CheckCircle2 className="w-3.5 h-3.5 text-forest-700" /> Objective Scoring</span>
                </div>
              </div>

              {/* Feature 2 */}
              <div className="p-3 rounded-xl bg-cream-50/90 border border-forest-800/8 space-y-1.5">
                <p className="font-bold text-forest-900">Accuracy & Integrity</p>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-sage-600">Generic Chatbots:</span>
                  <span className="text-amber-700 flex items-center gap-1 font-medium"><HelpCircle className="w-3 h-3" /> Fictional claims</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-forest-900 font-semibold">MatchMyResume:</span>
                  <span className="text-forest-800 flex items-center gap-1 font-bold"><CheckCircle2 className="w-3.5 h-3.5 text-forest-700" /> Grounded In Text</span>
                </div>
              </div>

              {/* Feature 3 */}
              <div className="p-3 rounded-xl bg-cream-50/90 border border-forest-800/8 space-y-1.5">
                <p className="font-bold text-forest-900">Skill Discovery</p>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-sage-600">Manual Reading:</span>
                  <span className="text-sage-700 font-medium">Misses subtle skill variants</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-forest-900 font-semibold">MatchMyResume:</span>
                  <span className="text-forest-800 flex items-center gap-1 font-bold"><CheckCircle2 className="w-3.5 h-3.5 text-forest-700" /> 500+ Curated Skills</span>
                </div>
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-forest-800/8 flex items-center justify-center gap-2 text-xs font-semibold text-forest-800">
              <ShieldCheck className="w-4 h-4 text-forest-700" />
              <span>Free, private, and zero subscription traps</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
