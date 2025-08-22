import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from typing import Dict, List

def create_impact_dashboard(recommendations: List[Dict]) -> go.Figure:
    """Create an impact dashboard visualization."""
    if not recommendations:
        return go.Figure()
    
    # Extract data for visualization
    activities = []
    personal_growth = []
    social_impact = []
    fulfillment = []
    overall_scores = []
    
    for rec in recommendations[:8]:  # Top 8 recommendations
        activity = rec['activity']
        activities.append(activity['name'][:20] + "..." if len(activity['name']) > 20 else activity['name'])
        personal_growth.append(activity.get('personal_growth_score', 5))
        social_impact.append(activity.get('social_impact_score', 5))
        fulfillment.append(activity.get('fulfillment_score', 5))
        overall_scores.append(rec['score'])
    
    # Create subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Recommendation Scores', 'Personal Growth Impact', 
                       'Social Impact', 'Personal Fulfillment'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Overall scores
    fig.add_trace(
        go.Bar(x=activities, y=overall_scores, name="Overall Score", 
               marker_color='rgb(26, 118, 255)'),
        row=1, col=1
    )
    
    # Personal growth
    fig.add_trace(
        go.Bar(x=activities, y=personal_growth, name="Personal Growth", 
               marker_color='rgb(55, 178, 77)'),
        row=1, col=2
    )
    
    # Social impact
    fig.add_trace(
        go.Bar(x=activities, y=social_impact, name="Social Impact", 
               marker_color='rgb(255, 153, 51)'),
        row=2, col=1
    )
    
    # Fulfillment
    fig.add_trace(
        go.Bar(x=activities, y=fulfillment, name="Fulfillment", 
               marker_color='rgb(255, 99, 132)'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Activity Impact Dashboard",
        title_x=0.5
    )
    
    # Update axes
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_yaxes(range=[0, 10], row=i, col=j)
            fig.update_xaxes(tickangle=45, row=i, col=j)
    
    return fig

def format_score_category(category: str) -> str:
    """Format score category names by replacing underscores with spaces and title casing."""
    return category.replace('_', ' ').title()

def create_score_breakdown_chart(recommendation: Dict) -> go.Figure:
    """Create a detailed score breakdown chart for a single recommendation."""
    breakdown = recommendation.get('score_breakdown', {})
    
    # Format category names
    categories = [format_score_category(cat) for cat in breakdown.keys()]
    scores = list(breakdown.values())
    
    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=f"Score Breakdown: {recommendation['activity']['name']}",
        xaxis_title="Score (0-10)",
        yaxis_title="Criteria",
        height=400,
        margin=dict(l=150)
    )
    
    return fig

def create_development_pathway_chart(pathway: Dict) -> go.Figure:
    """Create a development pathway visualization."""
    if not pathway or 'activity_sequence' not in pathway:
        return go.Figure()
    
    activities = []
    timelines = []
    colors = []
    
    color_map = {
        'immediate': 'rgb(255, 99, 132)',
        'short-term': 'rgb(255, 153, 51)',
        'medium-term': 'rgb(55, 178, 77)',
        'long-term': 'rgb(26, 118, 255)'
    }
    
    for i, activity_info in enumerate(pathway['activity_sequence']):
        activities.append(activity_info.get('activity', f'Activity {i+1}'))
        timeline = activity_info.get('timeline', 'unknown')
        timelines.append(timeline)
        
        # Assign color based on timeline
        color = color_map.get(timeline.lower(), 'rgb(128, 128, 128)')
        colors.append(color)
    
    fig = go.Figure(go.Bar(
        x=activities,
        y=list(range(len(activities), 0, -1)),  # Reverse order for timeline effect
        orientation='v',
        marker_color=colors,
        text=timelines,
        textposition='inside'
    ))
    
    fig.update_layout(
        title="Development Pathway Timeline",
        xaxis_title="Activities",
        yaxis_title="Sequence",
        height=400,
        xaxis_tickangle=45
    )
    
    return fig

