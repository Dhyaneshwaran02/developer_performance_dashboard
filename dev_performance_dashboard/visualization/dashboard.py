from dash import dcc, html, Input, Output
import dash
import plotly.graph_objs as go
from metrics.calculator import get_metrics

# Fetch metrics using get_metrics function from calculator.py
metrics = get_metrics()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Development Performance Dashboard'),

    # Dropdown for selecting developer
    html.Div(children=[
        html.Label('Select Developer:'),
        dcc.Dropdown(
            id='developer-dropdown',
            options=[{'label': dev, 'value': dev} for dev in metrics['daily_commits']['Author Name'].unique()],
            value=metrics['daily_commits']['Author Name'].unique()[0]  # Default value
        )
    ]),

    # Daily Commits Graph
    html.Div(children=[
        html.H2('Daily Commits'),
        dcc.Graph(id='daily-commits-graph')
    ]),

    # Weekly Commits Graph
    html.Div(children=[
        html.H2('Weekly Commits'),
        dcc.Graph(id='weekly-commits-graph')
    ]),

    # Monthly Commits Graph
    html.Div(children=[
        html.H2('Monthly Commits'),
        dcc.Graph(id='monthly-commits-graph')
    ]),

    # Yearly Commits Graph
    html.Div(children=[
        html.H2('Yearly Commits'),
        dcc.Graph(id='yearly-commits-graph')
    ]),

    # PR Merge Rates Graph
    html.Div(children=[
        html.H2('PR Merge Rates'),
        dcc.Graph(id='pr-merge-rate-graph')
    ]),

    # PR Resolution Times Graph
    html.Div(children=[
        html.H2('PR Resolution Times'),
        dcc.Graph(id='pr-resolution-times-graph')
    ])
])

# Callback to update graphs based on selected developer
@app.callback(
    [
        Output('daily-commits-graph', 'figure'),
        Output('weekly-commits-graph', 'figure'),
        Output('monthly-commits-graph', 'figure'),
        Output('yearly-commits-graph', 'figure'),
        Output('pr-merge-rate-graph', 'figure'),
        Output('pr-resolution-times-graph', 'figure')
    ],
    [Input('developer-dropdown', 'value')]
)
def update_graphs(selected_developer):
    # Filter data based on selected developer
    daily_commits = metrics['daily_commits'][metrics['daily_commits']['Author Name'] == selected_developer]
    weekly_commits = metrics['weekly_commits'][metrics['weekly_commits']['Author Name'] == selected_developer]
    monthly_commits = metrics['monthly_commits'][metrics['monthly_commits']['Author Name'] == selected_developer]
    yearly_commits = metrics['yearly_commits'][metrics['yearly_commits']['Author Name'] == selected_developer]
    
    pr_merge_rate = {
        'daily': metrics['daily_pr_merge_rate'][metrics['daily_pr_merge_rate']['Author Login'] == selected_developer],
        'monthly': metrics['monthly_pr_merge_rate'][metrics['monthly_pr_merge_rate']['Author Login'] == selected_developer]
    }
    
    pr_resolution_times = metrics['pr_resolution_times'][metrics['pr_resolution_times']['Author Login'] == selected_developer]

    # Create figures
    daily_commits_fig = go.Figure()
    daily_commits_fig.add_trace(go.Scatter(
        x=daily_commits['Date'],
        y=daily_commits['Commit Count'],
        mode='lines+markers',
        name='Daily Commits'
    ))
    daily_commits_fig.update_layout(title='Daily Commits Over Time',
                                    xaxis={'title': 'Date'},
                                    yaxis={'title': 'Commit Count'},
                                    hovermode='closest')

    weekly_commits_fig = go.Figure()
    weekly_commits_fig.add_trace(go.Scatter(
        x=weekly_commits['Week'].astype(str) + '-' + weekly_commits['Year'].astype(str),
        y=weekly_commits['Commit Count'],
        mode='lines+markers',
        name='Weekly Commits'
    ))
    weekly_commits_fig.update_layout(title='Weekly Commits Over Time',
                                     xaxis={'title': 'Week-Year'},
                                     yaxis={'title': 'Commit Count'},
                                     hovermode='closest')

    monthly_commits_fig = go.Figure()
    monthly_commits_fig.add_trace(go.Bar(
        x=monthly_commits['Month'].astype(str) + '-' + monthly_commits['Year'].astype(str),
        y=monthly_commits['Commit Count'],
        name='Monthly Commits',
        marker={'color': 'green'}
    ))
    monthly_commits_fig.update_layout(title='Monthly Commits',
                                      xaxis={'title': 'Month-Year'},
                                      yaxis={'title': 'Commit Count'},
                                      hovermode='closest')

    yearly_commits_fig = go.Figure()
    yearly_commits_fig.add_trace(go.Bar(
        x=yearly_commits['Year'],
        y=yearly_commits['Commit Count'],
        name='Yearly Commits',
        marker={'color': 'purple'}
    ))
    yearly_commits_fig.update_layout(title='Yearly Commits',
                                     xaxis={'title': 'Year'},
                                     yaxis={'title': 'Commit Count'},
                                     hovermode='closest')

    pr_merge_rate_fig = go.Figure()
    pr_merge_rate_fig.add_trace(go.Scatter(
        x=pr_merge_rate['daily']['Merged At'],
        y=pr_merge_rate['daily']['PR Merge Count'],
        mode='lines+markers',
        name='Daily PR Merge Rate',
        marker={'color': 'red'}
    ))
    pr_merge_rate_fig.add_trace(go.Bar(
        x=pr_merge_rate['monthly']['Month'].astype(str) + '-' + pr_merge_rate['monthly']['Year'].astype(str),
        y=pr_merge_rate['monthly']['PR Merge Count'],
        name='Monthly PR Merge Rate',
        marker={'color': 'orange'}
    ))
    pr_merge_rate_fig.update_layout(title='PR Merge Rates',
                                    xaxis={'title': 'Date'},
                                    yaxis={'title': 'PR Merge Count'},
                                    hovermode='closest')

    pr_resolution_times_fig = go.Figure()
    pr_resolution_times_fig.add_trace(go.Bar(
        y=pr_resolution_times['Title'],
        x=pr_resolution_times['Resolution Time (days)'],
        orientation='h',
        name='PR Resolution Times',
        marker={'color': 'blue'}
    ))
    pr_resolution_times_fig.update_layout(title='PR Resolution Times',
                                          xaxis={'title': 'Resolution Time (days)'},
                                          yaxis={'title': 'PR Title'},
                                          hovermode='closest')

    return (
        daily_commits_fig,
        weekly_commits_fig,
        monthly_commits_fig,
        yearly_commits_fig,
        pr_merge_rate_fig,
        pr_resolution_times_fig
    )

def run_dash_app():
    # Start the Dash app server
    app.run_server(port=8051, debug=True, use_reloader=False)

def get_dash_url():
    # Return the URL for embedding
    return 'http://127.0.0.1:8051'

if __name__ == "__main__":
    run_dash_app()
