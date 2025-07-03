import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.ai_agent import AmazonStrategyAgent

# Load environment variables (works for both local and cloud)
load_dotenv()

# Initialize AI agent with Streamlit secrets fallback
try:
    # Try environment variables first, then Streamlit secrets
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY")
    
    agent = AmazonStrategyAgent(
        openai_api_key=openai_key,
        serpapi_key=serpapi_key
    )
    agent_ready = True
except Exception as e:
    agent_ready = False
    st.error(f"⚠️ Configuration Error: {e}")

# Page configuration
st.set_page_config(
    page_title="Amazon Strategy Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF9900 0%, #232F3E 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        text-align: center;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0;
        text-align: center;
    }
    .report-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #FF9900;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .success-banner {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with professional styling
st.markdown("""
<div class="main-header">
    <h1>🛒 Amazon Strategy Assistant</h1>
    <p>AI-Powered Market Research & Strategic Analysis for Amazon Brands</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced features
with st.sidebar:
    st.header("⚙️ Research Settings")
    
    research_depth = st.selectbox(
        "Analysis Depth",
        ["Quick Analysis", "Deep Dive", "Comprehensive Report"],
        index=1,
        help="Choose how thorough you want the research to be"
    )
    
    st.header("💡 Example Questions")
    example_questions = [
        "What are emerging Amazon advertising trends for supplement brands?",
        "How should skincare brands compete against top sellers on Amazon?", 
        "What's the pricing opportunity for eco-friendly products on Amazon?",
        "What are customers saying about protein powders on Amazon?",
        "How can I optimize my Amazon product listings for better conversion?"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"📝 Use Example {i+1}", key=f"example_{i}"):
            st.session_state.example_question = question
    
    st.header("📊 Features")
    st.write("✅ Real-time market research")
    st.write("✅ Competitive analysis")
    st.write("✅ Professional reports")
    st.write("✅ Downloadable insights")
    st.write("✅ Source citations")    
    st.header("📊 Features")
    st.write("✅ Real-time market research")
    st.write("✅ Competitive analysis")
    st.write("✅ Professional reports")
    st.write("✅ Downloadable insights")
    st.write("✅ Source citations")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Your Strategy Question")
    
    # Use example question if selected
    default_question = ""
    if 'example_question' in st.session_state:
        default_question = st.session_state.example_question
        del st.session_state.example_question
    
    question = st.text_area(
        "What Amazon strategy question would you like researched?",
        value=default_question,
        placeholder="e.g., What are the key competitive advantages for supplement brands on Amazon in 2024?",
        height=120,
        help="Be specific about your brand category, target market, or strategic focus"
    )

with col2:
    st.header("🎯 Quick Stats")
    
    # Display some metrics
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Reports Generated", "50+", "↗️ Growing")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Data Sources", "Real-time", "🔄 Live")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Analysis Type", research_depth, "⚡ Fast")
    st.markdown('</div>', unsafe_allow_html=True)

# Generate button with enhanced styling
if st.button("🔍 Generate Strategy Report", type="primary", use_container_width=True):
    if not question:
        st.error("⚠️ Please enter a strategy question to get started!")
    elif not agent_ready:
        st.error("🔧 System not ready. Please check your configuration.")
    else:
        # Enhanced progress tracking
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Analyze question
                status_text.markdown("🔍 **Analyzing your strategy question...**")
                progress_bar.progress(15)
                
                # Step 2: Research
                status_text.markdown("🌐 **Searching Amazon market data...**")
                progress_bar.progress(35)
                
                # Step 3: Generate report
                status_text.markdown("🧠 **Processing insights with AI...**")
                progress_bar.progress(65)
                
                # Main research workflow
                results = agent.research_and_analyze(question, research_depth)
                
                progress_bar.progress(85)
                status_text.markdown("📊 **Finalizing your report...**")
                
                # Clear progress indicators
                progress_bar.progress(100)
                status_text.markdown("✅ **Report complete!**")
                
                # Success banner
                st.markdown("""
                <div class="success-banner">
                    <strong>🎉 Analysis Complete!</strong> Your Amazon strategy report is ready below.
                </div>
                """, unsafe_allow_html=True)
                
                # Clear progress after a moment
                import time
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Display results with enhanced styling
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                
                # Report metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"📋 **Report Type:** {results.get('template_used', 'Analysis')}")
                with col2:
                    st.info(f"🔍 **Sources Found:** {len(results.get('sources', []))}")
                with col3:
                    st.info(f"⚙️ **Analysis Depth:** {research_depth}")
                
                # Main report
                st.markdown("## 📊 Your Amazon Strategy Report")
                st.markdown(results["report"])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Sources section with better formatting
                if results["sources"]:
                    st.markdown("## 📚 Research Sources")
                    for i, source in enumerate(results["sources"][:5], 1):
                        st.markdown(f"**{i}.** [View Source]({source})")
                
                # Enhanced download functionality
                report_with_sources = results["report"]
                if results["sources"]:
                    report_with_sources += "\n\n## Research Sources\n"
                    for i, source in enumerate(results["sources"][:5], 1):
                        report_with_sources += f"{i}. {source}\n"
                
                # Download section
                st.markdown("## 📥 Export Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📄 Download Report (Markdown)",
                        data=report_with_sources,
                        file_name=f"amazon_strategy_report_{question[:30].replace(' ', '_')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # Copy to clipboard functionality
                    st.code(report_with_sources[:200] + "...", language="markdown")
                    st.caption("💡 Copy the full report above to paste into your documents")
                
            except Exception as e:
                st.error(f"❌ **Error generating report:** {str(e)}")
                st.markdown("""
                **Troubleshooting tips:**
                - Check your internet connection
                - Verify API keys are configured correctly  
                - Try a simpler question to test the system
                - Contact support if the issue persists
                """)

# Footer with additional info
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔗 About**")
    st.markdown("Powered by OpenAI GPT-4 and real-time market research")

with col2:
    st.markdown("**⚡ Performance**")
    st.markdown(f"Analysis Depth: {research_depth}")

with col3:
    st.markdown("**🛡️ Data**")
    st.markdown("Real-time Amazon market data")

# Optional: Add analytics or feedback
if st.button("👍 This tool was helpful", key="feedback"):
    st.balloons()
    st.success("Thank you for the feedback! 🙏")
