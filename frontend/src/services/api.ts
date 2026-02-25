import type { ATSRequest, ATSResponse } from '../types/ats';

// Use relative path for dev with proxy, or full URL for production/Docker
const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api` 
  : '/api';
const REQUEST_TIMEOUT = 30000; // 30 seconds

export const uploadResume = async (
  file: File, 
  targetRole: string,
  onProgress?: (progress: number) => void
): Promise<ATSResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_role', targetRole);

  let response: Response;

  // Simulate progress for upload phase (XHR provides real progress but fetch doesn't)
  if (onProgress) {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      if (progress < 90) {
        onProgress(progress);
      }
      clearInterval(interval);
    }, 100);
  }

  try {
    response = await fetchWithTimeout(
      `${API_BASE}/upload`,
      {
        method: 'POST',
        body: formData,
      },
      REQUEST_TIMEOUT
    );
    
    if (onProgress) {
      onProgress(100);
    }
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new ApiError('Request timed out. Please try again.', undefined, true);
      }
      throw new ApiError(
        'Unable to connect to server. Please check your connection.',
        undefined,
        true
      );
    }
    throw new ApiError('An unexpected error occurred', undefined, true);
  }

  if (!response.ok) {
    let errorMessage = 'Failed to upload and analyze resume';
    
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      if (response.status === 500) {
        errorMessage = 'Server error. Please try again later.';
      } else if (response.status === 429) {
        errorMessage = 'Too many requests. Please wait and try again.';
      }
    }
    
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
};

export class ApiError extends Error {
  statusCode?: number;
  isNetworkError: boolean;
  
  constructor(
    message: string,
    statusCode?: number,
    isNetworkError: boolean = false
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.isNetworkError = isNetworkError;
  }
}

const fetchWithTimeout = async (
  url: string,
  options: RequestInit,
  timeout: number
): Promise<Response> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
};

export const analyzeResume = async (request: ATSRequest): Promise<ATSResponse> => {
  let response: Response;

  try {
    response = await fetchWithTimeout(
      `${API_BASE}/analyze`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      },
      REQUEST_TIMEOUT
    );
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new ApiError('Request timed out. Please try again.', undefined, true);
      }
      // Network error (no internet, server down, etc.)
      throw new ApiError(
        'Unable to connect to server. Please check your connection.',
        undefined,
        true
      );
    }
    throw new ApiError('An unexpected error occurred', undefined, true);
  }

  if (!response.ok) {
    let errorMessage = 'Failed to analyze resume';
    
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // Response might not be JSON
      if (response.status === 500) {
        errorMessage = 'Server error. Please try again later.';
      } else if (response.status === 429) {
        errorMessage = 'Too many requests. Please wait and try again.';
      }
    }
    
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
};
