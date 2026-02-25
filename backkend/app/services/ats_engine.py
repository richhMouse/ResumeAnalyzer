import re
from typing import Dict, List, Any

class ATSEngine:
    """ATS Resume Analyzer for Management and Tech Roles"""
    
    ROLE_KEYWORDS = {
        # Management Roles
        "Product Manager": [
            "product", "roadmap", "features", "stakeholder", "user research", 
            "backlog", "sprint", "MVP", "product strategy", "roadmapping",
            "requirements", "PRDs", "specifications", "metrics", "KPI",
            "user stories", "agile", "scrum", "product lifecycle"
        ],
        "Project Manager": [
            "project", "timeline", "milestone", "deliverable", "budget",
            "resource", "scheduling", "risk", "stakeholder", "coordination",
            "planning", "execution", "monitoring", "reporting", "PMO",
            "scope", "WBS", "gantt", "critical path", "waterfall", "agile"
        ],
        "Business Analyst": [
            "requirements", "analysis", "stakeholder", "process", "workflow",
            "documentation", "BRD", "FRD", "use case", "data analysis",
            "modeling", "BAU", "improvement", "gap analysis", "solution",
            "consulting", "functional", "technical", "specifications"
        ],
        "Operations Manager": [
            "operations", "process", "efficiency", "optimization", "workflow",
            "supply chain", "inventory", "logistics", "vendor", "KPI",
            "metrics", "cost reduction", "throughput", "capacity", "planning",
            "resource allocation", "budget", "team management", "continuous improvement"
        ],
        "HR Manager": [
            "human resources", "HR", "recruitment", "hiring", "talent",
            "employee relations", "performance management", "compensation",
            "benefits", "training", "development", "policy", "compliance",
            "labor law", "onboarding", "offboarding", "succession", "culture"
        ],
        # Tech Roles
        "Software Engineer": [
            "software", "engineering", "code", "development", "programming",
            "algorithm", "debugging", "testing", "refactoring", "architecture",
            "design patterns", "OOP", "data structures", "API", "database",
            "SQL", "NoSQL", "Git", "CI/CD", "agile", "scrum"
        ],
        "Full Stack Developer": [
            "frontend", "backend", "full stack", "React", "Angular", "Vue",
            "Node.js", "Python", "Java", "REST API", "GraphQL", "database",
            "MongoDB", "PostgreSQL", "AWS", "Docker", "Kubernetes", "Git",
            "JavaScript", "TypeScript", "HTML", "CSS", "responsive design"
        ],
        "Data Scientist": [
            "machine learning", "deep learning", "data science", "Python", "R",
            "TensorFlow", "PyTorch", "scikit-learn", "statistics", "analytics",
            "predictive modeling", "NLP", "computer vision", "data visualization",
            "Pandas", "NumPy", "SQL", "big data", "feature engineering"
        ],
        "Data Analyst": [
            "data analysis", "analytics", "Excel", "SQL", "Tableau", "Power BI",
            "Python", "statistics", "reporting", "visualization", "dashboards",
            "data cleaning", "ETL", "business intelligence", "KPIs", "metrics",
            "insights", "trend analysis", "forecasting", "presentations"
        ],
        "DevOps Engineer": [
            "DevOps", "CI/CD", "Jenkins", "Docker", "Kubernetes", "AWS", "Azure",
            "GCP", "infrastructure", "automation", "scripting", "Terraform",
            "Ansible", "pipeline", "monitoring", "logging", "cloud", "Linux",
            "configuration management", "release management"
        ],
        "Cloud Engineer": [
            "cloud", "AWS", "Azure", "GCP", "infrastructure", "architecture",
            "serverless", "Lambda", "Kubernetes", "Docker", "networking",
            "security", "compliance", "cost optimization", "migration",
            "IaC", "Terraform", "cloudformation", "monitoring", "disaster recovery"
        ]
    }
    
    LEADERSHIP_KEYWORDS = [
        "led", "managed", "directed", "owned", "spearheaded", "championed",
        "mentored", "coached", "developed", "built", "established", "created",
        "implemented", "optimized", "transformed", "restructured", "negotiated",
        "approved", "authorized", "decided", "strategic", "vision", "roadmap"
    ]
    
    METRICS_PATTERNS = [
        r'(\d+%)\s*(increase|decrease|reduction|growth|improvement)',
        r'\$[\d,]+(?:\.\d+)?(?:\s*(million|billion|M|B))?',
        r'(\d+)\s*(x|times|fold)',
        r'($|€|£)\s*\d+[\d,]*\.?\d*\s*(k|m|billion)?',
        r'(\d+)\s*(employees|team members|reports|direct reports)',
        r'(\d+%)\s*(conversion|retention|engagement|adoption)',
        r'saved\s*\$?[\d,]+',
        r'reduced\s*\d+%',
        r'improved\s*\d+%',
    ]
    
    ACTION_VERBS = [
        "led", "managed", "coordinated", "developed", "implemented",
        "analyzed", "optimized", "streamlined", "reduced", "increased",
        "delivered", "executed", "facilitated", "negotiated", "influenced",
        "achieved", "exceeded", "transformed", "established", "created"
    ]
    
    def __init__(self):
        self.role_keywords = self.ROLE_KEYWORDS
        self.leadership_keywords = self.LEADERSHIP_KEYWORDS
        self.metrics_patterns = [re.compile(p, re.IGNORECASE) for p in self.METRICS_PATTERNS]
    
    def evaluate(self, resume_text: str, target_role: str) -> Dict[str, Any]:
        """Main evaluation method."""
        
        # Calculate all scores
        role_relevance_score = self._evaluate_role_relevance(resume_text, target_role)
        leadership_score = self._evaluate_leadership(resume_text)
        impact_metrics_score = self._evaluate_impact_metrics(resume_text)
        resume_structure_score = self._evaluate_resume_structure(resume_text)
        language_quality_score = self._evaluate_language_quality(resume_text)
        
        # Calculate total
        total_score = (
            role_relevance_score +
            leadership_score +
            impact_metrics_score +
            resume_structure_score +
            language_quality_score
        )
        
        # Determine shortlist probability
        if total_score >= 70:
            shortlist_prob = "High"
        elif total_score >= 50:
            shortlist_prob = "Medium"
        else:
            shortlist_prob = "Low"
        
        # Generate strengths, weaknesses, and suggestions
        strengths = self._extract_strengths(resume_text, target_role, role_relevance_score, leadership_score, impact_metrics_score)
        weaknesses = self._extract_weaknesses(resume_text, target_role, role_relevance_score, leadership_score, impact_metrics_score, resume_structure_score, language_quality_score)
        suggestions = self._generate_suggestions(resume_text, target_role, weaknesses)
        
        return {
            "ats_score": total_score,
            "shortlist_probability": shortlist_prob,
            "role_relevance_score": role_relevance_score,
            "leadership_score": leadership_score,
            "impact_metrics_score": impact_metrics_score,
            "resume_structure_score": resume_structure_score,
            "language_quality_score": language_quality_score,
            "factual_strengths": strengths,
            "factual_weaknesses": weaknesses,
            "improvement_suggestions": suggestions
        }
    
    def _evaluate_role_relevance(self, text: str, role: str) -> int:
        """Evaluate how well resume matches target role (30 points max)."""
        text_lower = text.lower()
        keywords = self.role_keywords.get(role, [])
        
        matched = sum(1 for kw in keywords if kw.lower() in text_lower)
        keyword_density = matched / len(keywords) if keywords else 0
        
        # Base score from keyword matching
        score = int(min(25, keyword_density * 50))
        
        # Check for role title mention
        role_title = role.lower()
        if role_title in text_lower:
            score += 5
        
        # Penalize keyword stuffing without context
        if keyword_density > 0.6 and not self._has_context(text, keywords):
            score -= 5
        
        return max(0, min(30, score))
    
    def _has_context(self, text: str, keywords: List[str]) -> bool:
        """Check if keywords appear in meaningful context."""
        sentences = text.split('.')
        for kw in keywords[:5]:
            for sentence in sentences:
                if kw.lower() in sentence.lower() and len(sentence.strip()) > 20:
                    return True
        return False
    
    def _evaluate_leadership(self, text: str) -> int:
        """Evaluate leadership and ownership signals (25 points max)."""
        text_lower = text.lower()
        
        # Count leadership keywords
        matched = sum(1 for kw in self.leadership_keywords if kw in text_lower)
        leadership_density = matched / len(self.leadership_keywords)
        
        score = int(min(20, leadership_density * 40))
        
        # Check for ownership language
        ownership_patterns = [
            r'\b(I led|I managed|I directed|I owned|I created)\b',
            r'\b(responsible for|accountable for)\b',
            r'\b(decision making|strategic|vision)\b',
            r'\b(cross-functional|cross functional)\b',
            r'\b(stakeholder|executive|board)\b',
        ]
        
        ownership_matches = 0
        for pattern in ownership_patterns:
            if re.search(pattern, text_lower):
                ownership_matches += 1
        
        score += ownership_matches * 2
        
        # Penalize passive language
        passive_count = len(re.findall(r'\b(was responsible|was involved|assisted|helped|supported)\b', text_lower))
        if passive_count > 3:
            score -= min(5, passive_count - 3)
        
        return max(0, min(25, score))
    
    def _evaluate_impact_metrics(self, text: str) -> int:
        """Evaluate quantified outcomes and business metrics (20 points max)."""
        metrics_found = []
        
        for pattern in self.metrics_patterns:
            matches = pattern.findall(text)
            metrics_found.extend(matches)
        
        unique_metrics = len(set(metrics_found))
        
        # Score based on quantified metrics
        if unique_metrics >= 5:
            score = 20
        elif unique_metrics >= 3:
            score = 15
        elif unique_metrics >= 1:
            score = 10
        else:
            score = 2
        
        # Bonus for revenue/growth metrics
        growth_keywords = ['revenue', 'growth', 'profit', 'ROI', 'savings', 'cost reduction']
        growth_count = sum(1 for kw in growth_keywords if kw in text.lower())
        
        if growth_count >= 2:
            score = min(20, score + 3)
        
        return max(0, min(20, score))
    
    def _evaluate_resume_structure(self, text: str) -> int:
        """Evaluate ATS readability and structure (15 points max)."""
        score = 0
        
        # Check for section headers
        section_keywords = ['experience', 'education', 'skills', 'work history', 'employment']
        text_lower = text.lower()
        
        section_count = sum(1 for sec in section_keywords if sec in text_lower)
        score += section_count * 2
        
        # Check for bullet points
        bullet_count = len(re.findall(r'[•\-\*]\s', text))
        if bullet_count >= 5:
            score += 5
        elif bullet_count >= 1:
            score += 3
        
        # Check for proper formatting (no huge text blocks)
        sentences = text.split('.')
        long_blocks = sum(1 for s in sentences if len(s) > 200)
        
        if long_blocks > 2:
            score -= 3
        
        return max(0, min(15, score))
    
    def _evaluate_language_quality(self, text: str) -> int:
        """Evaluate action verbs and outcome-focused language (10 points max)."""
        text_lower = text.lower()
        
        # Count action verbs
        action_verb_count = sum(1 for verb in self.ACTION_VERBS if verb in text_lower)
        
        if action_verb_count >= 10:
            score = 10
        elif action_verb_count >= 5:
            score = 7
        elif action_verb_count >= 2:
            score = 4
        else:
            score = 1
        
        # Check for outcome-focused language
        outcome_keywords = ['achieved', 'delivered', 'exceeded', 'improved', 'increased', 'reduced', 'saved']
        outcome_count = sum(1 for kw in outcome_keywords if kw in text_lower)
        
        if outcome_count >= 3:
            score = min(10, score + 2)
        
        # Penalize buzzword padding
        buzzwords = ['synergy', 'leverage', 'pivot', 'disrupt', 'innovate', 'revolutionize']
        buzzword_count = sum(1 for bw in buzzwords if bw in text_lower)
        
        if buzzword_count > 2:
            score -= min(3, buzzword_count - 2)
        
        return max(0, min(10, score))
    
    def _extract_strengths(self, text: str, role: str, role_score: int, leadership_score: int, impact_score: int) -> List[str]:
        """Extract factual strengths from resume."""
        strengths = []
        
        if role_score >= 20:
            strengths.append(f"Strong keyword alignment with {role} role requirements")
        
        if leadership_score >= 15:
            strengths.append("Demonstrates clear leadership and ownership in role descriptions")
        
        if impact_score >= 12:
            strengths.append("Includes quantified business metrics and measurable outcomes")
        
        # Check for specific leadership signals
        text_lower = text.lower()
        if 'led' in text_lower or 'managed' in text_lower:
            strengths.append("Uses action-oriented leadership verbs")
        
        if re.search(r'\$[\d,]+', text):
            strengths.append("Includes financial metrics and budget figures")
        
        if 'team' in text_lower or 'department' in text_lower:
            strengths.append("Demonstrates team management experience")
        
        if 'stakeholder' in text_lower:
            strengths.append("Shows stakeholder engagement and communication")
        
        return strengths[:5]  # Limit to 5 strengths
    
    def _extract_weaknesses(self, text: str, role: str, role_score: int, leadership_score: int, impact_score: int, structure_score: int, language_score: int) -> List[str]:
        """Extract factual weaknesses from resume."""
        weaknesses = []
        
        if role_score < 15:
            weaknesses.append(f"Weak alignment with {role} role keywords")
        
        if leadership_score < 10:
            weaknesses.append("Limited evidence of leadership ownership and decision-making authority")
        
        if impact_score < 8:
            weaknesses.append("Few or no quantified metrics to demonstrate business impact")
        
        if structure_score < 8:
            weaknesses.append("Poor ATS-friendly structure - missing clear section headers or bullet points")
        
        if language_score < 5:
            weaknesses.append("Weak action verb usage - relies on passive or vague language")
        
        # Check for specific issues
        text_lower = text.lower()
        if text_lower.count('responsible for') > 3:
            weaknesses.append("Overuses passive 'responsible for' phrasing")
        
        if len(text.split('.')) < 5:
            weaknesses.append("Resume content too brief for comprehensive evaluation")
        
        return weaknesses[:5]  # Limit to 5 weaknesses
    
    def _generate_suggestions(self, text: str, role: str, weaknesses: List[str]) -> List[str]:
        """Generate role-specific improvement suggestions."""
        suggestions = []
        text_lower = text.lower()
        
        # Role-specific suggestions
        role_suggestions = {
            # Management Roles
            "Product Manager": [
                "Add product roadmap, backlog management, and feature delivery examples",
                "Include user research and metrics-driven product decisions",
                "Show cross-functional collaboration with engineering and design"
            ],
            "Project Manager": [
                "Include specific project timelines, budgets, and resource allocation",
                "Add risk management and milestone achievement examples",
                "Demonstrate stakeholder coordination and reporting"
            ],
            "Business Analyst": [
                "Add requirements documentation and stakeholder analysis examples",
                "Include process mapping and improvement case studies",
                "Show data analysis and solution design experience"
            ],
            "Operations Manager": [
                "Add efficiency metrics and cost reduction examples",
                "Include workflow optimization and process improvement results",
                "Demonstrate vendor management and supply chain experience"
            ],
            "HR Manager": [
                "Add recruitment metrics and talent development examples",
                "Include employee relations and policy implementation results",
                "Demonstrate HR compliance and training program outcomes"
            ],
            # Tech Roles
            "Software Engineer": [
                "Add specific programming languages and technologies used",
                "Include code optimization and performance improvements",
                "Show system design and architecture experience"
            ],
            "Full Stack Developer": [
                "List specific frontend and backend technologies",
                "Include API design and database management examples",
                "Show deployment and DevOps experience"
            ],
            "Data Scientist": [
                "Add machine learning models and algorithms used",
                "Include metrics and accuracy improvements from models",
                "Show data preprocessing and feature engineering experience"
            ],
            "Data Analyst": [
                "Add specific tools used for analysis (Excel, SQL, Tableau)",
                "Include business insights derived from data",
                "Show dashboard creation and reporting experience"
            ],
            "DevOps Engineer": [
                "Add CI/CD pipeline and automation examples",
                "Include infrastructure-as-code and containerization",
                "Show monitoring and incident response experience"
            ],
            "Cloud Engineer": [
                "Add specific cloud platforms and services used",
                "Include cost optimization and security implementations",
                "Show cloud migration and architecture design experience"
            ]
        }
        
        # Add role-specific suggestions
        if role in role_suggestions:
            suggestions.extend(role_suggestions[role])
        
        # Add general improvement suggestions based on weaknesses
        if any('keyword' in w.lower() for w in weaknesses):
            suggestions.append("Integrate role-specific keywords naturally throughout experience descriptions")
        
        if any('metric' in w.lower() for w in weaknesses):
            suggestions.append("Add specific numbers: percentages, dollar amounts, timeframes, scale indicators")
        
        if any('leadership' in w.lower() for w in weaknesses):
            suggestions.append("Use stronger action verbs: led, directed, owned, spearheaded")
        
        if any('structure' in w.lower() for w in weaknesses):
            suggestions.append("Format with clear section headers and bullet points for ATS readability")
        
        return suggestions[:6]  # Limit to 6 suggestions
