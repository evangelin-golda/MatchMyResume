import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAnalysis } from '../../context/AnalysisContext';

export default function ProtectedRoute({ children }) {
  const { hasAnalysis } = useAnalysis();
  const location = useLocation();

  if (!hasAnalysis) {
    // Redirect unauthorized direct access to /analyze
    return <Navigate to="/analyze" state={{ from: location.pathname, message: 'Please upload and analyze a resume first.' }} replace />;
  }

  return children;
}