def create_category_distribution_chart(activities: List[Dict]) -> go.Figure:
    """Create a pie chart showing activity category distribution."""
    if not activities:
        return go.Figure()
    
    categories = {}
    for activity in activities:
        category = activity.get('category', 'Other')
        categories[category] = categories.get(category, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(categories.keys()),
        values=list(categories.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Activity Categories Distribution",
        height=400
    )
    
    return fig

def format_recommendation_card(recommendation: Dict) -> str:
    """Format a recommendation as an HTML card."""
    activity = recommendation['activity']
    score = recommendation['score']
    reasoning = recommendation['reasoning']
    
    # Create skill badges
    skills = activity.get('skills_developed', [])
    skill_badges = " ".join([f"<span style='background-color: #e1f5fe; color: #0277bd; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin: 2px;'>{skill}</span>" for skill in skills[:4]])
    
    card_html = f"""
    <div style='border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background-color: #fafafa;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
            <h4 style='margin: 0; color: #1f4e79;'>{activity['name']}</h4>
            <span style='background-color: #4caf50; color: white; padding: 4px 12px; border-radius: 16px; font-weight: bold;'>
                {score:.1f}/10
            </span>
        </div>
        <p style='color: #666; font-size: 14px; margin: 4px 0;'><strong>Category:</strong> {activity.get('category', 'N/A')}</p>
        <p style='color: #333; margin: 8px 0;'>{activity.get('description', 'No description available.')}</p>
        <div style='margin: 8px 0;'>
            <strong>Skills Developed:</strong><br>
            {skill_badges}
        </div>
        <div style='margin: 8px 0; padding: 8px; background-color: #e8f5e8; border-radius: 4px;'>
            <strong>Why this is recommended for you:</strong><br>
            <em>{reasoning}</em>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-top: 8px;'>
            <span><strong>Time:</strong> {activity.get('time_commitment', 'N/A')}</span>
            <span><strong>Difficulty:</strong> {activity.get('difficulty_level', 1)}/5</span>
        </div>
    </div>
    """
    
    return card_html

def display_student_insights(insights: Dict):
    """Display student profile insights in Streamlit."""
    if not insights:
        st.warning("No insights available.")
        return
    
    profile_analysis = insights.get('profile_analysis', {})
    
    if profile_analysis:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Personality Traits")
            traits = profile_analysis.get('personality_traits', [])
            if traits:
                for trait in traits:
                    st.write(f"• {trait}")
            else:
                st.write("No specific traits identified.")
            
            st.subheader("🌟 Leadership Potential")
            leadership = profile_analysis.get('leadership_potential', 'medium')
            leadership_color = {'high': '🔥', 'medium': '⭐', 'low': '💫'}
            st.write(f"{leadership_color.get(leadership, '⭐')} {leadership.title()}")
        
        with col2:
            st.subheader("🚀 Development Areas")
            dev_areas = profile_analysis.get('development_areas', [])
            if dev_areas:
                for area in dev_areas:
                    st.write(f"• {area}")
            else:
                st.write("No specific development areas identified.")
            
            st.subheader("🤝 Collaboration Style")
            collab_style = profile_analysis.get('collaboration_style', 'balanced')
            st.write(collab_style)

def export_recommendations_to_csv(recommendations: List[Dict]) -> pd.DataFrame:
    """Export recommendations to a pandas DataFrame for CSV download."""
    data = []
    
    for rec in recommendations:
        activity = rec['activity']
        data.append({
            'Activity Name': activity['name'],
            'Category': activity.get('category', ''),
            'Description': activity.get('description', ''),
            'Recommendation Score': rec['score'],
            'Time Commitment': activity.get('time_commitment', ''),
            'Difficulty Level': activity.get('difficulty_level', 1),
            'Skills Developed': ', '.join(activity.get('skills_developed', [])),
            'Reasoning': rec.get('reasoning', '')
        })
    
    return pd.DataFrame(data)
