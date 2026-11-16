import React from 'react';
import { motion } from 'framer-motion';
import {
  FileText,
  Layers,
  Scale,
  Target,
  Sparkles,
  Compass,
  ArrowRight
} from 'lucide-react';
import SectionHeading from '../common/SectionHeading';
import Card from '../common/Card';
import Badge from '../common/Badge';

export default function KeyFeatures() {
  const features = [
    {
      title: 'Resume Parsing',
      badge: 'Smart Resume Understanding',
      description: 'Extract relevant information, education, experience, and projects from your uploaded resume.',
      icon: <FileText className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      title: 'Skill Identification',
      badge: 'Comprehensive Skill Discovery',
      description: 'Identify important technical and professional skills from your resume and target job requirements.',
      icon: <Layers className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      title: 'Job Match Analysis',
      badge: 'Intelligent Job Matching',
      description: 'Understand how well your experience and qualifications align with the requirements of your desired role.',
      icon: <Scale className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      title: 'Skill Gap Detection',
      badge: 'Identify Missing Skills',
      description: 'Discover the important skills you may need to develop to improve your suitability for your target position.',
      icon: <Target className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      title: 'AI Resume Feedback',
      badge: 'Personalized Insights',
      description: 'Receive useful feedback on your resume, including strengths, improvement areas, and suggestions.',
      icon: <Sparkles className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
    {
      title: 'Career Recommendations',
      badge: 'Career Development',
      description: 'Discover relevant skills, projects, and learning opportunities that can help you move towards your career goals.',
      icon: <Compass className="w-5 h-5 text-forest-800 group-hover:text-forest-900 transition-colors" />,
    },
  ];

  return (
    <section className="max-w-6xl mx-auto px-4 py-12 sm:py-16">
      <SectionHeading
        tag="CAPABILITIES"
        title="Comprehensive Suite of Alignment Tools"
        description="Everything you need to evaluate, benchmark, and improve your resume for target career opportunities."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
        {features.map((feature, idx) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-30px" }}
            transition={{ duration: 0.45, delay: idx * 0.08 }}
          >
            <Card
              variant="cream"
              hoverEffect
              className="h-full flex flex-col justify-between p-6 border-forest-800/10 group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  {/* Icon container with preserved contrast on hover */}
                  <div className="w-10 h-10 rounded-xl bg-botanical-200/90 border border-forest-800/12 flex items-center justify-center shadow-pill group-hover:bg-mint-100 group-hover:border-forest-800/25 group-hover:scale-105 transition-all duration-200">
                    {feature.icon}
                  </div>
                  <Badge variant="mint" size="sm">
                    {feature.badge}
                  </Badge>
                </div>

                <h3 className="text-lg font-bold text-forest-900 tracking-tight mb-2.5">
                  {feature.title}
                </h3>

                <p className="text-xs sm:text-sm text-forest-800/75 leading-relaxed font-normal">
                  {feature.description}
                </p>
              </div>

              <div className="pt-4 mt-4 border-t border-forest-800/8 flex items-center text-xs font-semibold text-forest-800 group-hover:text-forest-900 transition-colors">
                <span>Explore capability</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1.5 opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
