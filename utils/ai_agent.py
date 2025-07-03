from openai import OpenAI
from serpapi import GoogleSearch
import os
from typing import Dict, List, Any
import json
import datetime

class AmazonStrategyAgent:
    def __init__(self, openai_api_key: str, serpapi_key: str):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.serpapi_key = serpapi_key
        
        # Report templates for different analysis types
        self.report_templates = {
            "competition": {
                "title": "🏆 Competitive Analysis Report",
                "sections": ["Market Position", "Competitor Strengths/Weaknesses", "Competitive Gaps", "Strategic Recommendations"]
            },
            "advertising": {
                "title": "📢 Amazon Advertising Strategy Report", 
                "sections": ["Current Ad Landscape", "Opportunity Analysis", "Budget Allocation", "Campaign Recommendations"]
            },
            "trends": {
                "title": "📈 Market Trends Analysis",
                "sections": ["Emerging Trends", "Consumer Behavior", "Market Opportunities", "Strategic Positioning"]
            },
            "pricing": {
                "title": "💰 Pricing Strategy Report",
                "sections": ["Price Analysis", "Competitive Pricing", "Value Positioning", "Pricing Recommendations"]
            },
            "reviews": {
                "title": "⭐ Customer Sentiment Analysis",
                "sections": ["Review Analysis", "Customer Pain Points", "Satisfaction Drivers", "Improvement Areas"]
            },
            "general": {
                "title": "📊 Amazon Strategy Analysis",
                "sections": ["Market Overview", "Key Insights", "Strategic Opportunities", "Action Plan"]
            }
        }
    
    def search_amazon_data(self, query: str, search_type: str = "general") -> List[Dict]:
        """Enhanced search with more targeted queries"""
        search_queries = {
            "general": f"Amazon {query} 2024",
            "competition": f"Amazon top sellers {query} competitors",
            "trends": f"Amazon marketplace trends {query} 2024",
            "advertising": f"Amazon PPC advertising strategy {query}",
            "reviews": f"Amazon customer reviews {query} analysis",
            "pricing": f"Amazon pricing strategy {query} market"
        }
        
        search_query = search_queries.get(search_type, f"Amazon {query}")
        
        params = {
            "q": search_query,
            "api_key": self.serpapi_key,
            "num": 8,  # Get more results
            "hl": "en",
            "gl": "us"
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            search_results = []
            if "organic_results" in results:
                for result in results["organic_results"][:6]:
                    search_results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "source": result.get("displayed_link", result.get("source", ""))
                    })
            
            return search_results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def analyze_strategy_question(self, question: str) -> Dict[str, Any]:
        """Fixed question analysis with better categorization"""
        prompt = f"""
        Analyze this Amazon strategy question and choose the SINGLE best category.
        
        Question: {question}
        
        Choose ONE category:
        - competition (for competitor analysis, market leaders)
        - advertising (for Amazon ads, PPC strategies)  
        - trends (for market trends, consumer behavior)
        - pricing (for pricing strategies, price analysis)
        - reviews (for customer feedback, reviews)
        - general (for broad strategy questions)
        
        Return only valid JSON with ONE category chosen:
        {{
            "category": "competition",
            "search_terms": ["supplement brands", "Amazon competitors", "market leaders"],
            "focus_areas": ["competitive analysis", "market positioning", "differentiation"],
            "analysis_type": "competitive landscape analysis",
            "key_questions": ["Who are the top competitors?", "What are their strengths?", "Where are the gaps?"]
        }}
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        try:
            analysis = json.loads(response.choices[0].message.content)
            # Validate category
            valid_categories = ["competition", "advertising", "trends", "pricing", "reviews", "general"]
            if analysis.get("category") not in valid_categories:
                analysis["category"] = "general"
            return analysis
        except:
            return {
                "category": "general",
                "search_terms": [question],
                "focus_areas": ["market analysis", "opportunities", "strategy"],
                "analysis_type": "General Amazon strategy analysis",
                "key_questions": [question]
            }
    
    def generate_enhanced_report(self, question: str, search_results: List[Dict], analysis: Dict, template_type: str) -> str:
        """Generate enhanced report using templates"""
        
        template = self.report_templates.get(template_type, self.report_templates["general"])
        
        # Prepare comprehensive search data
        search_summary = ""
        for i, result in enumerate(search_results[:4], 1):  # Limit to top 4 results
            if result['snippet']:
                search_summary += f"\n**Source {i}:** {result['title']}\n{result['snippet']}\n*From: {result['source']}*\n"
        
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""
        You are a senior Amazon strategy consultant. Create a comprehensive, professional strategy report.
        
        REPORT TYPE: {template['title']}
        DATE: {current_date}
        CLIENT QUESTION: {question}
        
        ANALYSIS FRAMEWORK: {analysis.get('analysis_type', 'Strategic analysis')}
        KEY FOCUS AREAS: {', '.join(analysis.get('focus_areas', []))}
        
        MARKET RESEARCH DATA:
        {search_summary}
        
        Create a detailed report with these sections:
        
        # {template['title']}
        *Generated on {current_date}*
        
        ## 🎯 EXECUTIVE SUMMARY
        • [Key insight 1 - most important finding]
        • [Key insight 2 - critical opportunity or challenge]  
        • [Key insight 3 - strategic implication]
        
        ## 🔍 {template['sections'][0].upper()}
        [Detailed analysis of first focus area with specific data points]
        
        ## 📊 {template['sections'][1].upper()}
        [Second major section with actionable insights]
        
        ## 💡 {template['sections'][2].upper()}
        [Third section focusing on opportunities and strategies]
        
        ## 🚀 {template['sections'][3].upper()}
        1. **Immediate Actions (Next 30 days)**
           - [Specific action item]
           - [Specific action item]
        
        2. **Strategic Initiatives (Next 90 days)**
           - [Strategic initiative]
           - [Strategic initiative]
        
        3. **Long-term Strategy (6+ months)**
           - [Long-term strategic direction]
           - [Long-term strategic direction]
        
        ## 📈 KEY METRICS TO TRACK
        • [Specific metric 1]
        • [Specific metric 2]
        • [Specific metric 3]
        
        ## ⚠️ POTENTIAL RISKS & MITIGATION
        • **Risk:** [Potential challenge] | **Mitigation:** [How to address]
        • **Risk:** [Potential challenge] | **Mitigation:** [How to address]
        
        Use specific data from the research. Be actionable and strategic. Focus on Amazon marketplace dynamics.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def research_and_analyze(self, question: str, research_depth: str = "Deep Dive") -> Dict[str, Any]:
        """Enhanced research workflow with depth options"""
        
        # Step 1: Analyze the question
        analysis = self.analyze_strategy_question(question)
        
        # Determine number of searches based on depth
        search_counts = {
            "Quick Analysis": 2,
            "Deep Dive": 3, 
            "Comprehensive Report": 4
        }
        
        num_searches = search_counts.get(research_depth, 3)
        
        # Step 2: Perform multiple targeted searches
        all_search_results = []
        
        # Primary search
        primary_results = self.search_amazon_data(
            analysis['search_terms'][0] if analysis['search_terms'] else question,
            analysis['category']
        )
        all_search_results.extend(primary_results[:3])
        
        # Additional searches based on depth
        if num_searches >= 3 and len(analysis['search_terms']) > 1:
            secondary_results = self.search_amazon_data(
                analysis['search_terms'][1],
                "general"
            )
            all_search_results.extend(secondary_results[:2])
        
        if num_searches >= 4 and len(analysis['search_terms']) > 2:
            tertiary_results = self.search_amazon_data(
                analysis['search_terms'][2],
                analysis['category']
            )
            all_search_results.extend(tertiary_results[:2])
        
        # Step 3: Generate enhanced report
        report = self.generate_enhanced_report(
            question, 
            all_search_results, 
            analysis, 
            analysis['category']
        )
        
        return {
            "question": question,
            "analysis": analysis,
            "search_results": all_search_results,
            "report": report,
            "sources": [result['link'] for result in all_search_results if result['link']],
            "report_type": analysis['category'],
            "template_used": self.report_templates[analysis['category']]['title']
        }
