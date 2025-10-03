from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import pandas as pd

class VendorMatchingAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.1
        )
        
        # Sample vendor database for MVP
        self.vendor_db = self._load_vendor_database()
    
    def _load_vendor_database(self):
        """Load sample vendor database for demo"""
        return {
            "ai_infrastructure": [
                {
                    "name": "Coactive AI",
                    "category": "AI Infrastructure",
                    "description": "Data labeling software",
                    "strengths": ["AI-powered data labeling", "Computer vision support", "Model training optimization"],
                    "integrations": ["Python", "TensorFlow", "PyTorch", "AWS", "GCP"],
                    "compliance": ["SOC2", "GDPR"],
                    "pricing_model": "Usage-based",
                    "adoption_score": 88,
                    "enterprise_fit": 92,
                    "funding": "$44M",
                    "year_founded": 2021,
                    "location": "San Jose, United States",
                    "icon": "🏷️"
                },
                {
                    "name": "Cohere",
                    "category": "AI Infrastructure",
                    "description": "AI model developer",
                    "strengths": ["Enterprise LLMs", "Customizable models", "Privacy-focused"],
                    "integrations": ["REST API", "Python SDK", "AWS", "Azure", "GCP"],
                    "compliance": ["SOC2", "GDPR", "HIPAA"],
                    "pricing_model": "API-based",
                    "adoption_score": 90,
                    "enterprise_fit": 95,
                    "funding": "$1B",
                    "year_founded": 2019,
                    "location": "Toronto, Canada",
                    "icon": "🧠"
                }
            ],
            "observability": [
                {
                    "name": "DataDog",
                    "category": "Observability & Monitoring",
                    "strengths": ["APM", "Infrastructure Monitoring", "Log Management"],
                    "integrations": ["AWS", "Kubernetes", "GitHub", "Slack"],
                    "compliance": ["SOC2", "GDPR", "HIPAA"],
                    "pricing_model": "Usage-based",
                    "adoption_score": 87,
                    "enterprise_fit": 95
                },
                {
                    "name": "New Relic",
                    "category": "Observability & Monitoring", 
                    "strengths": ["Full-stack Observability", "AI-powered Insights"],
                    "integrations": ["AWS", "Azure", "GCP", "Jenkins"],
                    "compliance": ["SOC2", "FedRAMP", "GDPR"],
                    "pricing_model": "User-based",
                    "adoption_score": 82,
                    "enterprise_fit": 90
                },
                {
                    "name": "Grafana",
                    "category": "Observability & Monitoring",
                    "strengths": ["Open Source", "Customizable Dashboards", "Cost-effective"],
                    "integrations": ["Prometheus", "InfluxDB", "Elasticsearch"],
                    "compliance": ["SOC2", "GDPR"],
                    "pricing_model": "Freemium",
                    "adoption_score": 78,
                    "enterprise_fit": 75
                }
            ],
            "crm": [
                {
                    "name": "Salesforce",
                    "category": "CRM",
                    "strengths": ["Market Leader", "Extensive Customization", "AppExchange"],
                    "integrations": ["Microsoft", "Google", "Slack", "Tableau"],
                    "compliance": ["SOC2", "GDPR", "HIPAA", "FedRAMP"],
                    "pricing_model": "Per-user",
                    "adoption_score": 89,
                    "enterprise_fit": 98
                },
                {
                    "name": "HubSpot",
                    "category": "CRM",
                    "strengths": ["User-friendly", "Marketing Automation", "Free Tier"],
                    "integrations": ["Gmail", "Outlook", "Slack", "Zoom"],
                    "compliance": ["SOC2", "GDPR"],
                    "pricing_model": "Freemium",
                    "adoption_score": 85,
                    "enterprise_fit": 70
                }
            ]
        }
    
    def match_vendors(self, requirements):
        """Match requirements to suitable vendors"""
        prompt = ChatPromptTemplate.from_template("""
You are a veteran enterprise software analyst with deep knowledge of the SaaS ecosystem.

Based on these enterprise requirements, identify and rank the most suitable vendors:

Requirements: {requirements}

Available Vendor Database: {vendor_db}

For each potential vendor match:
1. Calculate fit score (0-100) based on requirements alignment
2. Identify specific strengths that match requirements
3. Note any gaps or concerns
4. Assess integration compatibility
5. Evaluate compliance alignment
6. Consider enterprise readiness

Return top 3-5 vendors ranked by overall fit score with detailed reasoning.
Format as JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "requirements": json.dumps(requirements, indent=2),
            "vendor_db": json.dumps(self.vendor_db, indent=2)
        })
        
        try:
            content = result.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"vendor_analysis": content}
        except:
            return {"vendor_analysis": result.content}
    
    def generate_vendor_comparison(self, matched_vendors):
        """Generate side-by-side vendor comparison"""
        prompt = ChatPromptTemplate.from_template("""
Create a comprehensive side-by-side comparison of these matched vendors:

{matched_vendors}

Create a comparison table including:
1. Key Features and Capabilities
2. Integration Support
3. Compliance Certifications
4. Pricing Models
5. Implementation Complexity
6. Support and Training
7. Pros and Cons for this specific use case
8. Risk Assessment

Format as a structured comparison that helps decision-makers.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"matched_vendors": json.dumps(matched_vendors, indent=2)})
        return result.content
    
    def predict_adoption_success(self, vendor, requirements):
        """Predict likelihood of successful adoption"""
        # Simplified scoring algorithm for MVP
        base_score = vendor.get("adoption_score", 70)
        enterprise_fit = vendor.get("enterprise_fit", 70)
        
        # Adjust based on requirement complexity
        complexity_penalty = 0
        if "integration" in str(requirements).lower():
            complexity_penalty += 5
        if "compliance" in str(requirements).lower():
            complexity_penalty += 3
        
        final_score = min(95, (base_score + enterprise_fit) / 2 - complexity_penalty)
        
        return {
            "adoption_probability": final_score,
            "confidence_level": "High" if final_score > 80 else "Medium" if final_score > 60 else "Low",
            "key_success_factors": vendor.get("strengths", []),
            "potential_risks": ["Integration complexity", "Change management"] if final_score < 70 else []
        }
