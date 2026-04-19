import streamlit as st
import plotly.graph_objects as go


def analyze_repos_multiple_keywords(repos, keywords, category_name):
    """Analyze repositories for multiple keywords within a category"""
    matching_repos = []
    non_matching_repos = []

    for repo in repos:
        description = (repo.get("description", "") or "").lower()
        name = (repo.get("name", "") or "").lower()
        topics = [t.lower() for t in repo.get("topics", [])]

        matches = any(
            (
                keyword in description
                if keyword != "ai"
                else (" ai " in description or " ai-" in description)
            )
            or (
                keyword in name
                if keyword != "ai"
                else (" ai " in name or " ai-" in name)
            )
            or any(keyword == topic.strip() for topic in topics)
            for keyword in keywords
        )

        if matches:
            matching_repos.append(repo)
        else:
            non_matching_repos.append(repo)

    return matching_repos, non_matching_repos


def display_analysis(table_repos, category):
    """Pie chart + table for *category*. *table_repos* must match the main repository table."""
    keyword_sets = {
        "nocode": ["nocode", "no-code", "no code"],
        "lowcode": ["lowcode", "low code", "low-code"],
        "ai": ["ai", "artificial intelligence"],
        "plantuml": ["plantuml", "plant uml", "plant-uml"],
        "ocl": ["ocl", "object-constraint-language", "object constraint language"],
    }

    repos_to_analyze = table_repos

    allowed_urls = frozenset(
        r.get("html_url") for r in table_repos if r.get("html_url")
    )

    matching_repos, _non_matching_repos = analyze_repos_multiple_keywords(
        repos_to_analyze,
        keyword_sets[category],
        category,
    )

    matching_repos = [
        r for r in matching_repos if r.get("html_url") in allowed_urls
    ]
    n_match = len(matching_repos)
    n_non_match = len(repos_to_analyze) - n_match

    fig = go.Figure(
        data=[
            go.Pie(
                labels=[
                    f"Mentions {category}",
                    f"No {category} mention",
                ],
                values=[n_match, n_non_match],
                hole=0.3,
                marker_colors=["#2ecc71", "#e74c3c"],
            )
        ]
    )

    fig.update_layout(
        title=f"Distribution of UML tools mentioning also {category}",
        showlegend=True,
        width=700,
        height=500,
        annotations=[
            {
                "text": f"Total: {len(repos_to_analyze)}",
                "x": 0.5,
                "y": 0.5,
                "font_size": 20,
                "showarrow": False,
            }
        ],
    )

    st.plotly_chart(fig)

    if matching_repos:
        st.write(f"### UML Tools Mentioning '{category}'")
        data = [
            {
                "Name": repo["name"],
                "Description": repo.get("description", "No description"),
                "Stars": repo.get("stargazers_count", 0),
            }
            for repo in matching_repos
        ]
        st.table(data)
    else:
        st.write(f"No repositories found mentioning '{category}'")
