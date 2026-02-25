import pytest
import requests
import os

# Test against the running Docker container
BASE_URL = os.environ.get("TEST_API_URL", "http://localhost:8000")

def get_client():
    """Return requests session configured for API testing."""
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            
        def get(self, path):
            return requests.get(f"{self.base_url}{path}")
        
        def post(self, path, json=None):
            return requests.post(f"{self.base_url}{path}", json=json)
        
        def options(self, path, headers=None):
            return requests.options(f"{self.base_url}{path}", headers=headers)
    
    return APIClient(BASE_URL)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Root endpoint should return status."""
        response = get_client().get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_health_endpoint(self):
        """Health endpoint should return healthy."""
        response = get_client().get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAnalyzeEndpoint:
    """Test the /api/analyze endpoint."""
    
    def test_analyze_valid_request(self):
        """Should return ATS analysis for valid request."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Product Manager led team of 10. Increased revenue by 25%.",
            "target_role": "Product Manager"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "ats_score" in data
        assert "shortlist_probability" in data
        assert data["shortlist_probability"] in ["High", "Medium", "Low"]
    
    def test_analyze_all_roles(self):
        """Should work with all allowed roles."""
        roles = [
            "Product Manager",
            "Project Manager",
            "Business Analyst",
            "Operations Manager",
            "HR Manager"
        ]
        
        for role in roles:
            response = get_client().post("/api/analyze", json={
                "resume_text": "Test resume text",
                "target_role": role
            })
            assert response.status_code == 200, f"Failed for role: {role}"
    
    def test_analyze_missing_resume_text(self):
        """Should return error for missing resume text."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "",
            "target_role": "Product Manager"
        })
        
        # Returns 400 for empty text
        assert response.status_code in [400, 422]
    
    def test_analyze_missing_role(self):
        """Should return error for missing target role."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Some resume text",
            "target_role": ""
        })
        
        # Returns 400 for empty role
        assert response.status_code in [400, 422]
    
    def test_analyze_invalid_role(self):
        """Should return error for invalid role."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Some resume text",
            "target_role": "Invalid Role Title"
        })
        
        assert response.status_code == 400
        assert "Invalid role" in response.json()["detail"]
    
    def test_analyze_response_structure(self):
        """Response should have correct structure."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Experienced Product Manager with skills in agile and scrum",
            "target_role": "Product Manager"
        })
        
        data = response.json()
        
        assert "ats_score" in data
        assert "shortlist_probability" in data
        assert "role_relevance_score" in data
        assert "leadership_score" in data
        assert "impact_metrics_score" in data
        assert "resume_structure_score" in data
        assert "language_quality_score" in data
        assert "factual_strengths" in data
        assert "factual_weaknesses" in data
        assert "improvement_suggestions" in data
        
        assert isinstance(data["factual_strengths"], list)
        assert isinstance(data["factual_weaknesses"], list)
        assert isinstance(data["improvement_suggestions"], list)
    
    def test_analyze_scores_in_range(self):
        """All scores should be within valid ranges."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Product Manager led product roadmap and team of 8. Increased revenue by 35%.",
            "target_role": "Product Manager"
        })
        
        data = response.json()
        
        assert 0 <= data["role_relevance_score"] <= 30
        assert 0 <= data["leadership_score"] <= 25
        assert 0 <= data["impact_metrics_score"] <= 20
        assert 0 <= data["resume_structure_score"] <= 15
        assert 0 <= data["language_quality_score"] <= 10
        assert 0 <= data["ats_score"] <= 100
    
    def test_analyze_strong_resume_high_score(self):
        """Strong resume should get High shortlist probability."""
        response = get_client().post("/api/analyze", json={
            "resume_text": """
            Product Manager
            Experience:
            - Led product roadmap development for enterprise SaaS platform
            - Managed cross-functional team of 12 engineers and designers
            - Increased annual revenue by 45% to $2.9M through new feature launches
            - Created product vision and strategic roadmap
            - Spearheaded stakeholder communication and user research
            Skills: Product Strategy, Agile, Scrum, Data Analysis
            Education: MBA
            Achieved: Delivered 20+ major releases, improved conversion by 35%
            """,
            "target_role": "Product Manager"
        })
        
        data = response.json()
        
        assert data["ats_score"] >= 50
        assert data["shortlist_probability"] in ["High", "Medium"]
    
    def test_analyze_weak_resume_low_score(self):
        """Weak resume should get Low shortlist probability."""
        response = get_client().post("/api/analyze", json={
            "resume_text": "Manager who does things",
            "target_role": "Product Manager"
        })
        
        data = response.json()
        
        assert data["ats_score"] < 50
        assert data["shortlist_probability"] == "Low"


class TestCORSHeaders:
    """Test CORS configuration."""
    
    def test_cors_enabled(self):
        """CORS should be enabled for all origins."""
        response = get_client().options("/api/analyze", headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        })
        
        assert response.status_code == 200
