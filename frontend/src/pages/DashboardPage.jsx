import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  Send,
  MessageSquare,
  BarChart3,
  HelpCircle,
  FileText,
  RotateCcw,
  Check,
  ShieldCheck,
  Award
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import SectionHeading from '../components/common/SectionHeading';
import Card, { CardHeader } from '../components/common/Card';
import Badge from '../components/common/Badge';
import Button from '../components/common/Button';
import { useAnalysis } from '../context/AnalysisContext';
import { apiClient } from '../services/api';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { analysisResult, clearAnalysis } = useAnalysis();

  // Chat interface state
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: "Hello! I'm your MatchMyResume AI Assistant. I have evaluated your resume against your target job requirements. Feel free to ask me anything about your score, skill gaps, or how to strengthen your application."
    }
  ]);
  const [inputQuestion, setInputQuestion] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);

  if (!analysisResult) {
    return (
      <div className="max-w-md mx-auto text-center py-20">
        <AlertCircle className="w-12 h-12 text-[#8C291C] mx-auto mb-3" />
        <h3 className="text-xl font-bold text-forest-900">No Analysis Found</h3>
        <p className="text-xs text-sage-600 mt-2">Please upload a resume and job description to view results.</p>
        <Link to="/analyze" className="mt-6 inline-block">
          <Button variant="primary">Start Analysis</Button>
        </Link>
      </div>
    );
  }

  const { meta, similarity_metrics, skill_analysis, ai_insights } = analysisResult;
  const matchScore = similarity_metrics?.match_score_percentage || 0;
  const skillCoverage = skill_analysis?.skill_coverage_percentage || 0;

  // Visual Analytics data from ACTUAL results
  const chartData = [
    {
      name: 'Technical',
      Matched: skill_analysis?.matching_technical?.length || 0,
      Missing: skill_analysis?.missing_technical?.length || 0,
    },
    {
      name: 'Soft Skills',
      Matched: skill_analysis?.matching_soft?.length || 0,
      Missing: skill_analysis?.missing_soft?.length || 0,
    },
    {
      name: 'Total Skills',
      Matched: skill_analysis?.matching_skills?.length || 0,
      Missing: skill_analysis?.missing_skills?.length || 0,
    },
  ];

  const presetQuestions = [
    "Why is my match score at this level?",
    "Which key skills am I missing?",
    "How can I improve my resume for this role?",
    "What should I learn next?",
    "How can I improve my project descriptions?"
  ];

  const handleSendChat = async (questionText = inputQuestion) => {
    const textToSend = questionText.trim();
    if (!textToSend || isChatLoading) return;

    // Add user message
    const newMessages = [...messages, { sender: 'user', text: textToSend }];
    setMessages(newMessages);
    setInputQuestion('');
    setIsChatLoading(true);

    try {
      const summaryPayload = {
        match_score: matchScore,
        matching_skills: skill_analysis?.matching_skills || [],
        missing_skills: skill_analysis?.missing_skills || [],
        strengths: ai_insights?.strengths || [],
        weaknesses: ai_insights?.weaknesses || []
      };

      const res = await apiClient.post('/api/chat', {
        question: textToSend,
        resume_summary: summaryPayload,
        chat_history: newMessages.slice(-6)
      });

      setMessages((prev) => [
        ...prev,
        { sender: 'ai', text: res.data.answer }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: "I couldn't process this query right now. Please ensure your backend is running or try rephrasing your question."
        }
      ]);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="space-y-8 py-4 sm:py-6 max-w-6xl mx-auto">
      {/* Top Banner & Reset */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-forest-800/8 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-sage-600">Results Dashboard</span>
            <Badge variant="matched" dot>Analysis Completed</Badge>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-900 tracking-tight mt-0.5">
            Resume & Job Alignment Report
          </h1>
          <p className="text-xs text-sage-600 mt-1">
            File: <span className="font-semibold text-forest-900">{meta?.filename}</span> ({(meta?.filesize_bytes / 1024).toFixed(1)} KB)
          </p>
        </div>

        <button
          onClick={() => {
            clearAnalysis();
            navigate('/analyze');
          }}
          className="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-cream-50 hover:bg-cream-100 text-forest-800 border border-forest-800/10 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>New Analysis</span>
        </button>
      </div>

      {/* A. Overall Match Scores Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Metric 1: Text Similarity */}
        <Card variant="mint" className="p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-forest-900">Text Similarity Score</span>
              <Badge variant="forest" size="sm">{similarity_metrics?.interpretation}</Badge>
            </div>
            <div className="flex items-baseline gap-2 mt-3">
              <span className="text-4xl font-extrabold text-forest-900 tracking-tight">{matchScore}%</span>
              <span className="text-xs font-semibold text-forest-700">Similarity</span>
            </div>
          </div>
          <p className="text-[11px] text-forest-800/80 mt-3 pt-2 border-t border-forest-800/8 leading-relaxed">
            Derived from lexical and semantic word distribution. Not an official ATS score.
          </p>
        </Card>

        {/* Metric 2: Skill Coverage */}
        <Card variant="cream" className="p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-forest-900">Skill Coverage</span>
              <Badge variant="matched" size="sm">
                {skill_analysis?.total_matched_skills} / {skill_analysis?.total_required_skills} Required
              </Badge>
            </div>
            <div className="flex items-baseline gap-2 mt-3">
              <span className="text-4xl font-extrabold text-forest-900 tracking-tight">{skillCoverage}%</span>
              <span className="text-xs font-semibold text-forest-700">Coverage</span>
            </div>
          </div>
          <p className="text-[11px] text-sage-600 mt-3 pt-2 border-t border-forest-800/8 leading-relaxed">
            Percentage of identified job skills explicitly verified in your resume.
          </p>
        </Card>

        {/* Metric 3: Gaps Found */}
        <Card variant="default" className="p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-forest-900">Missing Skills</span>
              <Badge variant="missing" size="sm">Action Items</Badge>
            </div>
            <div className="flex items-baseline gap-2 mt-3">
              <span className="text-4xl font-extrabold text-[#8C291C] tracking-tight">
                {skill_analysis?.missing_skills?.length || 0}
              </span>
              <span className="text-xs font-semibold text-[#8C291C]">Gaps to Address</span>
            </div>
          </div>
          <p className="text-[11px] text-sage-600 mt-3 pt-2 border-t border-forest-800/8 leading-relaxed">
            Required keywords from the job description that do not appear in your resume.
          </p>
        </Card>
      </div>

      {/* B. Skills Analysis & D. Visual Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Skills Matrix (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {/* Matched Skills */}
          <Card variant="glass" className="p-5">
            <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-forest-700" />
                <h3 className="text-sm font-bold text-forest-900">
                  Matching Skills ({skill_analysis?.matching_skills?.length || 0})
                </h3>
              </div>
              <Badge variant="matched" size="sm">Found in Resume</Badge>
            </div>
            {skill_analysis?.matching_skills?.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {skill_analysis.matching_skills.map((s) => (
                  <Badge key={s} variant="matched" dot size="sm">
                    {s}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-xs text-sage-600">No direct skill matches detected in the text.</p>
            )}
          </Card>

          {/* Missing Skills */}
          <Card variant="glass" className="p-5">
            <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-3">
              <div className="flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-[#8C291C]" />
                <h3 className="text-sm font-bold text-[#8C291C]">
                  Missing Skills ({skill_analysis?.missing_skills?.length || 0})
                </h3>
              </div>
              <Badge variant="missing" size="sm">Add to Resume</Badge>
            </div>
            {skill_analysis?.missing_skills?.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {skill_analysis.missing_skills.map((s) => (
                  <Badge key={s} variant="missing" dot size="sm">
                    {s}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-xs text-forest-700">Excellent! No missing requirements detected.</p>
            )}
          </Card>

          {/* Additional Skills */}
          {skill_analysis?.additional_skills?.length > 0 && (
            <Card variant="cream" className="p-5">
              <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-3">
                <h3 className="text-sm font-bold text-forest-900">
                  Additional Profile Strengths ({skill_analysis.additional_skills.length})
                </h3>
                <Badge variant="sage" size="sm">Bonus Skills</Badge>
              </div>
              <div className="flex flex-wrap gap-2">
                {skill_analysis.additional_skills.slice(0, 12).map((s) => (
                  <Badge key={s} variant="sage" size="sm">
                    {s}
                  </Badge>
                ))}
              </div>
            </Card>
          )}
        </div>

        {/* Visual Analytics Recharts (5 cols) */}
        <div className="lg:col-span-5">
          <Card variant="glass" className="p-5 h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-4">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-forest-800" />
                  <h3 className="text-sm font-bold text-forest-900">Skill Breakdown Analytics</h3>
                </div>
                <span className="text-[10px] font-semibold text-sage-600">Actual Counts</span>
              </div>

              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#1B3E22' }} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#4D644A' }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#F7FAF4',
                        borderColor: '#1B3E22',
                        borderRadius: '0.75rem',
                        fontSize: '11px'
                      }}
                    />
                    <Bar dataKey="Matched" fill="#3D7A41" radius={[4, 4, 0, 0]} name="Matched" />
                    <Bar dataKey="Missing" fill="#922E21" radius={[4, 4, 0, 0]} name="Missing" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-forest-800/8 flex items-center justify-around text-xs">
              <span className="flex items-center gap-1.5 font-semibold text-forest-800">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#3D7A41]" /> Matched Skills
              </span>
              <span className="flex items-center gap-1.5 font-semibold text-[#8C291C]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#922E21]" /> Missing Skills
              </span>
            </div>
          </Card>
        </div>
      </div>

      {/* C. Resume Evaluation Summary */}
      <Card variant="glass" className="p-6">
        <CardHeader
          title="Resume Evaluation & Strengths"
          subtitle="Objective highlights directly grounded in your extracted content"
          action={<Badge variant="matched" dot>Verified</Badge>}
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
          <div className="space-y-2.5">
            <p className="font-bold text-forest-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-forest-700 shrink-0" />
              Verified Strengths:
            </p>
            <ul className="space-y-2 text-forest-800/85 pl-5 list-disc">
              {ai_insights?.strengths?.map((str, idx) => (
                <li key={idx} className="leading-relaxed">{str}</li>
              ))}
            </ul>
          </div>

          <div className="space-y-2.5">
            <p className="font-bold text-[#8C291C] flex items-center gap-1.5">
              <AlertCircle className="w-4 h-4 text-[#8C291C] shrink-0" />
              Identified Improvement Areas:
            </p>
            <ul className="space-y-2 text-forest-800/85 pl-5 list-disc">
              {ai_insights?.weaknesses?.map((wk, idx) => (
                <li key={idx} className="leading-relaxed">{wk}</li>
              ))}
            </ul>
          </div>
        </div>
      </Card>

      {/* E. Interactive AI Chat Interface */}
      <Card variant="glass" className="p-6">
        <div className="flex items-center justify-between pb-4 border-b border-forest-800/8 mb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-forest-800 text-cream-50 flex items-center justify-center shadow-pill">
              <MessageSquare className="w-4 h-4 text-cream-50" />
            </div>
            <div>
              <h3 className="font-bold text-forest-900 text-base">Interactive Resume Chat</h3>
              <p className="text-xs text-sage-600">Ask questions about your specific match score and recommendations</p>
            </div>
          </div>
          <Badge variant="mint" size="sm">Context-Aware AI</Badge>
        </div>

        {/* Preset Question Chips */}
        <div className="mb-4 flex flex-wrap gap-2">
          {presetQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSendChat(q)}
              disabled={isChatLoading}
              className="text-[11px] font-medium px-3 py-1.5 rounded-full bg-cream-50 hover:bg-botanical-100 text-forest-900 border border-forest-800/12 transition-colors disabled:opacity-50"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Chat Message Box */}
        <div className="h-64 overflow-y-auto space-y-3 p-4 rounded-2xl bg-cream-50/70 border border-forest-800/10 mb-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-forest-800 text-cream-50 rounded-tr-none'
                    : 'bg-cream-100 text-forest-900 border border-forest-800/10 rounded-tl-none shadow-sm'
                }`}
              >
                <p className="whitespace-pre-line">{msg.text}</p>
              </div>
            </div>
          ))}
          {isChatLoading && (
            <div className="flex justify-start">
              <div className="bg-cream-100 border border-forest-800/10 rounded-2xl rounded-tl-none p-3 text-xs text-sage-600 animate-pulse">
                Thinking and analyzing your resume context...
              </div>
            </div>
          )}
        </div>

        {/* Chat Input Field */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendChat();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputQuestion}
            onChange={(e) => setInputQuestion(e.target.value)}
            placeholder="Ask a question about your match or how to bridge skill gaps..."
            disabled={isChatLoading}
            className="flex-1 rounded-xl bg-cream-50/90 text-forest-900 text-xs sm:text-sm placeholder:text-sage-500 border border-forest-800/15 focus:border-forest-700 focus:ring-2 focus:ring-forest-700/20 outline-none px-4 py-2.5 transition-all"
          />
          <Button
            type="submit"
            variant="primary"
            size="md"
            disabled={!inputQuestion.trim() || isChatLoading}
            icon={<Send className="w-3.5 h-3.5" />}
          >
            Send
          </Button>
        </form>
      </Card>

      {/* F. Prominent AI Recommendations Button */}
      <div className="text-center pt-4 pb-6">
        <Link to="/insights">
          <Button
            variant="primary"
            size="lg"
            icon={<ArrowRight className="w-4 h-4" />}
            iconPosition="right"
            className="px-10 py-3.5 text-base shadow-soft hover:shadow-soft-md"
          >
            View AI Recommendations
          </Button>
        </Link>
        <p className="text-xs text-sage-600 mt-2">
          Proceed to detailed bullet point rewrites, skill roadmaps, and career development guidance.
        </p>
      </div>
    </div>
  );
}
