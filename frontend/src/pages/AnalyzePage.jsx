import React, { useState, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  X,
  ArrowRight,
  FileCheck2,
  Sparkles,
  Info
} from 'lucide-react';
import SectionHeading from '../components/common/SectionHeading';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Badge from '../components/common/Badge';
import LoadingIndicator from '../components/common/LoadingIndicator';
import { useAnalysis } from '../context/AnalysisContext';
import { apiClient } from '../services/api';

const SAMPLE_JOB_DESCRIPTIONS = {
  fullstack: `Role: Full-Stack Software Engineer
Requirements:
- 2+ years of experience with Python, FastAPI, and React.js
- Proficiency in PostgreSQL, Docker, Git, and REST APIs
- Familiarity with Tailwind CSS, CI/CD pipelines, and cloud services (AWS or Azure)
- Strong problem solving, collaboration, agile mindset, and communication skills.`,
  python: `Role: Senior Backend Python Developer
Requirements:
- Strong expertise in Python 3, asynchronous programming, and FastAPI or Django
- Hands-on experience with PostgreSQL, Redis, Docker, and Kubernetes
- Solid understanding of microservice architecture and RESTful API design
- Experience with unit testing, git, team leadership, and mentorship.`,
  frontend: `Role: Modern Frontend Engineer
Requirements:
- Strong proficiency in React.js, TypeScript, Next.js, and modern JavaScript (ES6+)
- Experience with Tailwind CSS, state management (Redux or Zustand), and REST APIs
- Familiarity with Git, UI/UX prototyping, cross-functional collaboration, and attention to detail.`
};

