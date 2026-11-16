import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  ArrowLeft,
  BookOpen,
  ArrowRight,
  TrendingUp,
  FileEdit,
  Award
} from 'lucide-react';
import SectionHeading from '../components/common/SectionHeading';
import Card, { CardHeader } from '../components/common/Card';
import Badge from '../components/common/Badge';
import Button from '../components/common/Button';
import { useAnalysis } from '../context/AnalysisContext';

export default function InsightsPage() {
  const navigate = useNavigate();
  const { analysisResult } = useAnalysis();

  if (!analysisResult) {
    return (
      <div className="max-w-md mx-auto text-center py-20">
        <h3 className="text-xl font-bold text-forest-900">No Active Analysis</h3>
        <p className="text-xs text-sage-600 mt-2">Please complete a resume analysis from the dashboard first.</p>
        <Link to="/analyze" className="mt-6 inline-block">
          <Button variant="primary">Start Analysis</Button>
        </Link>
      </div>
    );
  }

  const { ai_insights, similarity_metrics, skill_analysis } = analysisResult;

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4 sm:py-6">
      {/* Header & Back Action */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-forest-800/8 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-sage-600">Deep Guidance</span>
            <Badge variant="mint" size="sm" dot>Context-Aware AI</Badge>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-900 tracking-tight mt-0.5">
            AI Recommendations & Career Strategy
          </h1>
          <p className="text-xs text-sage-600 mt-1">
            Personalized guidance grounded in your resume text and target role requirements.
          </p>
        </div>

        <button
          onClick={() => navigate('/dashboard')}
          className="inline-flex items-center gap-1.5 text-xs font-semibold px-4 py-2 rounded-full bg-cream-50 hover:bg-cream-100 text-forest-800 border border-forest-800/10 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Dashboard</span>
        </button>
      </div>

      {/* 1. Executive Summary */}
      <Card variant="glass" className="p-6">
        <div className="flex items-start gap-3.5">
          <div className="w-9 h-9 rounded-xl bg-forest-800 text-cream-50 flex items-center justify-center shrink-0 shadow-pill mt-0.5">
            <Sparkles className="w-4 h-4 text-cream-50" />
          </div>
          <div>
            <h3 className="text-base font-bold text-forest-900">Executive Alignment Summary</h3>
            <p className="text-xs sm:text-sm text-forest-800/85 mt-1.5 leading-relaxed">
              {ai_insights?.summary}
            </p>
          </div>
        </div>
      </Card>

      {/* 2. Strengths & Weaknesses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <Card variant="glass" className="p-5">
          <CardHeader
            title="Resume Strengths"
            subtitle="Verified highlights directly matched against job expectations"
            action={<Badge variant="matched" size="sm" dot>Verified</Badge>}
          />
          <ul className="space-y-2.5 text-xs sm:text-sm">
            {ai_insights?.strengths?.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2 text-forest-800/90 leading-relaxed">
                <CheckCircle2 className="w-4 h-4 text-forest-700 shrink-0 mt-0.5" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </Card>

        {/* Weaknesses */}
        <Card variant="glass" className="p-5">
          <CardHeader
            title="Resume Weaknesses & Gaps"
            subtitle="Omissions or areas where qualifications are under-represented"
            action={<Badge variant="missing" size="sm">Gaps</Badge>}
          />
          <ul className="space-y-2.5 text-xs sm:text-sm">
            {ai_insights?.weaknesses?.map((wk, idx) => (
              <li key={idx} className="flex items-start gap-2 text-forest-800/90 leading-relaxed">
                <AlertTriangle className="w-4 h-4 text-[#8C291C] shrink-0 mt-0.5" />
                <span>{wk}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      {/* 3. Missing Skill Explanations */}
      {ai_insights?.missing_skill_explanations?.length > 0 && (
        <Card variant="glass" className="p-6">
          <CardHeader
            title="Missing Skill Deep-Dive"
            subtitle="Understanding why employers require these competencies and how to demonstrate related experience"
            action={<Badge variant="missing" size="sm">Employer Expectations</Badge>}
          />
          <div className="space-y-3 mt-4">
            {ai_insights.missing_skill_explanations.map((item, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-cream-50/80 border border-forest-800/8 text-xs sm:text-sm">
                <p className="font-bold text-forest-900 flex items-center gap-2">
                  <Badge variant="missing" size="sm">{item.skill}</Badge>
                  <span>Requirement Context:</span>
                </p>
                <p className="text-forest-800/80 mt-1.5 leading-relaxed pl-1">
                  {item.context}
                </p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* 4. Actionable Bullet Point Improvements (Google XYZ Format) */}
      <Card variant="glass" className="p-6">
        <CardHeader
          title="Resume Bullet Point Improvements"
          subtitle="Transform task descriptions into high-impact Google XYZ accomplishment bullets"
          action={<Badge variant="warning" size="sm">Google XYZ Format</Badge>}
        />
        <div className="space-y-4 mt-4">
          {ai_insights?.bullet_point_improvements?.map((item, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-cream-50/90 border border-forest-800/10 space-y-2.5 text-xs sm:text-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-sage-600">Original Phrasing:</span>
                <span className="text-[11px] text-[#8C291C] font-semibold bg-[#FCE8E4] px-2 py-0.5 rounded-full">Passive</span>
              </div>
              <p className="text-sage-700 italic pl-2 border-l-2 border-sage-300">
                "{item.original}"
              </p>

              <div className="pt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-forest-900">Recommended Improvement:</span>
                  <span className="text-[11px] text-[#16431D] font-semibold bg-[#D6ECD4] px-2 py-0.5 rounded-full">Quantified Result</span>
                </div>
                <p className="text-forest-900 font-semibold bg-[#E8F3DE]/80 p-3 rounded-xl border border-[#B2DCB0] leading-relaxed">
                  "{item.improved}"
                </p>
              </div>

              <p className="text-[11px] text-sage-600 mt-1 pl-1">
                <span className="font-semibold text-forest-900">Why this works:</span> {item.explanation}
              </p>
            </div>
          ))}
        </div>
      </Card>

      {/* 5. Career & Skill Growth Recommendations */}
      <Card variant="glass" className="p-6">
        <CardHeader
          title="Career Development Recommendations"
          subtitle="Highest-leverage learning steps to maximize interview success"
          action={<Badge variant="mint" size="sm">Next Steps</Badge>}
        />
        <div className="space-y-3 mt-4">
          {ai_insights?.career_recommendations?.map((rec, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-botanical-100/70 border border-forest-800/10 flex items-start gap-3 text-xs sm:text-sm">
              <span className="w-6 h-6 rounded-full bg-forest-800 text-cream-50 flex items-center justify-center shrink-0 text-xs font-bold mt-0.5">
                {idx + 1}
              </span>
              <p className="text-forest-900 font-medium leading-relaxed">
                {rec}
              </p>
            </div>
          ))}
        </div>
      </Card>

      {/* Footer Navigation */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-forest-800/10">
        <button
          onClick={() => navigate('/dashboard')}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-forest-800 hover:text-forest-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Dashboard</span>
        </button>

        <Link to="/analyze">
          <Button variant="secondary" size="md">
            Analyze Another Role
          </Button>
        </Link>
      </div>
    </div>
  );
}
