export interface ATSRequest {
  resume_text: string;
  target_role: string;
}

export interface ATSResponse {
  ats_score: number;
  shortlist_probability: 'High' | 'Medium' | 'Low';
  role_relevance_score: number;
  leadership_score: number;
  impact_metrics_score: number;
  resume_structure_score: number;
  language_quality_score: number;
  factual_strengths: string[];
  factual_weaknesses: string[];
  improvement_suggestions: string[];
}

export const ALLOWED_ROLES = [
  // Management Roles
  'Product Manager',
  'Project Manager',
  'Business Analyst',
  'Operations Manager',
  'HR Manager',
  // Tech Roles
  'Software Engineer',
  'Full Stack Developer',
  'Data Scientist',
  'Data Analyst',
  'DevOps Engineer',
  'Cloud Engineer'
] as const;

export type Role = typeof ALLOWED_ROLES[number];