export default function AnalyzePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setAnalysisResult } = useAnalysis();

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [errorMsg, setErrorMsg] = useState(location.state?.message || '');
  const [isProcessing, setIsProcessing] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);

  const fileInputRef = useRef(null);

  const loadingMessages = [
    'Uploading resume securely...',
    'Extracting resume information...',
    'Identifying technical & professional skills...',
    'Comparing job requirements & computing match...',
    'Generating personalized recommendations...',
  ];

  const handleFileSelect = (file) => {
    setErrorMsg('');
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      setErrorMsg('Invalid file format. Please upload a PDF (.pdf) resume.');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setErrorMsg('File size exceeds the 5MB limit. Please upload a smaller PDF.');
      return;
    }

    setResumeFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const removeFile = () => {
    setResumeFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const loadSampleJD = (key) => {
    setJobDescription(SAMPLE_JOB_DESCRIPTIONS[key]);
    setErrorMsg('');
  };

  const isFormValid = resumeFile && jobDescription.trim().length >= 30;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isFormValid || isProcessing) return;

    setIsProcessing(true);
    setErrorMsg('');
    setLoadingStep(0);

    // Progress stepper simulation while network request processes
    const stepInterval = setInterval(() => {
      setLoadingStep((prev) => (prev < loadingMessages.length - 1 ? prev + 1 : prev));
    }, 1200);

    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription.trim());

    try {
      const response = await apiClient.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      clearInterval(stepInterval);
      setAnalysisResult(response.data);
      // Navigate to dashboard only after successful completion
      navigate('/dashboard');
    } catch (err) {
      clearInterval(stepInterval);
      setIsProcessing(false);
      const detail = err.response?.data?.detail || err.message || 'Analysis failed. Please check your backend connection.';
      setErrorMsg(detail);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 py-4 sm:py-6">
      <SectionHeading
        tag="STEP 1 & 2"
        title="Resume Analysis & Job Matching"
        description="Provide your resume in PDF format and target job description to discover your alignment score and missing skills."
      />

      {errorMsg && (
        <div className="p-4 rounded-2xl bg-[#FCE8E4] border border-[#F5C2BA] text-[#8C291C] text-xs sm:text-sm flex items-start gap-3 animate-in fade-in duration-200">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-bold">Notice</p>
            <p className="mt-0.5 leading-relaxed">{errorMsg}</p>
          </div>
          <button onClick={() => setErrorMsg('')} className="p-1 hover:opacity-75">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {isProcessing ? (
        <Card variant="glass" className="py-16 text-center">
          <LoadingIndicator
            size="lg"
            title={loadingMessages[loadingStep]}
            subtitle="Processing your resume against job requirements. This takes only a few seconds..."
          />
          <div className="max-w-md mx-auto mt-6 bg-botanical-200/80 rounded-full h-2 overflow-hidden border border-forest-800/10">
            <div
              className="bg-forest-800 h-full transition-all duration-700 ease-out rounded-full"
              style={{ width: `${((loadingStep + 1) / loadingMessages.length) * 100}%` }}
            />
          </div>
        </Card>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* A. Resume Upload Card */}
            <Card variant="glass" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-4">
                  <div>
                    <h3 className="font-bold text-forest-900 text-base">1. Upload Resume</h3>
                    <p className="text-xs text-sage-600 mt-0.5">PDF format up to 5MB</p>
                  </div>
                  <Badge variant={resumeFile ? 'matched' : 'sage'} size="sm" dot={Boolean(resumeFile)}>
                    {resumeFile ? 'Ready' : 'PDF Only'}
                  </Badge>
                </div>

                {!resumeFile ? (
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`
                      border-2 border-dashed rounded-2xl p-8 text-center flex flex-col items-center justify-center cursor-pointer transition-all duration-200
                      ${isDragging
                        ? 'border-forest-800 bg-mint-100/80 scale-[1.01]'
                        : 'border-forest-800/20 bg-cream-50/60 hover:bg-cream-50/90 hover:border-forest-800/35'}
                    `}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf,application/pdf"
                      onChange={(e) => handleFileSelect(e.target.files?.[0])}
                      className="hidden"
                    />
                    <div className="w-12 h-12 rounded-2xl bg-botanical-200/80 border border-forest-800/12 flex items-center justify-center shadow-pill mb-3">
                      <UploadCloud className="w-6 h-6 text-forest-800" />
                    </div>
                    <p className="text-sm font-bold text-forest-900">Drag & drop your resume PDF</p>
                    <p className="text-xs text-sage-600 mt-1">or click to browse from device</p>
                    <span className="text-[10px] font-semibold text-sage-600 bg-cream-100 px-2.5 py-1 rounded-full border border-forest-800/8 mt-3">
                      Standard text-selectable PDF
                    </span>
                  </div>
                ) : (
                  <div className="p-5 rounded-2xl bg-[#D6ECD4]/60 border border-[#B2DCB0] flex items-center justify-between">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <div className="w-10 h-10 rounded-xl bg-forest-800 text-cream-50 flex items-center justify-center shrink-0 shadow-pill">
                        <FileCheck2 className="w-5 h-5 text-cream-50" />
                      </div>
                      <div className="truncate">
                        <p className="text-xs sm:text-sm font-bold text-forest-900 truncate">
                          {resumeFile.name}
                        </p>
                        <p className="text-[11px] text-forest-700 font-medium">
                          {(resumeFile.size / 1024).toFixed(1)} KB • Ready for extraction
                        </p>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={removeFile}
                      className="p-1.5 rounded-full hover:bg-forest-800/10 text-forest-900 transition-colors"
                      title="Remove file"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-forest-800/8 mt-4 flex items-center gap-1.5 text-[11px] text-sage-600">
                <Info className="w-3.5 h-3.5 text-forest-700 shrink-0" />
                <span>Files are processed in-memory and never stored permanently.</span>
              </div>
            </Card>

            {/* B. Job Description Card */}
            <Card variant="glass" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-forest-800/8 mb-3">
                  <div>
                    <h3 className="font-bold text-forest-900 text-base">2. Job Description</h3>
                    <p className="text-xs text-sage-600 mt-0.5">Paste target qualifications</p>
                  </div>
                  <span className="text-[11px] font-mono text-sage-600">
                    {jobDescription.length} chars
                  </span>
                </div>

                {/* Quick Sample JD Buttons */}
                <div className="mb-2.5 flex items-center gap-1.5 flex-wrap">
                  <span className="text-[11px] font-semibold text-sage-700">Quick load sample:</span>
                  <button
                    type="button"
                    onClick={() => loadSampleJD('fullstack')}
                    className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-cream-50 hover:bg-botanical-100 text-forest-900 border border-forest-800/10 transition-colors"
                  >
                    Full-Stack
                  </button>
                  <button
                    type="button"
                    onClick={() => loadSampleJD('python')}
                    className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-cream-50 hover:bg-botanical-100 text-forest-900 border border-forest-800/10 transition-colors"
                  >
                    Python Backend
                  </button>
                  <button
                    type="button"
                    onClick={() => loadSampleJD('frontend')}
                    className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-cream-50 hover:bg-botanical-100 text-forest-900 border border-forest-800/10 transition-colors"
                  >
                    Frontend
                  </button>
                </div>

                <textarea
                  rows={7}
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the complete job description, technical requirements, responsibilities, and qualifications here..."
                  className="w-full rounded-xl bg-cream-50/90 text-forest-900 text-xs sm:text-sm placeholder:text-sage-500 border border-forest-800/15 focus:border-forest-700 focus:ring-2 focus:ring-forest-700/20 outline-none p-3.5 leading-relaxed resize-none transition-all"
                />
              </div>

              <div className="pt-2 flex items-center justify-between text-[11px] text-sage-600">
                <span>Minimum 30 characters required</span>
                {jobDescription.length >= 30 && (
                  <span className="text-forest-800 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-forest-700" />
                    Valid input
                  </span>
                )}
              </div>
            </Card>
          </div>

          {/* Primary Action Button */}
          <div className="flex flex-col items-center justify-center pt-2">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              disabled={!isFormValid || isProcessing}
              icon={<ArrowRight className="w-4 h-4" />}
              iconPosition="right"
              className="w-full sm:w-80 shadow-soft hover:shadow-soft-md text-base py-3.5"
            >
              Analyze Resume Match
            </Button>
            {!isFormValid && (
              <p className="text-xs text-sage-600 mt-2 text-center">
                {!resumeFile ? 'Please select a PDF resume' : 'Please provide at least 30 characters for the job description'}
              </p>
            )}
          </div>
        </form>
      )}
    </div>
  );
}
