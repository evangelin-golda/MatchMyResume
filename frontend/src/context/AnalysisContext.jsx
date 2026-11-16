import React, { createContext, useContext, useState, useEffect } from 'react';

const AnalysisContext = createContext(null);

const STORAGE_KEY = 'matchmyresume_session_analysis';

export function AnalysisProvider({ children }) {
  const [analysisResult, setAnalysisResultState] = useState(() => {
    try {
      const saved = sessionStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const setAnalysisResult = (data) => {
    setAnalysisResultState(data);
    if (data) {
      try {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch (err) {
        console.error('Failed to save to sessionStorage', err);
      }
    } else {
      sessionStorage.removeItem(STORAGE_KEY);
    }
  };

  const clearAnalysis = () => {
    setAnalysisResult(null);
  };

  const hasAnalysis = Boolean(analysisResult && analysisResult.similarity_metrics);

  return (
    <AnalysisContext.Provider
      value={{
        analysisResult,
        setAnalysisResult,
        clearAnalysis,
        hasAnalysis,
        isAnalyzing,
        setIsAnalyzing,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
}
