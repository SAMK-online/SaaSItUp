import streamlit as st
import os
import json
from dotenv import load_dotenv
from agents.requirements_agent import RequirementsAgent
from agents.vendor_matching_agent import VendorMatchingAgent
from agents.poc_evaluation_agent import POCEvaluationAgent
from agents.recommendation_agent import RecommendationAgent

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(
    page_title="SaaSItIs - Enterprise SaaS Consultant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'requirements' not in st.session_state:
    st.session_state.requirements = None
if 'vendors' not in st.session_state:
    st.session_state.vendors = None
if 'poc_rubric' not in st.session_state:
    st.session_state.poc_rubric = None
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = None

def initialize_agents():
    """Initialize all agents with OpenAI API key"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set your OPENAI_API_KEY environment variable")
        st.stop()
    
    return {
        'requirements': RequirementsAgent(api_key),
        'vendor_matching': VendorMatchingAgent(api_key),
        'poc_evaluation': POCEvaluationAgent(api_key),
        'recommendation': RecommendationAgent(api_key)
    }

def get_marketplace_data():
    """Return marketplace data for all SaaS tools"""
    return [
        {"name": "Abridge", "description": "AI notetaker for doctors", "funding": "$458M", "year": 2018, "city": "San Francisco", "country": "United States", "category": "Healthcare", "icon": "🏥"},
        {"name": "Anthropic", "description": "AI model developer", "funding": "$17B", "year": 2020, "city": "San Francisco", "country": "United States", "category": "AI Infrastructure", "icon": "🤖"},
        {"name": "Anysphere", "description": "AI coding tools", "funding": "$176M", "year": 2022, "city": "San Francisco", "country": "United States", "category": "Development", "icon": "💻"},
        {"name": "Baseten", "description": "AI app deployment software", "funding": "$135M", "year": 2019, "city": "San Francisco", "country": "United States", "category": "DevOps", "icon": "🚀"},
        {"name": "Captions", "description": "Video editor", "funding": "$100M", "year": 2021, "city": "New York", "country": "United States", "category": "Media", "icon": "🎬"},
        {"name": "Clay", "description": "AI go-to-market tools", "funding": "$104M", "year": 2017, "city": "New York", "country": "United States", "category": "Sales", "icon": "📊"},
        {"name": "Coactive AI", "description": "Data labeling software", "funding": "$44M", "year": 2021, "city": "San Jose", "country": "United States", "category": "AI Infrastructure", "icon": "🏷️"},
        {"name": "Cohere", "description": "AI model developer", "funding": "$1B", "year": 2019, "city": "Toronto", "country": "Canada", "category": "AI Infrastructure", "icon": "🧠"},
        {"name": "Crusoe", "description": "AI infrastructure", "funding": "$1.6B", "year": 2018, "city": "San Francisco", "country": "United States", "category": "Infrastructure", "icon": "⚡"},
        {"name": "Databricks", "description": "Data storage and analytics", "funding": "$19B", "year": 2013, "city": "San Francisco", "country": "United States", "category": "Analytics", "icon": "📈"},
        {"name": "Decagon", "description": "AI agents for customer service", "funding": "$100M", "year": 2023, "city": "San Francisco", "country": "United States", "category": "Customer Service", "icon": "💬"},
        {"name": "DeepL", "description": "Language translation service", "funding": "$420M", "year": 2017, "city": "Cologne", "country": "Germany", "category": "Translation", "icon": "🌐"},
        {"name": "ElevenLabs", "description": "Voice generation software", "funding": "$281M", "year": 2022, "city": "London", "country": "United Kingdom", "category": "AI Tools", "icon": "🎙️"},
        {"name": "Figure AI", "description": "Humanoid robots", "funding": "$750M", "year": 2022, "city": "San Jose", "country": "United States", "category": "Robotics", "icon": "🤖"},
        {"name": "Fireworks AI", "description": "AI app development software", "funding": "$77M", "year": 2022, "city": "Redwood City", "country": "United States", "category": "Development", "icon": "🎆"},
        {"name": "Glean", "description": "Enterprise search engine", "funding": "$600M", "year": 2019, "city": "Palo Alto", "country": "United States", "category": "Search", "icon": "🔍"},
        {"name": "Harvey", "description": "Legal automation software", "funding": "$500M", "year": 2022, "city": "San Francisco", "country": "United States", "category": "Legal", "icon": "⚖️"},
        {"name": "Hebbia", "description": "General purpose AI for finance and legal", "funding": "$160M", "year": 2020, "city": "New York", "country": "United States", "category": "Finance", "icon": "💼"},
        {"name": "Hugging Face", "description": "Open-source library for AI models", "funding": "$395M", "year": 2016, "city": "New York", "country": "United States", "category": "AI Infrastructure", "icon": "🤗"},
        {"name": "Lambda", "description": "AI cloud provider", "funding": "$863M", "year": 2012, "city": "San Jose", "country": "United States", "category": "Cloud", "icon": "☁️"},
        {"name": "LangChain", "description": "AI app development tools", "funding": "$35M", "year": 2023, "city": "San Francisco", "country": "United States", "category": "Development", "icon": "🔗"},
        {"name": "Luminance", "description": "Enterprise contract automation", "funding": "$165M", "year": 2015, "city": "Cambridge", "country": "United Kingdom", "category": "Legal", "icon": "📄"},
        {"name": "Mercor", "description": "AI-powered hiring platform", "funding": "$135M", "year": 2023, "city": "San Francisco", "country": "United States", "category": "HR", "icon": "👥"},
        {"name": "Midjourney", "description": "Image generation service", "funding": "$0M", "year": 2021, "city": "San Francisco", "country": "United States", "category": "AI Tools", "icon": "🎨"},
    ]

def main():
    st.title("🤖 SaaSItIs - Multi-Agent Enterprise SaaS Consultant")
    st.markdown("*Transform your enterprise SaaS procurement with AI-powered agents*")
    
    # Create tabs
    tab1, tab2 = st.tabs(["🔍 AI Consultant", "🏪 Marketplace"])
    
    with tab1:
        # Initialize agents
        agents = initialize_agents()
        
        # Progress indicator
        progress_steps = ["Requirements", "Vendor Matching", "POC Evaluation", "Recommendations"]
        cols = st.columns(4)
        for i, step_name in enumerate(progress_steps):
            with cols[i]:
                if st.session_state.step > i + 1:
                    st.success(f"✅ {step_name}")
                elif st.session_state.step == i + 1:
                    st.info(f"🔄 {step_name}")
                else:
                    st.markdown(f"⏳ {step_name}")
        
        st.divider()
        
        # All the existing consultant workflow code goes here
        render_consultant_workflow(agents)
    
    with tab2:
        render_marketplace()

def render_consultant_workflow(agents):
    """Render the AI consultant workflow"""
    
    # Step 1: Requirements Gathering
    if st.session_state.step == 1:
        st.header("Step 1: Requirements Gathering")
        st.markdown("Provide detailed information about your SaaS needs and our AI will structure them into comprehensive requirements.")
        
        # Check if we should use sample data
        use_sample = st.session_state.get('use_sample_data', False)
        if use_sample:
            st.session_state.use_sample_data = False  # Reset flag
        
        # Organization Details
        st.subheader("🏢 Organization Details")
        col1, col2 = st.columns(2)
        with col1:
            company_size_options = ["1-50 employees", "51-200 employees", "201-1000 employees", "1001-5000 employees", "5000+ employees"]
            company_size = st.selectbox(
                "Company Size",
                company_size_options,
                index=2 if use_sample else 0
            )
            team_size = st.number_input("Team Size (users who will use this tool)", min_value=1, max_value=10000, value=150 if use_sample else 50)
        with col2:
            country_options = ["United States", "United Kingdom", "Canada", "Germany", "France", "India", "Australia", "Singapore", "Other"]
            country = st.selectbox(
                "Primary Country of Operations",
                country_options,
                index=0 if use_sample else 0
            )
            industry_options = ["Technology", "Finance", "Healthcare", "E-commerce", "Manufacturing", "Education", "Media", "Other"]
            industry = st.selectbox(
                "Industry",
                industry_options,
                index=0 if use_sample else 0
            )
        
        # Requirements Details
        st.subheader("📋 Requirements Details")
        sample_requirements = """We need AI infrastructure tools to support our machine learning and data science teams. Our primary needs include:

1. AI model development and training capabilities
2. Data labeling and annotation for computer vision projects  
3. Integration with our existing ML stack (TensorFlow, PyTorch, Python)
4. Enterprise-grade API access for model deployment
5. Strong data privacy and security controls

We're building customer-facing AI features and need tools that can scale with our growing team of 40 data scientists and ML engineers. Must support both cloud deployment (AWS, GCP) and meet SOC2 and GDPR compliance requirements."""

        user_input = st.text_area(
            "Describe your SaaS requirements:",
            value=sample_requirements if use_sample else "",
            placeholder="Example: We need an observability platform that integrates with our GitHub workflow, provides <2s latency monitoring, and meets SOC2 compliance requirements...",
            height=120
        )
        
        col3, col4 = st.columns(2)
        with col3:
            use_case_options = ["Development & DevOps", "Customer Support", "Sales & CRM", "Marketing", "Analytics", "Collaboration", "Security", "HR Management", "Finance & Accounting", "Other"]
            use_case = st.multiselect(
                "Primary Use Case",
                use_case_options,
                default=["Development & DevOps", "Analytics"] if use_sample else []
            )
            compliance_options = ["SOC2", "ISO 27001", "GDPR", "HIPAA", "PCI DSS", "FedRAMP", "None"]
            compliance_requirements = st.multiselect(
                "Compliance Requirements",
                compliance_options,
                default=["SOC2", "GDPR"] if use_sample else []
            )
        with col4:
            integrations_needed = st.text_input(
                "Required Integrations (comma-separated)",
                value="Python, TensorFlow, PyTorch, AWS, GCP, REST API" if use_sample else "",
                placeholder="e.g., GitHub, Slack, Salesforce, AWS"
            )
            priority_options = ["Critical - Immediate Need", "High - Within 1 month", "Medium - Within 3 months", "Low - Exploratory"]
            priority = st.selectbox(
                "Priority Level",
                priority_options,
                index=1 if use_sample else 0
            )
        
        # Budget & Timeline
        st.subheader("💰 Budget & Timeline")
        col5, col6 = st.columns(2)
        with col5:
            budget_options = ["< $10K", "$10K - $50K", "$50K - $100K", "$100K - $250K", "$250K - $500K", "$500K+", "Not Yet Determined"]
            budget_range = st.selectbox(
                "Annual Budget Range",
                budget_options,
                index=3 if use_sample else 0
            )
            time_options = ["1-2 weeks", "2-4 weeks", "1-2 months", "2-3 months", "3-6 months", "6+ months"]
            max_time_to_decision = st.selectbox(
                "Maximum Time to Find Right Fit",
                time_options,
                index=2 if use_sample else 0
            )
        with col6:
            deployment_options = ["Cloud (SaaS)", "On-Premise", "Hybrid", "No Preference"]
            deployment_preference = st.selectbox(
                "Deployment Preference",
                deployment_options,
                index=0 if use_sample else 0
            )
            support_options = ["24/7 Enterprise Support", "Business Hours Support", "Community Support", "Self-Service"]
            support_level = st.selectbox(
                "Required Support Level",
                support_options,
                index=0 if use_sample else 0
            )
        
        # Additional Context
        st.subheader("📝 Additional Context")
        sample_pain_points = """Current challenges:
- Manual data labeling is time-consuming and inconsistent
- Difficulty scaling ML model training across our team
- Need better tools for model versioning and deployment
- Lack of standardized workflows for AI development
- Security concerns with current open-source solutions"""

        sample_success = """Success metrics:
- Reduce data labeling time by 60%
- Improve model training efficiency by 40%
- Deploy 3+ new AI features per quarter
- Maintain 99.9% API uptime for production models
- Full SOC2 compliance within 6 months"""

        pain_points = st.text_area(
            "Current Pain Points (What problems are you trying to solve?)",
            value=sample_pain_points if use_sample else "",
            placeholder="e.g., Manual processes taking too long, lack of visibility, integration issues...",
            height=80
        )
        
        success_criteria = st.text_area(
            "Success Criteria (How will you measure success?)",
            value=sample_success if use_sample else "",
            placeholder="e.g., 50% reduction in deployment time, 99.9% uptime, improved team collaboration...",
            height=80
        )
        
        st.divider()
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🔍 Analyze Requirements", type="primary"):
                if user_input:
                    # Compile all inputs into structured format
                    detailed_requirements = {
                        "organization": {
                            "company_size": company_size,
                            "team_size": team_size,
                            "country": country,
                            "industry": industry
                        },
                        "requirements": {
                            "description": user_input,
                            "use_case": use_case,
                            "integrations": integrations_needed,
                            "compliance": compliance_requirements,
                            "priority": priority
                        },
                        "budget_timeline": {
                            "budget_range": budget_range,
                            "max_time_to_decision": max_time_to_decision,
                            "deployment_preference": deployment_preference,
                            "support_level": support_level
                        },
                        "additional_context": {
                            "pain_points": pain_points,
                            "success_criteria": success_criteria
                        }
                    }
                    
                    with st.spinner("AI is analyzing your detailed requirements..."):
                        # Create comprehensive input for the agent
                        full_input = f"""
                        Organization Details:
                        - Company Size: {company_size}
                        - Team Size: {team_size} users
                        - Country: {country}
                        - Industry: {industry}
                        
                        Requirements:
                        {user_input}
                        
                        Use Cases: {', '.join(use_case) if use_case else 'Not specified'}
                        Required Integrations: {integrations_needed}
                        Compliance Requirements: {', '.join(compliance_requirements) if compliance_requirements else 'None'}
                        Priority: {priority}
                        
                        Budget & Timeline:
                        - Budget Range: {budget_range}
                        - Time to Decision: {max_time_to_decision}
                        - Deployment: {deployment_preference}
                        - Support Level: {support_level}
                        
                        Pain Points: {pain_points}
                        Success Criteria: {success_criteria}
                        """
                        
                        # Gather requirements
                        requirements = agents['requirements'].gather_requirements(full_input)
                        requirements['detailed_input'] = detailed_requirements
                        st.session_state.requirements = requirements
                        
                        # Generate RFP
                        rfp = agents['requirements'].generate_rfp(requirements)
                        st.session_state.rfp = rfp
                        
                        st.session_state.step = 2
                        st.rerun()
                else:
                    st.error("Please describe your requirements first.")
        
        # Show example
        with st.expander("💡 Load Sample Data"):
            if st.button("📝 Fill Form with Sample Data"):
                # This will trigger a rerun with sample data
                st.session_state.use_sample_data = True
                st.rerun()
            
            st.markdown("""
            **Sample Scenario:** Enterprise looking for AI infrastructure tools for machine learning workflows
            
            **Organization:** 201-1000 employees tech company in United States
            **Use Case:** AI/ML model development and deployment
            **Budget:** $100K - $250K annually
            **Timeline:** Need solution within 1-2 months
            """)
    
    # Step 2: Vendor Matching
    elif st.session_state.step == 2:
        st.header("Step 2: Vendor Matching & Analysis")
        
        if st.session_state.requirements:
            # Show structured requirements
            with st.expander("📋 Structured Requirements"):
                st.json(st.session_state.requirements)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🎯 Find Matching Vendors", type="primary"):
                    with st.spinner("AI is analyzing vendor database..."):
                        # For demo, show Coactive AI and Cohere as top matches
                        demo_vendors = {
                            "top_matches": [
                                {
                                    "name": "Coactive AI",
                                    "category": "AI Infrastructure",
                                    "description": "Data labeling software",
                                    "fit_score": 92,
                                    "strengths": ["AI-powered data labeling", "Computer vision support", "Model training optimization"],
                                    "integrations": ["Python", "TensorFlow", "PyTorch", "AWS", "GCP"],
                                    "compliance": ["SOC2", "GDPR"],
                                    "pricing_model": "Usage-based",
                                    "adoption_score": 88,
                                    "funding": "$44M",
                                    "year_founded": 2021,
                                    "location": "San Jose, United States",
                                    "icon": "🏷️",
                                    "website": "https://coactive.ai",
                                    "pros": [
                                        "Excellent for training ML models with high-quality labeled data",
                                        "Strong computer vision capabilities",
                                        "Scales well for enterprise needs"
                                    ],
                                    "cons": [
                                        "Relatively new (founded 2021)",
                                        "Smaller funding compared to competitors"
                                    ]
                                },
                                {
                                    "name": "Cohere",
                                    "category": "AI Infrastructure",
                                    "description": "AI model developer",
                                    "fit_score": 95,
                                    "strengths": ["Enterprise LLMs", "Customizable models", "Privacy-focused"],
                                    "integrations": ["REST API", "Python SDK", "AWS", "Azure", "GCP"],
                                    "compliance": ["SOC2", "GDPR", "HIPAA"],
                                    "pricing_model": "API-based",
                                    "adoption_score": 90,
                                    "funding": "$1B",
                                    "year_founded": 2019,
                                    "location": "Toronto, Canada",
                                    "icon": "🧠",
                                    "website": "https://cohere.com",
                                    "pros": [
                                        "Industry-leading enterprise LLM capabilities",
                                        "Strong focus on data privacy and security",
                                        "Well-funded with proven track record",
                                        "Excellent HIPAA compliance"
                                    ],
                                    "cons": [
                                        "Higher pricing for premium features",
                                        "Based in Canada (may affect data residency)"
                                    ]
                                }
                            ],
                            "reasoning": "Based on your requirements for AI infrastructure, these two vendors offer the best combination of enterprise readiness, compliance, and proven technology."
                        }
                        st.session_state.vendors = demo_vendors
                        st.session_state.step = 3
                        st.rerun()
            
            with col2:
                if st.button("⬅️ Back to Requirements"):
                    st.session_state.step = 1
                    st.rerun()
        else:
            st.error("No requirements found. Please go back to Step 1.")
    
    # Step 3: POC Evaluation
    elif st.session_state.step == 3:
        st.header("Step 3: Top Vendor Matches")
        
        if st.session_state.vendors:
            # Display matched vendors in beautiful cards
            st.markdown("### 🎯 AI-Recommended Vendors")
            st.markdown(st.session_state.vendors.get('reasoning', ''))
            st.divider()
            
            # Display vendor cards
            vendors = st.session_state.vendors.get('top_matches', [])
            cols = st.columns(2)
            
            for idx, vendor in enumerate(vendors):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #3b82f6;
                        border-radius: 16px;
                        padding: 24px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                        margin-bottom: 20px;
                    ">
                        <div style="font-size: 64px; text-align: center; margin-bottom: 16px;">
                            {vendor['icon']}
                        </div>
                        <h2 style="text-align: center; margin: 12px 0; color: white;">
                            {vendor['name']}
                        </h2>
                        <p style="text-align: center; font-size: 16px; margin: 12px 0; opacity: 0.9;">
                            {vendor['description']}
                        </p>
                        <div style="text-align: center; margin: 16px 0;">
                            <span style="
                                background: rgba(255,255,255,0.3);
                                padding: 8px 20px;
                                border-radius: 20px;
                                font-size: 20px;
                                font-weight: bold;
                            ">Fit Score: {vendor['fit_score']}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Website link button
                    if 'website' in vendor:
                        st.link_button(f"🌐 Visit {vendor['name']} Website", vendor['website'], use_container_width=True)
                    
                    # Details
                    with st.expander(f"📊 {vendor['name']} Details"):
                        st.markdown(f"**🌐 Website:** [{vendor.get('website', 'N/A')}]({vendor.get('website', '#')})")
                        st.markdown(f"**📍 Location:** {vendor['location']}")
                        st.markdown(f"**💰 Funding:** {vendor['funding']}")
                        st.markdown(f"**📅 Founded:** {vendor['year_founded']}")
                        st.markdown(f"**💳 Pricing:** {vendor['pricing_model']}")
                        
                        st.markdown("**✅ Strengths:**")
                        for strength in vendor['strengths']:
                            st.markdown(f"  - {strength}")
                        
                        st.markdown("**🔌 Integrations:**")
                        st.markdown(f"  {', '.join(vendor['integrations'])}")
                        
                        st.markdown("**🔒 Compliance:**")
                        st.markdown(f"  {', '.join(vendor['compliance'])}")
                        
                        st.markdown("**👍 Pros:**")
                        for pro in vendor['pros']:
                            st.markdown(f"  - {pro}")
                        
                        st.markdown("**👎 Cons:**")
                        for con in vendor['cons']:
                            st.markdown(f"  - {con}")
            
            st.divider()
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("📊 Create POC Rubric", type="primary"):
                    with st.spinner("Creating custom evaluation rubric..."):
                        rubric = agents['poc_evaluation'].create_poc_rubric(
                            st.session_state.requirements, 
                            st.session_state.vendors
                        )
                        st.session_state.poc_rubric = rubric
                        
                        # Simulate evaluations for demo
                        evaluations = {}
                        for vendor in vendors:
                            evaluations[vendor['name']] = agents['poc_evaluation'].simulate_poc_evaluation(
                                rubric, vendor['name']
                            )
                        st.session_state.evaluations = evaluations
                        st.session_state.step = 4
                        st.rerun()
            
            with col2:
                if st.button("⬅️ Back to Requirements"):
                    st.session_state.step = 1
                    st.rerun()
        else:
            st.error("No vendor matches found. Please go back to Step 2.")
    
    # Step 4: Final Recommendations
    elif st.session_state.step == 4:
        st.header("Step 4: Final Recommendations")
        
        if st.session_state.evaluations:
            # Show POC rubric
            with st.expander("📏 POC Evaluation Rubric"):
                st.json(st.session_state.poc_rubric)
            
            # Show evaluations
            with st.expander("📈 POC Evaluation Results"):
                st.json(st.session_state.evaluations)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🎯 Generate Final Report", type="primary"):
                    with st.spinner("Synthesizing final recommendations..."):
                        recommendation = agents['recommendation'].generate_final_recommendation(
                            st.session_state.requirements,
                            st.session_state.vendors,
                            st.session_state.evaluations
                        )
                        
                        # Display recommendation
                        st.success("✅ Analysis Complete!")
                        st.markdown("### 📊 Executive Recommendation Report")
                        st.markdown(recommendation)
                        
                        # Show confidence score
                        confidence = agents['recommendation'].calculate_confidence_score(
                            st.session_state.evaluations
                        )
                        
                        st.markdown("### 🎯 Decision Confidence")
                        col_conf1, col_conf2 = st.columns(2)
                        with col_conf1:
                            st.metric("Confidence Score", f"{confidence['confidence_score']}%")
                        with col_conf2:
                            st.metric("Confidence Level", confidence['confidence_level'])
            
            with col2:
                if st.button("🔄 Start New Analysis"):
                    # Reset session state
                    for key in ['step', 'requirements', 'vendors', 'poc_rubric', 'evaluations']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state.step = 1
                    st.rerun()
            
            with col3:
                if st.button("⬅️ Back to POC"):
                    st.session_state.step = 3
                    st.rerun()
        else:
            st.error("No evaluations found. Please go back to Step 3.")
    
    # Sidebar with info
    with st.sidebar:
        st.markdown("### 🤖 Multi-Agent System")
        st.markdown("""
        **Active Agents:**
        - 📝 Requirements Agent
        - 🎯 Vendor Matching Agent  
        - 📊 POC Evaluation Agent
        - 🎯 Recommendation Agent
        
        **Demo Features:**
        - Conversational requirement gathering
        - AI-powered vendor matching
        - Custom POC rubric generation
        - Multi-stakeholder evaluation
        - Confidence-scored recommendations
        """)
        
        st.markdown("### 🚀 Hackathon MVP")
        st.markdown("Built for Multi-Agent Hackathon 2025")
        
        if st.button("ℹ️ About SaaSItIs"):
            st.info("""
            SaaSItIs transforms enterprise SaaS procurement through:
            
            ✅ 70% faster vendor selection
            ✅ 50% higher implementation success  
            ✅ Structured, objective evaluations
            ✅ Multi-stakeholder coordination
            ✅ Data-driven confidence scoring
            """)

def render_marketplace():
    """Render the marketplace with all SaaS tools"""
    st.header("🏪 SaaS Marketplace")
    st.markdown("*Discover and explore top enterprise SaaS tools*")
    
    # Get marketplace data
    tools = get_marketplace_data()
    
    # Filters
    st.subheader("🔍 Filters")
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        # Get unique categories
        categories = sorted(list(set([tool['category'] for tool in tools])))
        selected_category = st.selectbox("Category", ["All"] + categories)
    
    with col_filter2:
        # Get unique countries
        countries = sorted(list(set([tool['country'] for tool in tools])))
        selected_country = st.selectbox("Country", ["All"] + countries)
    
    with col_filter3:
        # Search
        search_term = st.text_input("🔍 Search", placeholder="Search by name or description...")
    
    # Filter tools
    filtered_tools = tools
    if selected_category != "All":
        filtered_tools = [t for t in filtered_tools if t['category'] == selected_category]
    if selected_country != "All":
        filtered_tools = [t for t in filtered_tools if t['country'] == selected_country]
    if search_term:
        search_lower = search_term.lower()
        filtered_tools = [t for t in filtered_tools if search_lower in t['name'].lower() or search_lower in t['description'].lower()]
    
    # Stats
    st.markdown(f"**Showing {len(filtered_tools)} of {len(tools)} tools**")
    st.divider()
    
    # Display tools in grid layout (3 per row)
    for i in range(0, len(filtered_tools), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_tools):
                tool = filtered_tools[i + j]
                with cols[j]:
                    # Create app-store style card
                    st.markdown(f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 12px;
                        padding: 20px;
                        height: 280px;
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    ">
                        <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                            {tool['icon']}
                        </div>
                        <h3 style="text-align: center; margin: 10px 0; color: #1f2937;">
                            {tool['name']}
                        </h3>
                        <p style="text-align: center; color: #6b7280; font-size: 14px; margin: 8px 0;">
                            {tool['description']}
                        </p>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
                            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                                <span style="color: #6b7280; font-size: 12px;">💰 Funding:</span>
                                <span style="color: #1f2937; font-weight: bold; font-size: 12px;">{tool['funding']}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                                <span style="color: #6b7280; font-size: 12px;">📅 Founded:</span>
                                <span style="color: #1f2937; font-weight: bold; font-size: 12px;">{tool['year']}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                                <span style="color: #6b7280; font-size: 12px;">📍 Location:</span>
                                <span style="color: #1f2937; font-weight: bold; font-size: 12px;">{tool['city']}, {tool['country'][:2]}</span>
                            </div>
                            <div style="text-align: center; margin-top: 10px;">
                                <span style="
                                    background: #3b82f6;
                                    color: white;
                                    padding: 4px 12px;
                                    border-radius: 12px;
                                    font-size: 11px;
                                    font-weight: 500;
                                ">{tool['category']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add some spacing
                    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
