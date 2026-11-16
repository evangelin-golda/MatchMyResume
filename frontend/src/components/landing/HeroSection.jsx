import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, Target, Sparkles } from 'lucide-react';
import Button from '../common/Button';
import Badge from '../common/Badge';

export default function HeroSection() {
  return (
    <section className="relative text-center max-w-4xl mx-auto px-4 pt-4 pb-8 sm:pt-8 sm:pb-12">
      {/* Eyebrow Badge */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="inline-block mb-6"
      >
        <Badge variant="mint" size="md" dot className="shadow-pill border-forest-800/10">
          Intelligent Resume Alignment
        </Badge>
      </motion.div>

      {/* Main Headline */}
      <motion.h1
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-forest-900 tracking-tight leading-[1.12]"
      >
        Align your resume with your dream role with ease.
      </motion.h1>

      {/* Supporting Description */}
      <motion.p
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="mt-6 text-base sm:text-lg md:text-xl text-forest-800/80 max-w-2xl mx-auto leading-relaxed font-normal"
      >
        Discover your strengths, identify missing skills, and receive intelligent recommendations to improve your job readiness.
      </motion.p>

      {/* Single Prominent Primary CTA Button */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="mt-8 flex items-center justify-center"
      >
        <Link to="/analyze">
          <Button
            variant="primary"
            size="lg"
            icon={<ArrowRight className="w-4 h-4" />}
            iconPosition="right"
            className="shadow-soft hover:shadow-soft-md px-8 py-3.5 text-base"
          >
            Start Analysis
          </Button>
        </Link>
      </motion.div>

      {/* Non-Technical User-Friendly Trust Highlights */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.7, delay: 0.45 }}
        className="mt-10 flex flex-wrap items-center justify-center gap-6 text-xs text-forest-800/75"
      >
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-forest-700" />
          <span>Private & In-Memory Processing</span>
        </div>
        <div className="flex items-center gap-2">
          <Target className="w-4 h-4 text-forest-700" />
          <span>Objective Skill Gap Detection</span>
        </div>
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-forest-700" />
          <span>Personalized Career Suggestions</span>
        </div>
      </motion.div>
    </section>
  );
}
