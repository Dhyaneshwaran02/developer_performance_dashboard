import pandas as pd

# Load CSV data into DataFrames
def load_data():
    repos_df = pd.read_csv(r"C:\Users\KD\OneDrive\Desktop\cit\dev_performance_dashboard\data_collection\repos_info.csv")
    commits_df = pd.read_csv(r"C:\Users\KD\OneDrive\Desktop\cit\dev_performance_dashboard\data_collection\commits_info.csv")
    pull_request_df = pd.read_csv(r"C:\Users\KD\OneDrive\Desktop\cit\dev_performance_dashboard\data_collection\pull_requests_info.csv")
    
    return repos_df, commits_df, pull_request_df

# Calculate Commit Frequency per Developer
def calculate_commit_frequency(commits_df):
    commits_df['Date'] = pd.to_datetime(commits_df['Date'], errors='coerce')

    # Group by Author Name
    daily_commits = commits_df.groupby(['Author Name', commits_df['Date'].dt.date]).size().reset_index(name='Commit Count')
    weekly_commits = commits_df.groupby(['Author Name', commits_df['Date'].dt.year, commits_df['Date'].dt.isocalendar().week]).size().reset_index(name='Commit Count')
    weekly_commits.columns = ['Author Name', 'Year', 'Week', 'Commit Count']
    monthly_commits = commits_df.groupby(['Author Name', commits_df['Date'].dt.to_period('M')]).size().reset_index(name='Commit Count')
    monthly_commits['Year'] = monthly_commits['Date'].dt.year
    monthly_commits['Month'] = monthly_commits['Date'].dt.month
    monthly_commits.drop('Date', axis=1, inplace=True)
    yearly_commits = commits_df.groupby(['Author Name', commits_df['Date'].dt.year]).size().reset_index(name='Commit Count')
    yearly_commits.rename(columns={'Date': 'Year'}, inplace=True)

    return daily_commits, weekly_commits, monthly_commits, yearly_commits

# Calculate PR Merge Rate per Developer
def calculate_pr_merge_rate(pull_request_df):
    pull_request_df['Created At'] = pd.to_datetime(pull_request_df['Created At'], errors='coerce')
    pull_request_df['Merged At'] = pd.to_datetime(pull_request_df['Merged At'], errors='coerce')

    if pull_request_df['Created At'].dt.tz is None:
        pull_request_df['Created At'] = pull_request_df['Created At'].dt.tz_localize('UTC')
    else:
        pull_request_df['Created At'] = pull_request_df['Created At'].dt.tz_convert('UTC')

    if pull_request_df['Merged At'].dt.tz is None:
        pull_request_df['Merged At'] = pull_request_df['Merged At'].dt.tz_localize('UTC')
    else:
        pull_request_df['Merged At'] = pull_request_df['Merged At'].dt.tz_convert('UTC')

    merged_prs_df = pull_request_df.dropna(subset=['Merged At'])

    daily_pr_merge_rate = merged_prs_df.groupby(['Author Login', merged_prs_df['Merged At'].dt.date]).size().reset_index(name='PR Merge Count')
    weekly_pr_merge_rate = merged_prs_df.groupby(['Author Login', merged_prs_df['Merged At'].dt.year, merged_prs_df['Merged At'].dt.isocalendar().week]).size().reset_index(name='PR Merge Count')
    weekly_pr_merge_rate.columns = ['Author Login', 'Year', 'Week', 'PR Merge Count']
    monthly_pr_merge_rate = merged_prs_df.groupby(['Author Login', merged_prs_df['Merged At'].dt.to_period('M')]).size().reset_index(name='PR Merge Count')
    monthly_pr_merge_rate['Year'] = monthly_pr_merge_rate['Merged At'].dt.year
    monthly_pr_merge_rate['Month'] = monthly_pr_merge_rate['Merged At'].dt.month
    monthly_pr_merge_rate.drop('Merged At', axis=1, inplace=True)
    yearly_pr_merge_rate = merged_prs_df.groupby(['Author Login', merged_prs_df['Merged At'].dt.year]).size().reset_index(name='PR Merge Count')
    yearly_pr_merge_rate.rename(columns={'Merged At': 'Year'}, inplace=True)

    return daily_pr_merge_rate, weekly_pr_merge_rate, monthly_pr_merge_rate, yearly_pr_merge_rate

# Calculate Resolution Time per Pull Request
def calculate_pr_resolution_time(pull_request_df):
    pull_request_df['Created At'] = pd.to_datetime(pull_request_df['Created At'], errors='coerce')
    pull_request_df['Merged At'] = pd.to_datetime(pull_request_df['Merged At'], errors='coerce')

    if pull_request_df['Created At'].dt.tz is None:
        pull_request_df['Created At'] = pull_request_df['Created At'].dt.tz_localize('UTC')
    else:
        pull_request_df['Created At'] = pull_request_df['Created At'].dt.tz_convert('UTC')

    if pull_request_df['Merged At'].dt.tz is None:
        pull_request_df['Merged At'] = pull_request_df['Merged At'].dt.tz_localize('UTC')
    else:
        pull_request_df['Merged At'] = pull_request_df['Merged At'].dt.tz_convert('UTC')

    merged_pr_df = pull_request_df.dropna(subset=['Merged At'])

    merged_pr_df.loc[:, 'Resolution Time (days)'] = (merged_pr_df['Merged At'] - merged_pr_df['Created At']).dt.total_seconds() / (60 * 60 * 24)
    merged_pr_df.loc[:, 'Resolution Time (days)'] = merged_pr_df['Resolution Time (days)'].round(2)

    return merged_pr_df[['Author Login', 'Repo Name', 'PR Number', 'Title', 'Resolution Time (days)']]

# Function to get all metrics
def get_metrics():
    repos_df, commits_df, pull_request_df = load_data()
    daily_commits, weekly_commits, monthly_commits, yearly_commits = calculate_commit_frequency(commits_df)
    daily_pr_merge_rate, weekly_pr_merge_rate, monthly_pr_merge_rate, yearly_pr_merge_rate = calculate_pr_merge_rate(pull_request_df)
    pr_resolution_times = calculate_pr_resolution_time(pull_request_df)

    return {
        "daily_commits": daily_commits,
        "weekly_commits": weekly_commits,
        "monthly_commits": monthly_commits,
        "yearly_commits": yearly_commits,
        "daily_pr_merge_rate": daily_pr_merge_rate,
        "weekly_pr_merge_rate": weekly_pr_merge_rate,
        "monthly_pr_merge_rate": monthly_pr_merge_rate,
        "yearly_pr_merge_rate": yearly_pr_merge_rate,
        "pr_resolution_times": pr_resolution_times
    }

if __name__ == "__main__":
    metrics = get_metrics()
    for key, df in metrics.items():
        print(f"{key}:\n{df}\n")
