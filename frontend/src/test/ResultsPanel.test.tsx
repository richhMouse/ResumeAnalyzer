import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ResultsPanel from '../components/ResultsPanel'

describe('ResultsPanel', () => {
  const mockData = {
    strengths: ['Strong leadership experience', 'Good metrics'],
    weaknesses: ['Missing keywords', 'Poor structure'],
    suggestions: ['Add more metrics', 'Use bullet points']
  }

  it('renders all three sections', () => {
    render(<ResultsPanel {...mockData} />)
    
    expect(screen.getByText('Factual Strengths')).toBeInTheDocument()
    expect(screen.getByText('Factual Weaknesses')).toBeInTheDocument()
    expect(screen.getByText('Actionable Improvements')).toBeInTheDocument()
  })

  it('renders strengths items', () => {
    render(<ResultsPanel {...mockData} />)
    
    expect(screen.getByText('Strong leadership experience')).toBeInTheDocument()
    expect(screen.getByText('Good metrics')).toBeInTheDocument()
  })

  it('renders weaknesses items', () => {
    render(<ResultsPanel {...mockData} />)
    
    expect(screen.getByText('Missing keywords')).toBeInTheDocument()
    expect(screen.getByText('Poor structure')).toBeInTheDocument()
  })

  it('renders suggestions with numbers', () => {
    render(<ResultsPanel {...mockData} />)
    
    expect(screen.getByText('Add more metrics')).toBeInTheDocument()
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })

  it('handles empty arrays', () => {
    render(<ResultsPanel strengths={[]} weaknesses={[]} suggestions={[]} />)
    
    expect(screen.getByText('Factual Strengths')).toBeInTheDocument()
    expect(screen.getByText('Factual Weaknesses')).toBeInTheDocument()
    expect(screen.getByText('Actionable Improvements')).toBeInTheDocument()
  })
})
