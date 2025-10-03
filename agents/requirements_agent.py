from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json

class RequirementsAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.1
        )
        
    def gather_requirements(self, user_input):
        """Convert conversational input into structured requirements"""
        prompt = ChatPromptTemplate.from_template("""
You are an expert enterprise software consultant with 15+ years experience helping 
Fortune 500 companies select SaaS tools.

Analyze the following enterprise SaaS requirement and extract structured information:

User Input: {user_input}

Extract and structure the following:
1. Primary use case and business objectives
2. Technical requirements (integrations, performance, scalability)
3. Compliance and security requirements
4. Stakeholder concerns (different departments)
5. Budget constraints and timeline
6. Success criteria and KPIs

Return ONLY a valid JSON object with these categories.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"user_input": user_input})
        
        try:
            # Try to parse JSON from the response
            content = result.content
            # Find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"raw_requirements": content}
        except:
            return {"raw_requirements": result.content}
    
    def generate_rfp(self, structured_requirements):
        """Generate a comprehensive RFP from structured requirements"""
        prompt = ChatPromptTemplate.from_template("""
You are an expert enterprise software consultant creating RFP documents.

Create a comprehensive Request for Proposal (RFP) document based on these requirements:

{requirements}

Generate an RFP that includes:
1. Executive Summary
2. Detailed Functional Requirements
3. Technical Specifications
4. Security and Compliance Requirements
5. Integration Requirements
6. Performance and Scalability Needs
7. Evaluation Criteria and Weightings
8. Timeline and Implementation Requirements
9. Vendor Response Format
10. Selection Process Overview

Make it professional and comprehensive for enterprise procurement.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"requirements": json.dumps(structured_requirements, indent=2)})
        return result.content
    
    def identify_stakeholders(self, requirements):
        """Identify key stakeholders based on requirements"""
        stakeholder_map = {
            "security": ["CISO", "Security Team", "Compliance Officer"],
            "integration": ["CTO", "Engineering Manager", "DevOps Team"],
            "budget": ["CFO", "Finance Team", "Procurement"],
            "compliance": ["Legal Team", "Compliance Officer", "Risk Management"],
            "user_experience": ["End Users", "Department Heads", "Training Team"]
        }
        
        identified_stakeholders = []
        req_text = json.dumps(requirements).lower()
        
        for category, stakeholders in stakeholder_map.items():
            if category in req_text:
                identified_stakeholders.extend(stakeholders)
        
        return list(set(identified_stakeholders))
