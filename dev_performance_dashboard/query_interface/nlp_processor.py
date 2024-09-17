import plotly.graph_objs as go
import plotly.io as pio
from metrics.calculator import get_metrics

# Predefined list of time ranges
time_range_keywords = ["daily", "weekly", "monthly", "yearly"]

# Function to extract developers from the metrics data
def get_developer_list(metrics):
    developer_list = metrics['daily_commits']['Author Name'].unique().tolist()
    return developer_list

# Function to extract time range from the query
def extract_time_range(query):
    for keyword in time_range_keywords:
        if keyword in query.lower():
            return keyword
    return None

# Function to extract developer's name from the query
def extract_developer_name(query, developer_list):
    for developer in developer_list:
        if developer.lower() in query.lower():
            return developer
    return None

# Function to process the query and generate a Plotly figure
def process_query(query):
    metrics = get_metrics()  # Retrieve metrics data
    developer_list = get_developer_list(metrics)  # Update the developer list dynamically
    
    time_range = extract_time_range(query)
    selected_developer = extract_developer_name(query, developer_list)
    
    print(f"Extracted Time Range: {time_range}")
    print(f"Extracted Developer: {selected_developer}")
    
    if not time_range or not selected_developer:
        print("Invalid query. Please specify a valid developer and a time range.")
        return None
    
    time_range_mapping = {
        'daily': 'daily_commits',
        'weekly': 'weekly_commits',
        'monthly': 'monthly_commits',
        'yearly': 'yearly_commits'
    }
    
    if time_range not in time_range_mapping:
        print("Time range not recognized.")
        return None
    
    time_range_key = time_range_mapping[time_range]
    
    if selected_developer not in metrics[time_range_key]['Author Name'].unique():
        print(f"Developer '{selected_developer}' not found.")
        return None

    filtered_data = metrics[time_range_key][metrics[time_range_key]['Author Name'] == selected_developer]
    
    if time_range == 'daily':
        data = go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data['Commit Count'],
            mode='lines+markers',
            name='Daily Commits'
        )
        layout = go.Layout(
            title=f'Daily Commits for {selected_developer} Over Time',
            xaxis_title='Date',
            yaxis_title='Commit Count'
        )
    elif time_range == 'weekly':
        data = go.Scatter(
            x=filtered_data['Week'],
            y=filtered_data['Commit Count'],
            mode='lines+markers',
            name='Weekly Commits'
        )
        layout = go.Layout(
            title=f'Weekly Commits for {selected_developer} Over Time',
            xaxis_title='Week',
            yaxis_title='Commit Count'
        )
    elif time_range == 'monthly':
        data = go.Bar(
            x=filtered_data['Month'],
            y=filtered_data['Commit Count'],
            name='Monthly Commits'
        )
        layout = go.Layout(
            title=f'Monthly Commits for {selected_developer}',
            xaxis_title='Month',
            yaxis_title='Commit Count'
        )
    elif time_range == 'yearly':
        data = go.Bar(
            x=filtered_data['Year'],
            y=filtered_data['Commit Count'],
            name='Yearly Commits'
        )
        layout = go.Layout(
            title=f'Yearly Commits for {selected_developer}',
            xaxis_title='Year',
            yaxis_title='Commit Count'
        )
    else:
        print("Time range not recognized.")
        return None

    figure = {'data': [data], 'layout': layout}
    
    return figure
