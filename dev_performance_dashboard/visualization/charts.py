import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Adding the parent directory to the path to import the metrics module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metrics.calculator import get_metrics

# Function to generate commit charts using Plotly
def generate_commit_charts(metrics):
    # Daily Commits
    daily_commits = metrics['daily_commits']
    fig = go.Figure()
    for developer in daily_commits['Author Name'].unique():
        developer_data = daily_commits[daily_commits['Author Name'] == developer]
        fig.add_trace(go.Scatter(x=developer_data['Date'], y=developer_data['Commit Count'],
                                 mode='lines+markers', name=developer))
    fig.update_layout(title='Daily Commits per Developer',
                      xaxis_title='Date',
                      yaxis_title='Commit Count',
                      xaxis_tickangle=-45)
    fig.write_html('daily_commits_chart.html')  # Save as HTML for interactivity

    # Weekly Commits
    weekly_commits = metrics['weekly_commits']
    fig = go.Figure()
    for developer in weekly_commits['Author Name'].unique():
        developer_data = weekly_commits[weekly_commits['Author Name'] == developer]
        fig.add_trace(go.Scatter(x=developer_data['Week'].astype(str) + '-' + developer_data['Year'].astype(str),
                                 y=developer_data['Commit Count'],
                                 mode='lines+markers', name=developer))
    fig.update_layout(title='Weekly Commits per Developer',
                      xaxis_title='Week-Year',
                      yaxis_title='Commit Count',
                      xaxis_tickangle=-45)
    fig.write_html('weekly_commits_chart.html')

    # Monthly Commits
    monthly_commits = metrics['monthly_commits']
    fig = go.Figure()
    for developer in monthly_commits['Author Name'].unique():
        developer_data = monthly_commits[monthly_commits['Author Name'] == developer]
        fig.add_trace(go.Bar(x=developer_data['Month'].astype(str) + '-' + developer_data['Year'].astype(str),
                             y=developer_data['Commit Count'],
                             name=developer))
    fig.update_layout(title='Monthly Commits per Developer',
                      xaxis_title='Month-Year',
                      yaxis_title='Commit Count',
                      xaxis_tickangle=-45)
    fig.write_html('monthly_commits_chart.html')

    # Yearly Commits
    yearly_commits = metrics['yearly_commits']
    fig = go.Figure()
    for developer in yearly_commits['Author Name'].unique():
        developer_data = yearly_commits[yearly_commits['Author Name'] == developer]
        fig.add_trace(go.Bar(x=developer_data['Year'],
                             y=developer_data['Commit Count'],
                             name=developer))
    fig.update_layout(title='Yearly Commits per Developer',
                      xaxis_title='Year',
                      yaxis_title='Commit Count')
    fig.write_html('yearly_commits_chart.html')

def generate_pr_charts(metrics):
    # Daily PR Merge Rate
    daily_pr_merge_rate = metrics['daily_pr_merge_rate']
    fig = go.Figure()
    for developer in daily_pr_merge_rate['Author Login'].unique():
        developer_data = daily_pr_merge_rate[daily_pr_merge_rate['Author Login'] == developer]
        fig.add_trace(go.Scatter(x=developer_data['Merged At'],
                                 y=developer_data['PR Merge Count'],
                                 mode='lines+markers', name=developer))
    fig.update_layout(title='Daily PR Merge Rates per Developer',
                      xaxis_title='Date',
                      yaxis_title='PR Merge Count',
                      xaxis_tickangle=-45)
    fig.write_html('daily_pr_merge_rate_chart.html')

    # Monthly PR Merge Rate
    monthly_pr_merge_rate = metrics['monthly_pr_merge_rate']
    fig = go.Figure()
    for developer in monthly_pr_merge_rate['Author Login'].unique():
        developer_data = monthly_pr_merge_rate[monthly_pr_merge_rate['Author Login'] == developer]
        fig.add_trace(go.Bar(x=developer_data['Month'].astype(str) + '-' + developer_data['Year'].astype(str),
                             y=developer_data['PR Merge Count'],
                             name=developer))
    fig.update_layout(title='Monthly PR Merge Rates per Developer',
                      xaxis_title='Month-Year',
                      yaxis_title='PR Merge Count',
                      xaxis_tickangle=-45)
    fig.write_html('monthly_pr_merge_rate_chart.html')

    # Yearly PR Merge Rate
    yearly_pr_merge_rate = metrics['yearly_pr_merge_rate']
    fig = go.Figure()
    for developer in yearly_pr_merge_rate['Author Login'].unique():
        developer_data = yearly_pr_merge_rate[yearly_pr_merge_rate['Author Login'] == developer]
        fig.add_trace(go.Bar(x=developer_data['Year'],
                             y=developer_data['PR Merge Count'],
                             name=developer))
    fig.update_layout(title='Yearly PR Merge Rates per Developer',
                      xaxis_title='Year',
                      yaxis_title='PR Merge Count')
    fig.write_html('yearly_pr_merge_rate_chart.html')

    # PR Resolution Time
    pr_resolution_times = metrics['pr_resolution_times']
    fig = go.Figure()
    for developer in pr_resolution_times['Author Login'].unique():
        developer_data = pr_resolution_times[pr_resolution_times['Author Login'] == developer]
        fig.add_trace(go.Box(y=developer_data['Resolution Time (days)'],
                             name=developer))
    fig.update_layout(title='PR Resolution Time per Developer',
                      yaxis_title='Resolution Time (days)')
    fig.write_html('pr_resolution_times_chart.html')

if __name__ == "__main__":
    metrics = get_metrics()
    generate_commit_charts(metrics)
    generate_pr_charts(metrics)
