"""
Quick test script to verify the setup before running the full app
"""
import os
import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        from crewai import Agent, Task, Crew
        print("✅ CrewAI imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test if OpenAI API key is set"""
    print("\nTesting API key...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("\n📝 To set your API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n   Or create a .env file with:")
        print("   OPENAI_API_KEY=your-api-key-here")
        return False
    
    if api_key.startswith("sk-"):
        print(f"✅ OPENAI_API_KEY found (starts with: {api_key[:10]}...)")
        return True
    else:
        print("⚠️  OPENAI_API_KEY found but doesn't look valid (should start with 'sk-')")
        return False

def test_agent_files():
    """Test if all agent files exist"""
    print("\nTesting agent files...")
    
    agent_files = [
        "agents/__init__.py",
        "agents/requirements_agent.py",
        "agents/vendor_matching_agent.py",
        "agents/poc_evaluation_agent.py",
        "agents/recommendation_agent.py"
    ]
    
    all_exist = True
    for file_path in agent_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("SaaSItIs MVP Setup Verification")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("API Key", test_api_key()))
    results.append(("Agent Files", test_agent_files()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = all(result[1] for result in results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    if all_passed:
        print("\n🎉 All tests passed! Ready to run the app:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the app.")
        sys.exit(1)

if __name__ == "__main__":
    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📁 Loaded environment variables from .env file\n")
    except:
        pass
    
    main()
