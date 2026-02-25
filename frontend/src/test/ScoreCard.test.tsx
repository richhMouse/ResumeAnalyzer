import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ScoreCard from '../components/ScoreCard'

describe('ScoreCard', () => {
  it('renders title and score correctly', () => {
    render(<ScoreCard title="Role Relevance" score={25} max={30} color="#8b5cf6" />)
    
    expect(screen.getByText('Role Relevance')).toBeInTheDocument()
    expect(screen.getByText('25/30')).toBeInTheDocument()
  })

  it('calculates percentage correctly', () => {
    render(<ScoreCard title="Leadership" score={15} max={25} color="#3b82f6" />)
    
    const fillBar = document.querySelector('.score-card-fill') as HTMLElement
    expect(fillBar.style.width).toBe('60%')
  })

  it('accepts delay prop for animation', () => {
    const { container } = render(
      <ScoreCard title="Impact" score={10} max={20} color="#10b981" delay={2} />
    )
    
    const card = container.querySelector('.score-card')
    expect(card).toHaveStyle({ '--delay': '0.2s' })
  })

  it('handles zero score', () => {
    render(<ScoreCard title="Structure" score={0} max={15} color="#f59e0b" />)
    
    expect(screen.getByText('0/15')).toBeInTheDocument()
  })

  it('handles max score', () => {
    render(<ScoreCard title="Language" score={10} max={10} color="#ec4899" />)
    
    expect(screen.getByText('10/10')).toBeInTheDocument()
  })
})
