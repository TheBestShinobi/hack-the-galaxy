import React from 'react'
import { motion } from 'framer-motion'

// Kawaii 5-pointed star with rounded edges
const StarWithFace = ({ size, color, isHighEco, className }) => {
  // Different gradient for high eco score (light blue "higher flame")
  const gradientId = isHighEco ? "starGradBlue" : "starGradPink"
  
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" className={className}>
      <defs>
        {/* Pink/Lavender gradient - default */}
        <radialGradient id="starGradPink" cx="35%" cy="35%" r="70%">
          <stop offset="0%" stopColor="#FF85C1" />
          <stop offset="40%" stopColor="#7B61FF" />
          <stop offset="100%" stopColor="#5222A5" />
        </radialGradient>
        
        {/* Light blue gradient - high eco score ("higher flame") */}
        <radialGradient id="starGradBlue" cx="35%" cy="35%" r="70%">
          <stop offset="0%" stopColor="#60A5FA" />
          <stop offset="40%" stopColor="#3B82F6" />
          <stop offset="100%" stopColor="#1D4ED8" />
        </radialGradient>
        
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <filter id="innerShadow">
          <feOffset dx="0" dy="2"/>
          <feGaussianBlur stdDeviation="3" result="offset-blur"/>
          <feComposite operator="out" in="SourceGraphic" in2="offset-blur" result="inverse"/>
          <feFlood floodColor="black" floodOpacity="0.3" result="color"/>
          <feComposite operator="in" in="color" in2="inverse" result="shadow"/>
          <feComposite operator="over" in="shadow" in2="SourceGraphic"/>
        </filter>
      </defs>
      
      {/* Star shape with rounded points - fully filled */}
      <path
        fill={`url(#${gradientId})`}
        filter="url(#glow)"
        stroke={isHighEco ? "#60A5FA" : "#FF85C1"}
        strokeWidth="0.5"
        d="M50 5 
           L61 35 
           L93 35 
           L68 55 
           L78 85 
           L50 68 
           L22 85 
           L32 55 
           L7 35 
           L39 35 
           Z"
      />
      
      {/* Inner fill to remove any dark spots */}
      <path
        fill={`url(#${gradientId})`}
        opacity="0.8"
        transform="translate(1, 1)"
        d="M50 8 
           L59 33 
           L88 33 
           L66 50 
           L75 78 
           L50 63 
           L25 78 
           L34 50 
           L12 33 
           L41 33 
           Z"
      />
    </svg>
  )
}

const AvaSTAR = ({ ecoScore, carbonMass, isHighEcoScore, isHighCarbonMass }) => {
  const getStarColor = () => {
    if (isHighCarbonMass) return '#4B5563'
    if (isHighEcoScore) return '#60A5FA' // Light blue for high eco
    return '#7B61FF'
  }

  const getAuraColor = () => {
    if (isHighCarbonMass) return 'rgba(75, 85, 99, 0.3)'
    if (isHighEcoScore) return 'rgba(96, 165, 250, 0.4)' // Blue aura
    return 'rgba(123, 97, 255, 0.3)'
  }

  const getGlowIntensity = () => {
    if (isHighCarbonMass) return 20
    if (isHighEcoScore) return 80 // Brighter glow for high eco
    return 50
  }

  const starColor = getStarColor()
  const glowIntensity = getGlowIntensity()

  return (
    <div className="relative w-72 h-72 flex items-center justify-center">
      {/* Outer Aura - blue for high eco ("higher flame") */}
      {isHighEcoScore && !isHighCarbonMass && (
        <>
          <motion.div
            animate={{ scale: [1, 1.4, 1], opacity: [0.2, 0.5, 0.2] }}
            transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
            className="absolute w-64 h-64 rounded-full"
            style={{
              background: `radial-gradient(circle, ${getAuraColor()} 0%, transparent 70%)`,
              filter: 'blur(20px)',
            }}
          />
        </>
      )}

      {/* Space Debris */}
      {isHighCarbonMass && (
        <div className="absolute inset-0">
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              animate={{ rotate: 360 }}
              transition={{ duration: 8 + i * 2, repeat: Infinity, ease: "linear" }}
              className="absolute"
              style={{
                top: '50%', left: '50%',
                transform: `rotate(${i * 60}deg) translateY(-100px)`,
              }}
            >
              <div className="w-8 h-8 bg-cosmic-debris rounded-full" />
            </motion.div>
          ))}
        </div>
      )}

      {/* Main Kawaii Star */}
      <motion.div
        animate={{ scale: [1, 1.05, 1], rotate: [0, 3, -3, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        className="relative"
        style={{
          filter: `drop-shadow(0 0 ${glowIntensity}px ${starColor})`,
        }}
      >
        <StarWithFace 
          size={150} 
          color={starColor} 
          isHighEco={isHighEcoScore}
        />
        
        {/* Kawaii face - cute simple style */}
        {/* Eyes - simple dots */}
        <div className="absolute top-[38%] left-[30%] w-4 h-5 bg-white rounded-full" />
        <div className="absolute top-[38%] right-[30%] w-4 h-5 bg-white rounded-full" />
        
        {/* Tiny eye shine */}
        <div className="absolute top-[40%] left-[32%] w-1.5 h-1.5 bg-white rounded-full opacity-80" />
        <div className="absolute top-[40%] right-[32%] w-1.5 h-1.5 bg-white rounded-full opacity-80" />
        
        {/* Blush - soft pink/blue ovals */}
        <div 
          className="absolute top-[52%] left-[20%] w-8 h-5 rounded-full opacity-40" 
          style={{ background: isHighEcoScore ? '#60A5FA' : '#FF85C1' }}
        />
        <div 
          className="absolute top-[52%] right-[20%] w-8 h-5 rounded-full opacity-40" 
          style={{ background: isHighEcoScore ? '#60A5FA' : '#FF85C1' }}
        />
        
        {/* Mouth - tiny curve */}
        <div className="absolute top-[60%] left-1/2 -translate-x-1/2 w-5 h-2 border-b-2 border-white rounded-full opacity-70" />
      </motion.div>

      {/* Orbiting sparkles - blue for high eco */}
      {!isHighCarbonMass && (
        <>
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              animate={{ rotate: 360 }}
              transition={{ duration: 6 + i, repeat: Infinity, ease: "linear" }}
              className="absolute"
              style={{
                top: '50%', left: '50%',
                transform: `rotate(${i * 45}deg) translateY(-90px)`,
              }}
            >
              <motion.div
                animate={{ scale: [0.6, 1, 0.6], opacity: [0.4, 0.9, 0.4] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="w-2 h-2 rounded-full"
                style={{
                  background: isHighEcoScore ? '#60A5FA' : (i % 2 === 0 ? '#FF85C1' : '#7B61FF'),
                  boxShadow: `0 0 6px ${isHighEcoScore ? '#60A5FA' : (i % 2 === 0 ? '#FF85C1' : '#7B61FF')}`,
                }}
              />
            </motion.div>
          ))}
        </>
      )}

      {/* Status */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="absolute -bottom-10"
      >
        <span 
          className="text-sm font-mono px-4 py-1.5 rounded-full"
          style={{ 
            color: starColor,
            background: `${starColor}20`,
            border: `1px solid ${starColor}40`
          }}
        >
          {isHighCarbonMass ? 'Space Debris Mode' : isHighEcoScore ? 'Supernova!' : 'Cosmic Cruising'}
        </span>
      </motion.div>
    </div>
  )
}

export default AvaSTAR
