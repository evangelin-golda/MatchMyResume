import React from 'react';
import { motion } from 'framer-motion';
import { UploadCloud, FileText, Cpu, Sparkles, ArrowRight } from 'lucide-react';
import SectionHeading from '../common/SectionHeading';
import Card from '../common/Card';

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Upload Resume',
      badge: 'Simple & Secure',
      description: 'Upload your PDF resume and let MatchMyResume understand your experience, education, projects, and skills.',
      icon: <UploadCloud className="w-6 h-6 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      number: '02',
      title: 'Add Job Description',
      badge: 'Understand Job Requirements',
      description: 'Share your target job description so we can identify the important qualifications and skills employers are looking for.',
      icon: <FileText className="w-6 h-6 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      number: '03',
      title: 'Intelligent Analysis',
      badge: 'Detailed Resume Matching',
      description: 'Discover how closely your experience and skills align with the requirements of your desired role.',
      icon: <Cpu className="w-6 h-6 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      number: '04',
      title: 'Get Recommendations',
      badge: 'Actionable Career Insights',
      description: 'Receive personalized feedback, discover missing skills, and find practical ways to strengthen your resume.',
      icon: <Sparkles className="w-6 h-6 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
  ];

  return (
    <section id="how-it-works" className="max-w-6xl mx-auto px-4 py-12 sm:py-16 scroll-mt-24">
      <SectionHeading
        tag="HOW IT WORKS"
        title="Simple 4-Step Alignment Process"
        description="Experience an effortless, transparent evaluation from PDF upload to targeted career refinement."
      />

      <div className="relative mt-12">
        {/* Subtle connecting line for desktop view */}
        <div className="hidden lg:block absolute top-1/2 left-8 right-8 h-0.5 bg-forest-800/10 -translate-y-8 z-0" />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
          {steps.map((step, idx) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, delay: idx * 0.12 }}
            >
              <Card
                variant="glass"
                hoverEffect
                className="h-full flex flex-col justify-between p-6 relative group"
              >
                <div>
                  {/* Top row with step number and icon - fixed hover styles */}
                  <div className="flex items-center justify-between mb-5">
                    <div className="w-12 h-12 rounded-2xl bg-botanical-200/90 border border-forest-800/15 flex items-center justify-center shadow-pill group-hover:scale-105 group-hover:bg-mint-100 group-hover:border-forest-800/30 transition-all duration-300">
                      {step.icon}
                    </div>
                    <span className="font-mono text-2xl font-extrabold text-forest-900/25 tracking-tighter">
                      {step.number}
                    </span>
                  </div>

                  <span className="inline-block text-[11px] font-bold text-forest-800 bg-mint-100/90 px-2.5 py-0.5 rounded-full border border-forest-800/10 mb-2">
                    {step.badge}
                  </span>

                  <h3 className="text-lg font-bold text-forest-900 tracking-tight mt-1 mb-2">
                    {step.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-forest-800/75 leading-relaxed font-normal">
                    {step.description}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-forest-800/8 flex items-center text-xs font-semibold text-forest-800 group-hover:text-forest-900 transition-colors">
                  <span>Step {step.number}</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1.5 opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
