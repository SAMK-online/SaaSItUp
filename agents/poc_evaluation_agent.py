from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

class POCEvaluationAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.1
        )
    
    def create_poc_rubric(self, requirements, vendors):
        """Generate custom POC evaluation rubric based on requirements"""
        prompt = ChatPromptTemplate.from_template("""
You are an expert in enterprise software evaluation methodologies.

Create a comprehensive POC evaluation rubric based on these requirements and vendors:

Requirements: {requirements}
Vendors: {vendors}

Create a rubric with:
1. Evaluation Categories (Integration, Performance, Security, UX, Cost, Operability)
2. Weighted scoring (total = 100%)
3. Specific criteria for each category
4. Scoring scale (1-5) with clear descriptions
5. Success thresholds for each criterion
6. Stakeholder assignment (who evaluates what)

Customize weights based on requirement priorities:
- High integration needs = higher Integration weight
- Performance critical = higher Performance weight
- Compliance heavy = higher Security weight

Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "requirements": json.dumps(requirements, indent=2),
            "vendors": json.dumps(vendors, indent=2)
        })
        
        try:
            content = result.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"rubric": content}
        except:
            return {"rubric": result.content}
    
    def simulate_poc_evaluation(self, rubric, vendor_name):
        """Simulate POC evaluation scores for demo purposes"""
        prompt = ChatPromptTemplate.from_template("""
Simulate realistic POC evaluation scores for {vendor_name} based on this rubric:

{rubric}

Generate realistic scores (1-5) for each criterion that reflect:
1. Typical enterprise evaluation patterns
2. Vendor strengths and weaknesses
3. Common implementation challenges
4. Stakeholder feedback variations

Include:
- Individual criterion scores with brief justification
- Stakeholder-specific feedback
- Overall category scores
- Weighted total score
- Key strengths and concerns identified

Make it realistic - no vendor is perfect, include both positives and areas for improvement.
Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "vendor_name": vendor_name,
            "rubric": json.dumps(rubric, indent=2)
        })
        
        try:
            content = result.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"evaluation": content}
        except:
            return {"evaluation": result.content}
    
    def synthesize_evaluations(self, evaluations):
        """Synthesize multiple vendor evaluations into final recommendations"""
        prompt = ChatPromptTemplate.from_template("""
Synthesize these POC evaluation results into final recommendations:

{evaluations}

Provide:
1. Vendor ranking with overall scores
2. Strengths and weaknesses comparison
3. Risk assessment for each vendor
4. Implementation complexity analysis
5. Adoption success predictions
6. Final recommendation with reasoning
7. Decision confidence score
8. Key factors that drove the recommendation

Consider:
- Not just highest score wins - factor in risk, complexity, stakeholder buy-in
- Implementation timeline and resource requirements
- Long-term strategic fit
- Change management implications
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"evaluations": json.dumps(evaluations, indent=2)})
        return result.content
    
    def generate_stakeholder_feedback(self, vendor, criteria):
        """Generate realistic stakeholder feedback for different personas"""
        feedback_templates = {
            "Engineering": {
                "focus": ["Integration", "Performance", "Operability"],
                "concerns": ["Technical debt", "Maintenance overhead", "Learning curve"]
            },
            "Security": {
                "focus": ["Security", "Compliance"],
                "concerns": ["Data privacy", "Access controls", "Audit trails"]
            },
            "Finance": {
                "focus": ["Cost", "ROI"],
                "concerns": ["Hidden costs", "Scalability pricing", "Contract terms"]
            },
            "End Users": {
                "focus": ["UX", "Performance"],
                "concerns": ["Ease of use", "Training requirements", "Workflow disruption"]
            }
        }
        
        stakeholder_feedback = {}
        for stakeholder, profile in feedback_templates.items():
            # Simulate realistic feedback based on stakeholder priorities
            feedback = {
                "overall_satisfaction": 3.5,  # Base score, would be customized per vendor
                "key_positives": [],
                "key_concerns": [],
                "recommendation": "Proceed with caution"
            }
            stakeholder_feedback[stakeholder] = feedback
        
        return stakeholder_feedback
