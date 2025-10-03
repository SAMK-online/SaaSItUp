from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

class RecommendationAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.1
        )
    
    def generate_final_recommendation(self, requirements, vendor_matches, poc_evaluations):
        """Generate comprehensive final recommendation report"""
        prompt = ChatPromptTemplate.from_template("""
You are a senior enterprise technology advisor with 20+ years experience.

Create an executive-level recommendation report based on:

Original Requirements: {requirements}
Vendor Analysis: {vendor_matches}
POC Evaluations: {poc_evaluations}

Generate a comprehensive report with:

1. EXECUTIVE SUMMARY
   - Clear recommendation with confidence score
   - Key decision factors
   - Expected business impact

2. VENDOR COMPARISON
   - Side-by-side scoring summary
   - Strengths/weaknesses matrix
   - Risk assessment for each option

3. IMPLEMENTATION ANALYSIS
   - Timeline and resource requirements
   - Change management considerations
   - Success probability assessment

4. FINANCIAL ANALYSIS
   - Total cost of ownership comparison
   - ROI projections
   - Budget impact analysis

5. RISK MITIGATION
   - Identified risks and mitigation strategies
   - Contingency planning
   - Success metrics and monitoring

6. NEXT STEPS
   - Immediate actions required
   - Implementation roadmap
   - Stakeholder communication plan

Make it executive-ready with clear action items and decision rationale.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "requirements": json.dumps(requirements, indent=2),
            "vendor_matches": json.dumps(vendor_matches, indent=2),
            "poc_evaluations": json.dumps(poc_evaluations, indent=2)
        })
        return result.content
    
    def calculate_confidence_score(self, evaluation_data):
        """Calculate decision confidence based on evaluation quality and consensus"""
        # Simplified confidence calculation for MVP
        factors = {
            "evaluation_completeness": 0.3,
            "stakeholder_consensus": 0.25,
            "vendor_differentiation": 0.2,
            "requirement_clarity": 0.15,
            "risk_assessment": 0.1
        }
        
        # Mock scoring for demo - would be based on actual evaluation data
        scores = {
            "evaluation_completeness": 85,  # Based on rubric coverage
            "stakeholder_consensus": 78,    # Based on score variance
            "vendor_differentiation": 82,   # Based on score gaps
            "requirement_clarity": 90,      # Based on requirement structure
            "risk_assessment": 75           # Based on identified risks
        }
        
        weighted_score = sum(scores[factor] * weight for factor, weight in factors.items())
        
        return {
            "confidence_score": round(weighted_score, 1),
            "confidence_level": self._get_confidence_level(weighted_score),
            "contributing_factors": scores,
            "improvement_areas": [factor for factor, score in scores.items() if score < 80]
        }
    
    def _get_confidence_level(self, score):
        """Convert numeric confidence to qualitative level"""
        if score >= 85:
            return "Very High"
        elif score >= 75:
            return "High"
        elif score >= 65:
            return "Medium"
        else:
            return "Low"
    
    def generate_adoption_prediction(self, recommended_vendor, requirements):
        """Predict adoption success and provide success factors"""
        prompt = ChatPromptTemplate.from_template("""
Based on the recommended vendor and requirements, predict adoption success:

Recommended Vendor: {recommended_vendor}
Requirements: {requirements}

Provide:
1. Adoption success probability (0-100%)
2. Key success factors that support adoption
3. Potential adoption risks and mitigation strategies
4. Timeline to full adoption
5. Success metrics to track
6. Change management recommendations

Base predictions on:
- Vendor's enterprise adoption track record
- Complexity of implementation
- Stakeholder buy-in levels
- Organizational change readiness
- Technical integration challenges

Return as JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "recommended_vendor": json.dumps(recommended_vendor, indent=2),
            "requirements": json.dumps(requirements, indent=2)
        })
        
        try:
            content = result.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"adoption_prediction": content}
        except:
            return {"adoption_prediction": result.content}
    
    def create_implementation_roadmap(self, recommended_vendor, requirements):
        """Create detailed implementation roadmap"""
        return {
            "phases": [
                {
                    "phase": "Planning & Preparation",
                    "duration": "2-4 weeks",
                    "key_activities": [
                        "Finalize contract negotiations",
                        "Set up project team",
                        "Define success metrics",
                        "Create communication plan"
                    ]
                },
                {
                    "phase": "Technical Setup",
                    "duration": "3-6 weeks", 
                    "key_activities": [
                        "Environment provisioning",
                        "Integration development",
                        "Security configuration",
                        "Data migration planning"
                    ]
                },
                {
                    "phase": "Pilot Deployment",
                    "duration": "2-4 weeks",
                    "key_activities": [
                        "Limited user rollout",
                        "Feedback collection",
                        "Issue resolution",
                        "Process refinement"
                    ]
                },
                {
                    "phase": "Full Rollout",
                    "duration": "4-8 weeks",
                    "key_activities": [
                        "Organization-wide deployment",
                        "User training delivery",
                        "Support process activation",
                        "Success metric tracking"
                    ]
                }
            ],
            "critical_success_factors": [
                "Executive sponsorship",
                "User training and adoption",
                "Technical integration quality",
                "Change management execution"
            ],
            "risk_mitigation": [
                "Regular stakeholder check-ins",
                "Phased rollout approach",
                "Dedicated support resources",
                "Rollback plan preparation"
            ]
        }
