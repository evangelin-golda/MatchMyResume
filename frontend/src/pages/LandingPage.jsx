import React from 'react';
import HeroSection from '../components/landing/HeroSection';
import HowItWorks from '../components/landing/HowItWorks';
import KeyFeatures from '../components/landing/KeyFeatures';
import WhyMatchMyResume from '../components/landing/WhyMatchMyResume';
import FinalCta from '../components/landing/FinalCta';

export default function LandingPage() {
  return (
    <div className="space-y-10 sm:space-y-16">
      {/* 1. Hero Section */}
      <HeroSection />

      {/* 2. Four-Step Workflow */}
      <HowItWorks />

      {/* 3. Six Key Feature Cards */}
      <KeyFeatures />

      {/* 4. Value Proposition & Transparency */}
      <WhyMatchMyResume />

      {/* 5. Final Call to Action */}
      <FinalCta />
    </div>
  );
}
