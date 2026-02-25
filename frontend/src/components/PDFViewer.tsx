import { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface PDFViewerProps {
  file: File;
}

function PDFViewer({ file }: PDFViewerProps) {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [loading, setLoading] = useState(true);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
    setLoading(false);
  };

  const goToPrevPage = () => {
    setPageNumber(prev => Math.max(prev - 1, 1));
  };

  const goToNextPage = () => {
    setPageNumber(prev => Math.min(prev + 1, numPages));
  };

  const zoomIn = () => {
    setScale(prev => Math.min(prev + 0.25, 2.5));
  };

  const zoomOut = () => {
    setScale(prev => Math.max(prev - 0.25, 0.5));
  };

  return (
    <div className="pdf-viewer">
      <div className="pdf-viewer-header">
        <span className="pdf-title">{file.name}</span>
        <div className="pdf-controls">
          <button 
            onClick={zoomOut} 
            disabled={scale <= 0.5}
            className="pdf-control-btn"
            aria-label="Zoom out"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
              <line x1="8" y1="11" x2="14" y2="11" />
            </svg>
          </button>
          <span className="pdf-zoom-level">{Math.round(scale * 100)}%</span>
          <button 
            onClick={zoomIn} 
            disabled={scale >= 2.5}
            className="pdf-control-btn"
            aria-label="Zoom in"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
              <line x1="11" y1="8" x2="11" y2="14" />
              <line x1="8" y1="11" x2="14" y2="11" />
            </svg>
          </button>
        </div>
      </div>

      <div className="pdf-viewer-content">
        {loading && (
          <div className="pdf-loading">
            <div className="spinner"></div>
            <span>Loading PDF...</span>
          </div>
        )}
        <Document
          file={file}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={null}
          className="pdf-document"
        >
          <Page 
            pageNumber={pageNumber} 
            scale={scale}
            className="pdf-page"
          />
        </Document>
      </div>

      {numPages > 1 && (
        <div className="pdf-viewer-footer">
          <button 
            onClick={goToPrevPage} 
            disabled={pageNumber <= 1}
            className="pdf-page-btn"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
            Previous
          </button>
          <span className="pdf-page-info">
            Page {pageNumber} of {numPages}
          </span>
          <button 
            onClick={goToNextPage} 
            disabled={pageNumber >= numPages}
            className="pdf-page-btn"
          >
            Next
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
}

export default PDFViewer;
