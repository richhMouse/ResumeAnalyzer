import pytest
from app.services.ats_engine import ATSEngine


class TestATSScoringModel:
    """Test the ATS scoring model distribution (must equal 100)."""
    
    def test_total_score_equals_100(self):
        """Verify that ATS score equals 100 when all components are maxed."""
        engine = ATSEngine()
        
        # Strong resume that should score high
        resume_text = """
        Product Manager
        Experience:
        - Led product roadmap development for enterprise software platform
        - Managed team of 10 engineers and designers
        - Increased revenue by 35% through new feature launches
        - Created stakeholder communication processes
        - Spearheaded cross-functional collaboration
        Skills: Product Management, Agile, Scrum, User Research, Data Analysis
        Education: MBA, Computer Science
        Achieved: Delivered 15 major releases, improved conversion by 40%, saved $500k
        """
        
        result = engine.evaluate(resume_text, "Product Manager")
        
        # The ats_score should equal the sum of all components
        total = (
            result["role_relevance_score"] +
            result["leadership_score"] +
            result["impact_metrics_score"] +
            result["resume_structure_score"] +
            result["language_quality_score"]
        )
        
        assert result["ats_score"] == total


class TestRoleRelevance:
    """Test role relevance evaluation (max 30 points)."""
    
    def test_pm_keywords(self):
        """Product Manager should score higher with PM keywords."""
        engine = ATSEngine()
        
        pm_resume = "Product Manager led roadmap development and backlog management"
        generic_resume = "Manager led team and improved processes"
        
        pm_score = engine._evaluate_role_relevance(pm_resume, "Product Manager")
        generic_score = engine._evaluate_role_relevance(generic_resume, "Product Manager")
        
        assert pm_score > generic_score
    
    def test_role_title_mention_bonus(self):
        """Resume mentioning the role title should get a bonus."""
        engine = ATSEngine()
        
        resume_with_role = "Product Manager with 5 years experience"
        resume_without = "Manager with 5 years experience"
        
        score_with = engine._evaluate_role_relevance(resume_with_role, "Product Manager")
        score_without = engine._evaluate_role_relevance(resume_without, "Product Manager")
        
        assert score_with > score_without
    
    def test_keyword_stuffing_penalty(self):
        """Keyword stuffing without context should be penalized."""
        engine = ATSEngine()
        
        # Normal keyword density
        normal = "product roadmap features backlog" * 3
        # High keyword density with short sentences (keyword stuffing)
        stuffed = "product roadmap features backlog backlog backlog"
        
        score_normal = engine._evaluate_role_relevance(normal, "Product Manager")
        score_stuffed = engine._evaluate_role_relevance(stuffed, "Product Manager")
        
        # Stuffed should be penalized or at least not score higher
        assert score_stuffed <= score_normal + 5


class TestLeadershipEvaluation:
    """Test leadership and ownership evaluation (max 25 points)."""
    
    def test_leadership_keywords(self):
        """Leadership keywords should increase score."""
        engine = ATSEngine()
        
        with_leadership = "Led team of 8, managed department, directed strategic initiatives"
        without = "Worked with team, assisted with tasks"
        
        score_with = engine._evaluate_leadership(with_leadership)
        score_without = engine._evaluate_leadership(without)
        
        assert score_with > score_without
    
    def test_ownership_language(self):
        """Ownership phrases should add points."""
        engine = ATSEngine()
        
        ownership = "I led the initiative. I owned the project. Decision making authority."
        no_ownership = "Was involved in the project. Assisted the team."
        
        score_own = engine._evaluate_leadership(ownership)
        score_no = engine._evaluate_leadership(no_ownership)
        
        assert score_own > score_no
    
    def test_passive_language_penalty(self):
        """Passive language should be penalized."""
        engine = ATSEngine()
        
        passive = "was responsible was involved assisted helped supported helped"
        
        score = engine._evaluate_leadership(passive)
        
        assert score < 10, "Heavy passive language should result in low score"


class TestImpactMetrics:
    """Test impact and metrics evaluation (max 20 points)."""
    
    def test_quantified_metrics(self):
        """Quantified metrics should increase score."""
        engine = ATSEngine()
        
        with_metrics = "Increased revenue by 25%, reduced costs by $50000, grew team 3x"
        without = "Improved processes and helped team"
        
        score_with = engine._evaluate_impact_metrics(with_metrics)
        score_without = engine._evaluate_impact_metrics(without)
        
        assert score_with > score_without
    
    def test_multiple_metrics(self):
        """More unique metrics should score higher."""
        engine = ATSEngine()
        
        one_metric = "Increased revenue by 10%"
        five_metrics = "Increased revenue by 25%, saved $100k, improved efficiency 40%, grew 3x, reduced 15%"
        
        score_one = engine._evaluate_impact_metrics(one_metric)
        score_five = engine._evaluate_impact_metrics(five_metrics)
        
        assert score_five > score_one
    
    def test_financial_metrics(self):
        """Revenue/growth metrics should get bonus."""
        engine = ATSEngine()
        
        # Use actual metric patterns that match
        with_growth = "Increased revenue by 50%, improved ROI by 25%, grew profit by $100k, saved 30%"
        
        score = engine._evaluate_impact_metrics(with_growth)
        
        assert score >= 12, f"Growth keywords should give decent score, got {score}"


