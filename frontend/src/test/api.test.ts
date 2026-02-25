import { describe, it, expect, vi, beforeEach } from 'vitest'
import { analyzeResume, uploadResume } from '../services/api'
import type { ATSResponse } from '../types/ats'

// Mock global fetch
const mockFetch = vi.fn();
Object.defineProperty(globalThis, 'fetch', {
  value: mockFetch,
  writable: true,
});

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('analyzeResume', () => {
    it('calls API with correct payload', async () => {
      const mockResponse: ATSResponse = {
        ats_score: 75,
        shortlist_probability: 'High',
        role_relevance_score: 25,
        leadership_score: 20,
        impact_metrics_score: 15,
        resume_structure_score: 10,
        language_quality_score: 5,
        factual_strengths: ['Good experience'],
        factual_weaknesses: ['Needs more metrics'],
        improvement_suggestions: ['Add numbers']
      }

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      const result = await analyzeResume({
        resume_text: 'Test resume',
        target_role: 'Product Manager'
      })

      expect(fetch).toHaveBeenCalledWith('/api/analyze', expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: 'Test resume',
          target_role: 'Product Manager'
        })
      }))
      expect(result).toEqual(mockResponse)
    })

    it('throws ApiError on non-ok response', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid role' })
      } as Response)

      await expect(analyzeResume({
        resume_text: 'test',
        target_role: 'Invalid Role'
      })).rejects.toThrow()
    })

    it('throws ApiError on network failure', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'))

      await expect(analyzeResume({
        resume_text: 'test',
        target_role: 'Product Manager'
      })).rejects.toThrow()
    })
  })

  describe('uploadResume', () => {
    it('uploads file and returns ATS response', async () => {
      const mockResponse: ATSResponse = {
        ats_score: 80,
        shortlist_probability: 'High',
        role_relevance_score: 28,
        leadership_score: 22,
        impact_metrics_score: 15,
        resume_structure_score: 10,
        language_quality_score: 5,
        factual_strengths: ['Excellent'],
        factual_weaknesses: [],
        improvement_suggestions: []
      }

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      const mockFile = new File(['test content'], 'resume.pdf', { type: 'application/pdf' })
      const onProgress = vi.fn()

      const result = await uploadResume(mockFile, 'Product Manager', onProgress)

      expect(fetch).toHaveBeenCalledWith('/api/upload', expect.objectContaining({
        method: 'POST'
      }))
      expect(result).toEqual(mockResponse)
    })
  })
})
