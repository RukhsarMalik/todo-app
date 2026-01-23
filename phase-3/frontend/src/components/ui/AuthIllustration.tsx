'use client';

/**
 * SVG Illustration component for auth pages.
 * Shows a person working with task boards.
 */

import React from 'react';

interface AuthIllustrationProps {
  type?: 'login' | 'signup';
}

export function AuthIllustration({ type = 'login' }: AuthIllustrationProps) {
  return (
    <div className="relative w-full h-full flex items-center justify-center p-8">
      <svg
        viewBox="0 0 500 400"
        className="w-full max-w-md h-auto"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background Elements */}
        <circle cx="250" cy="200" r="150" fill="#EBF4FF" opacity="0.5" />
        <circle cx="380" cy="100" r="30" fill="#DBEAFE" opacity="0.6" />
        <circle cx="100" cy="320" r="20" fill="#FEE2E2" opacity="0.6" />

        {/* Task Board - Main */}
        <rect x="180" y="80" width="140" height="180" rx="8" fill="#60A5FA" />
        <rect x="190" y="95" width="120" height="12" rx="2" fill="#BFDBFE" />
        <rect x="190" y="115" width="100" height="8" rx="2" fill="#DBEAFE" />
        <rect x="190" y="135" width="80" height="8" rx="2" fill="#DBEAFE" />
        <rect x="190" y="160" width="120" height="12" rx="2" fill="#BFDBFE" />
        <rect x="190" y="180" width="90" height="8" rx="2" fill="#DBEAFE" />
        <rect x="190" y="205" width="120" height="12" rx="2" fill="#BFDBFE" />
        <rect x="190" y="225" width="70" height="8" rx="2" fill="#DBEAFE" />

        {/* Task Board - Secondary */}
        <rect x="280" y="140" width="100" height="130" rx="8" fill="#34D399" />
        <rect x="290" y="155" width="80" height="10" rx="2" fill="#A7F3D0" />
        <rect x="290" y="175" width="60" height="6" rx="2" fill="#D1FAE5" />
        <rect x="290" y="195" width="80" height="10" rx="2" fill="#A7F3D0" />
        <rect x="290" y="215" width="50" height="6" rx="2" fill="#D1FAE5" />

        {/* Checkmark on secondary board */}
        <circle cx="350" cy="250" r="12" fill="#10B981" />
        <path d="M345 250L348 253L355 246" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />

        {/* Person */}
        {/* Head */}
        <circle cx="120" cy="180" r="35" fill="#C4B5FD" />
        <circle cx="120" cy="175" r="30" fill="#8B5CF6" />

        {/* Hair */}
        <path d="M90 165C90 145 105 130 130 135C155 140 160 160 155 175C140 165 100 160 90 165Z" fill="#4C1D95" />

        {/* Face features */}
        <circle cx="110" cy="175" r="3" fill="#1E1B4B" />
        <circle cx="130" cy="175" r="3" fill="#1E1B4B" />
        <path d="M115 188C118 192 125 192 128 188" stroke="#1E1B4B" strokeWidth="2" strokeLinecap="round" />

        {/* Body */}
        <path d="M80 220C80 210 100 200 120 200C140 200 160 210 160 220L165 320H75L80 220Z" fill="#8B5CF6" />

        {/* Arm pointing */}
        <path d="M160 230C170 225 180 220 195 218" stroke="#C4B5FD" strokeWidth="12" strokeLinecap="round" />
        <circle cx="195" cy="218" r="8" fill="#C4B5FD" />

        {/* Legs */}
        <rect x="90" y="310" width="20" height="60" rx="4" fill="#4C1D95" />
        <rect x="130" y="310" width="20" height="60" rx="4" fill="#4C1D95" />

        {/* Decorative elements */}
        <circle cx="400" cy="200" r="8" fill="#F87171" opacity="0.6" />
        <circle cx="60" cy="120" r="6" fill="#60A5FA" opacity="0.6" />
        <circle cx="420" cy="300" r="10" fill="#34D399" opacity="0.5" />

        {/* Floating task items */}
        <rect x="350" y="60" width="60" height="40" rx="4" fill="#FEF3C7" />
        <rect x="358" y="72" width="44" height="4" rx="1" fill="#FCD34D" />
        <rect x="358" y="82" width="30" height="4" rx="1" fill="#FDE68A" />

        {type === 'signup' && (
          <>
            {/* Extra elements for signup */}
            <rect x="70" y="60" width="50" height="35" rx="4" fill="#DBEAFE" />
            <rect x="78" y="72" width="34" height="4" rx="1" fill="#93C5FD" />
            <rect x="78" y="80" width="24" height="4" rx="1" fill="#BFDBFE" />
          </>
        )}
      </svg>
    </div>
  );
}