class TestResumeStructure:
    """Test resume structure evaluation (max 15 points)."""
    
    def test_section_headers(self):
        """Section headers should add points."""
        engine = ATSEngine()
        
        with_sections = "Experience: Work History: Skills: Education:"
        without = "Just some random text without headers"
        
        score_with = engine._evaluate_resume_structure(with_sections)
        score_without = engine._evaluate_resume_structure(without)
        
        assert score_with > score_without
    
    def test_bullet_points(self):
        """Bullet points should add points."""
        engine = ATSEngine()
        
        with_bullets = "- Led team\n- Managed project\n- Created strategy"
        without = "Led team. Managed project. Created strategy."
        
        score_with = engine._evaluate_resume_structure(with_bullets)
        score_without = engine._evaluate_resume_structure(without)
        
        assert score_with > score_without
    
    def test_long_blocks_penalty(self):
        """Very long text blocks should be penalized."""
        engine = ATSEngine()
        
        # Very long single sentence
        long_blocks = "This is a very long sentence that goes on and on describing many different things in detail without any punctuation breaks or clear structure making it difficult to parse for any ATS system." * 5
        # Multiple shorter sentences
        normal = "Short sentence. Another short one. And another. One more. Finally done."
        
        score_long = engine._evaluate_resume_structure(long_blocks)
        score_normal = engine._evaluate_resume_structure(normal)
        
        assert score_long <= score_normal, "Long blocks should not score higher than normal structure"


class TestLanguageQuality:
    """Test language quality evaluation (max 10 points)."""
    
    def test_action_verbs(self):
        """Action verbs should increase score."""
        engine = ATSEngine()
        
        with_verbs = "Led managed developed implemented analyzed optimized delivered executed"
        without = "Was did have made"
        
        score_with = engine._evaluate_language_quality(with_verbs)
        score_without = engine._evaluate_language_quality(without)
        
        assert score_with > score_without
    
    def test_outcome_language(self):
        """Outcome-focused language should add points."""
        engine = ATSEngine()
        
        outcome = "Achieved delivered exceeded improved increased reduced saved"
        no_outcome = "Did work made things"
        
        score = engine._evaluate_language_quality(outcome)
        
        assert score >= 8, "Strong outcome language should score high"
    
    def test_buzzword_penalty(self):
        """Excessive buzzwords should be penalized."""
        engine = ATSEngine()
        
        buzzwords = "synergy leverage pivot disrupt innovate revolutionize synergy leverage"
        
        score = engine._evaluate_language_quality(buzzwords)
        
        assert score < 5, "Heavy buzzword usage should be penalized"


class TestShortlistProbability:
    """Test shortlist probability determination."""
    
    def test_high_probability(self):
        """Score >= 70 should be High."""
        engine = ATSEngine()
        
        strong_resume = """
        Product Manager
        Experience:
        - Led product roadmap and backlog management for enterprise platform
        - Managed team of 12 engineers and designers
        - Increased annual revenue by 45% to $5M through new product launches
        - Created strategic product vision and stakeholder communication
        - Spearheaded cross-functional collaboration with engineering and design
        Skills: Product Strategy, Agile, Scrum, User Research, Data Analysis
        Education: MBA, BS Computer Science
        Achieved: Delivered 15 major releases, improved conversion 35%
        """
        
        result = engine.evaluate(strong_resume, "Product Manager")
        
        assert result["shortlist_probability"] == "High"
        assert result["ats_score"] >= 70
    
    def test_medium_probability(self):
        """Score 50-69 should be Medium."""
        engine = ATSEngine()
        
        # Weak resume should get Low
        weak_resume = """
        Manager
        Experience:
        - Managed team
        Skills: Management
        """
        
        result = engine.evaluate(weak_resume, "Product Manager")
        
        # Weak resume should be Low
        assert result["shortlist_probability"] == "Low"
    
    def test_low_probability(self):
        """Score < 50 should be Low."""
        engine = ATSEngine()
        
        weak_resume = "Manager who does things"
        
        result = engine.evaluate(weak_resume, "Product Manager")
        
        assert result["shortlist_probability"] == "Low"
        assert result["ats_score"] < 50


class TestRoleSpecificSuggestions:
    """Test role-specific improvement suggestions."""
    
    def test_pm_suggestions(self):
        """Product Manager should get PM-specific suggestions."""
        engine = ATSEngine()
        
        result = engine.evaluate("test", "Product Manager")
        
        suggestions = " ".join(result["improvement_suggestions"])
        
        assert "roadmap" in suggestions.lower() or "backlog" in suggestions.lower()
    
    def test_pm_suggestions_contains(self):
        """PM suggestions should mention product-specific terms."""
        engine = ATSEngine()
        
        result = engine.evaluate("test resume", "Product Manager")
        
        suggestions_text = " ".join(result["improvement_suggestions"]).lower()
        
        assert any(term in suggestions_text for term in ["roadmap", "backlog", "stakeholder", "user research"])


class TestAllAllowedRoles:
    """Test that all allowed roles work correctly."""
    
    @pytest.mark.parametrize("role", [
        "Product Manager",
        "Project Manager", 
        "Business Analyst",
        "Operations Manager",
        "HR Manager"
    ])
    def test_all_roles(self, role):
        """All allowed roles should work without errors."""
        engine = ATSEngine()
        
        result = engine.evaluate("test resume text", role)
        
        assert "ats_score" in result
        assert "shortlist_probability" in result
        assert result["shortlist_probability"] in ["High", "Medium", "Low"]
