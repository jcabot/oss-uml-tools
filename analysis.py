import streamlit as st
import plotly.graph_objects as go

def analyze_repos_multiple_keywords(repos, keywords, category_name):
    """Analyze repositories for multiple keywords within a category"""
    matching_repos = []
    non_matching_repos = []
    
    for repo in repos:
        description = (repo.get('description', '') or '').lower()
        name = (repo.get('name', '') or '').lower()
        topics = [t.lower() for t in repo.get('topics', [])]
        
        # Check if any of the keywords match
        matches = any(
            (keyword in description if keyword != 'ai' else (' ai ' in description  or ' ai-' in description)) or
            (keyword in name if keyword != 'ai' else (' ai ' in name  or ' ai-' in name)) or
            any(keyword == topic.strip() for topic in topics)
            for keyword in keywords
        )
        
        if matches:
            matching_repos.append(repo)
        else:
            non_matching_repos.append(repo)
            
    return matching_repos, non_matching_repos

def display_analysis(repos, category):
    """Display pie chart and table for a specific category analysis"""
    # Define keyword sets for each category
    keyword_sets = {
        'nocode': ['nocode', 'no-code', 'no code'],
        'lowcode': ['lowcode', 'low code', 'low-code'],
        'ai': ['ai', 'artificial intelligence'],
        'plantuml': ['plantuml', 'plant uml', 'plant-uml'],
        'ocl': ['ocl', 'object-constraint-language', 'object constraint language']
    }
    
    
    # Filter out specific repos for modeling category
    repos_to_analyze = repos

    matching_repos, non_matching_repos = analyze_repos_multiple_keywords(
        repos_to_analyze, 
        keyword_sets[category], 
        category
    )
    
    fig = go.Figure(data=[go.Pie(
        labels=[f'Mentions {category}', f'No {category} mention'],
        values=[len(matching_repos), len(non_matching_repos)],
        hole=0.3,
        marker_colors=['#2ecc71', '#e74c3c']
    )])
    
    fig.update_layout(
        title=f'Distribution of UML tools mentioning also {category}',
        showlegend=True,
        width=700,
        height=500,
        annotations=[{
            'text': f'Total: {len(repos)}',
            'x': 0.5,
            'y': 0.5,
            'font_size': 20,
            'showarrow': False
        }]
    )
    
    st.plotly_chart(fig)
    
    if matching_repos:
        st.write(f"### UML Tools Mentioning '{category}'")
        data = [{
            'Name': repo['name'],
            'Description': repo.get('description', 'No description'),
            'Stars': repo.get('stargazers_count', 0)
        } for repo in matching_repos]
        st.table(data)
    else:
        st.write(f"No repositories found mentioning '{category}'") 