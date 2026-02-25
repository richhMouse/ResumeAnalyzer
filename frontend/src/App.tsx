import { useState, useEffect, useRef, useCallback } from 'react';
import { ALLOWED_ROLES } from './types/ats';
import { analyzeResume, uploadResume, ApiError } from './services/api';
import type { ATSResponse, Role } from './types/ats';
import ScoreCard from './components/ScoreCard';
import ResultsPanel from './components/ResultsPanel';
import PDFViewer from './components/PDFViewer';
import ImageViewer from './components/ImageViewer';
import { SAMPLE_RESUMES } from './data/sampleResumes';
import './App.css';

function App() {
  const [resumeText, setResumeText] = useState('');
  const [selectedRole, setSelectedRole] = useState<Role>('Product Manager');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<ATSResponse | null>(null);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    const saved = localStorage.getItem('ats-theme');
    return (saved as 'dark' | 'light') || 'dark';
  });
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [showPDFPreview, setShowPDFPreview] = useState(false);
  const [showImagePreview, setShowImagePreview] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const [showSkeleton, setShowSkeleton] = useState(false);
  const skeletonTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('ats-theme', theme);
  }, [theme]);

  useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 400);
    };
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
    };
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  }, []);

  const handleFile = (file: File) => {
    const validTypes = [
      'application/pdf', 
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/png',
      'image/jpeg',
      'image/jpg',
      'image/webp'
    ];
    const validExtensions = ['.pdf', '.docx', '.png', '.jpg', '.jpeg', '.webp'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      setError('Invalid file type. Please upload a PDF, DOCX, PNG, JPG, or WebP file.');
      return;
    }
    
    setSelectedFile(file);
    setShowPDFPreview(false);
    setError('');
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;
    
    setIsLoading(true);
    setError('');
    setResults(null);
    setUploadProgress(0);
    
    // Clear any existing timeout
    if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
    
    // Delay skeleton show slightly to prevent flash
    skeletonTimeoutRef.current = setTimeout(() => setShowSkeleton(true), 100);
    
    try {
      const response = await uploadResume(selectedFile, selectedRole, (progress) => {
        setUploadProgress(progress);
      });
      setResults(response);
      setShowResults(true);
      if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
      setShowSkeleton(false);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
      setShowSkeleton(false);
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setShowPDFPreview(false);
    setShowImagePreview(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const togglePDFPreview = () => {
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setShowPDFPreview(!showPDFPreview);
    }
  };

  const toggleImagePreview = () => {
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setShowImagePreview(!showImagePreview);
    }
  };

  const isImageFile = selectedFile && selectedFile.type.startsWith('image/');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setResults(null);
    
    if (!resumeText.trim()) {
      setError('Please enter your resume text');
      return;
    }

    setIsLoading(true);
    
    // Clear any existing timeout
    if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
    
    // Delay skeleton show slightly
    skeletonTimeoutRef.current = setTimeout(() => setShowSkeleton(true), 100);
    try {
      const response = await analyzeResume({
        resume_text: resumeText,
        target_role: selectedRole,
      });
      setResults(response);
      setShowResults(true);
      if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
      setShowSkeleton(false);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      if (skeletonTimeoutRef.current) clearTimeout(skeletonTimeoutRef.current);
      setShowSkeleton(false);
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score: number): string => {
    if (score >= 70) return '#22c55e';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <polyline points="10 9 9 9 8 9" />
            </svg>
            <h1>ATS Resume Analyzer</h1>
          </div>
          <p className="subtitle">Management & Tech Roles • AI-Powered • ATS Simulation</p>
        </div>
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === 'dark' ? (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" />
              <line x1="12" y1="21" x2="12" y2="23" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
              <line x1="1" y1="12" x2="3" y2="12" />
              <line x1="21" y1="12" x2="23" y2="12" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          )}
        </button>
      </header>

      <main className="main">
        <form onSubmit={handleSubmit} className="analyzer-form">
          <div className="file-upload-section">
            <div 
              className={`drop-zone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.png,.jpg,.jpeg,.webp"
                onChange={handleFileSelect}
                hidden
              />
              {selectedFile ? (
                <div className="file-selected">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                  </svg>
                  <span className="file-name">{selectedFile.name}</span>
                  {(selectedFile.type === 'application/pdf' || isImageFile) && (
                    <button 
                      type="button" 
                      className="preview-file"
                      onClick={(e) => { 
                        e.stopPropagation(); 
                        selectedFile.type === 'application/pdf' ? togglePDFPreview() : toggleImagePreview(); 
                      }}
                      aria-label={isImageFile ? "Preview Image" : "Preview PDF"}
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                        <circle cx="12" cy="12" r="3" />
                      </svg>
                      {(isImageFile ? showImagePreview : showPDFPreview) ? 'Hide' : 'Preview'}
                    </button>
                  )}
                  <button 
                    type="button" 
                    className="clear-file"
                    onClick={(e) => { e.stopPropagation(); clearFile(); }}
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18" />
                      <line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </div>
              ) : (
                <>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" y1="3" x2="12" y2="15" />
                  </svg>
                  <p>Drag & drop your resume here</p>
                  <span>or click to browse (PDF, DOCX, PNG, JPG, WebP)</span>
                </>
              )}
            </div>
            {selectedFile && (
              <>
                {isLoading && (
                  <div className="progress-container">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                    <span className="progress-text">
                      {uploadProgress < 100 ? `Uploading... ${uploadProgress}%` : 'Analyzing...'}
                    </span>
                  </div>
                )}
                <button 
                  type="button" 
                  className="upload-btn"
                  onClick={handleFileUpload}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <span className="loading">
                      <span className="spinner"></span>
                      Analyzing...
                    </span>
                  ) : (
                    <>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <line x1="21" y1="21" x2="16.65" y2="16.65" />
                      </svg>
                      Analyze {selectedFile.name}
                    </>
                  )}
                </button>
              </>
            )}
          </div>

          {(showPDFPreview || showImagePreview) && selectedFile && (
            <div className="pdf-preview-section">
              {showPDFPreview && <PDFViewer file={selectedFile} />}
              {showImagePreview && <ImageViewer file={selectedFile} />}
            </div>
          )}

          <div className="divider">
            <span>or paste text</span>
          </div>

          <div className="form-group">
            <label htmlFor="role-select">Target Role</label>
            <select
              id="role-select"
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value as Role)}
              className="role-select"
            >
              {ALLOWED_ROLES.map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <div className="resume-label-row">
              <label htmlFor="resume-text">Resume Text</label>
              <button 
                type="button" 
                className="sample-btn"
                onClick={() => setResumeText(SAMPLE_RESUMES[selectedRole])}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
                Load Sample {selectedRole} Resume
              </button>
            </div>
            <textarea
              id="resume-text"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume text here... (Plain text only, no formatting)"
              className="resume-input"
              rows={12}
            />
            <span className="char-count">{resumeText.length} characters</span>
          </div>

          <button 
            type="submit" 
            className="submit-btn"
            disabled={isLoading || !resumeText.trim()}
          >
            {isLoading ? (
              <span className="loading">
                <span className="spinner"></span>
                Analyzing...
              </span>
            ) : (
              <>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                Analyze Resume
              </>
            )}
          </button>

          {error && (
            <div className="error-message">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}
        </form>

        {(showSkeleton || (results && showResults)) && (
          <div className="results-container" ref={resultsRef}>
            <div className="score-overview">                {showSkeleton ? (
                <div className="skeleton-main-score"></div>
              ) : results ? (
              <div className="main-score" style={{ '--score-color': getScoreColor(results.ats_score) } as React.CSSProperties}>
                <div className="score-circle">
                  <svg viewBox="0 0 36 36" className="score-ring">
                    <path
                      className="score-ring-bg"
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="score-ring-fill"
                      strokeDasharray={`${results.ats_score}, 100`}
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="score-value">
                    <span className="score-number">{results!.ats_score}</span>
                    <span className="score-label">/ 100</span>
                  </div>
                </div>
                <div className="shortlist-badge" data-probability={results.shortlist_probability}>
                  {results.shortlist_probability} Shortlist Probability
                </div>
              </div>
              ) : null}

              <div className="score-cards">
                {showSkeleton ? (
                  [...Array(5)].map((_, i) => (
                    <div key={i} className="skeleton-card-inline">
                      <div className="skeleton-bar"></div>
                    </div>
                  ))
                ) : results ? (
                  <>
                <ScoreCard 
                  title="Role Relevance" 
                  score={results.role_relevance_score} 
                  max={30}
                  color="#8b5cf6"
                  delay={0}
                />
                <ScoreCard 
                  title="Leadership & Ownership" 
                  score={results.leadership_score} 
                  max={25}
                  color="#3b82f6"
                  delay={1}
                />
                <ScoreCard 
                  title="Impact & Metrics" 
                  score={results.impact_metrics_score} 
                  max={20}
                  color="#10b981"
                  delay={2}
                />
                <ScoreCard 
                  title="Resume Structure" 
                  score={results.resume_structure_score} 
                  max={15}
                  color="#f59e0b"
                  delay={3}
                />
                <ScoreCard 
                  title="Language Quality" 
                  score={results.language_quality_score} 
                  max={10}
                  color="#ec4899"
                  delay={4}
                />
                  </>
                ) : null}
              </div>
            </div>

            {showSkeleton ? (
              <div className="skeleton-results">
                <div className="skeleton-score-cards">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="skeleton-card">
                      <div className="skeleton-bar"></div>
                    </div>
                  ))}
                </div>
                <div className="skeleton-panels">
                  <div className="skeleton-panel"></div>
                  <div className="skeleton-panel"></div>
                  <div className="skeleton-panel"></div>
                </div>
              </div>
            ) : results ? (
              <>
                <ResultsPanel 
                  strengths={results.factual_strengths || []}
                  weaknesses={results.factual_weaknesses || []}
                  suggestions={results.improvement_suggestions || []}
                />
              </>
            ) : null}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>ATS Resume Analyzer • Management & Tech Roles Edition</p>
      </footer>

      {showBackToTop && (
        <button className="back-to-top" onClick={scrollToTop} aria-label="Back to top">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="18 15 12 9 6 15" />
          </svg>
        </button>
      )}
    </div>
  );
}

export default App;
