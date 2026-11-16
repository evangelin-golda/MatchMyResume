import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import Button from '../common/Button';

export default function FinalCta() {
  return (
    <section className="max-w-5xl mx-auto px-4 py-12 sm:py-16">
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true, margin: "-40px" }}
        transition={{ duration: 0.6 }}
        className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#1E3F20] via-[#1B3E22] to-[#142E19] text-cream-50 p-8 sm:p-12 md:p-16 text-center shadow-soft-lg border border-forest-700/30"
      >
        {/* Subtle decorative nature shapes */}
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-forest-600/20 blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 rounded-full bg-mint-400/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cream-50/10 backdrop-blur-md border border-cream-50/15 text-cream-100 text-xs font-semibold mb-6 shadow-pill">
            <Sparkles className="w-3.5 h-3.5 text-mint-300" />
            <span>Ready in under 10 seconds</span>
          </div>

          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-cream-50 tracking-tight leading-tight">
            Your next opportunity starts with a better match.
          </h2>

          <p className="mt-5 text-sm sm:text-base md:text-lg text-cream-200/80 leading-relaxed font-normal">
            Understand where you stand and take the next step towards your career goals.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/analyze">
              <Button
                variant="secondary"
                size="lg"
                icon={<ArrowRight className="w-4 h-4 text-forest-900" />}
                iconPosition="right"
                className="bg-cream-50 text-forest-900 hover:bg-cream-100 border-none font-bold text-base px-8 py-3.5 shadow-soft hover:shadow-soft-lg"
              >
                Start Analysis
              </Button>
            </Link>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-6 text-xs text-cream-200/70 font-medium">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-mint-300" />
              100% Free
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-mint-300" />
              No Account Required
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-mint-300" />
              Zero Data Retention
            </span>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
