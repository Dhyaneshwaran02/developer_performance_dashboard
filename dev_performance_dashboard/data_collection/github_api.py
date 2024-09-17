from github import Github
import pandas as pd
import requests
import os

def fetch_data(access_token):
    # Initialize Github object using the token
    g = Github(access_token)
    
    # Get the authenticated user's data
    user = g.get_user()
    
    # Collect all the user details into a dictionary
    user_data = {
        'avatar_url': user.avatar_url,
        'bio': user.bio,
        'blog': user.blog,
        'collaborators': user.collaborators,
        'company': user.company,
        'created_at': user.created_at,
        'disk_usage': user.disk_usage,
        'email': user.email,
        'followers': user.followers,
        'following': user.following,
        'location': user.location,
        'login': user.login,
        'name': user.name,
        'public_repos': user.public_repos,
        'public_gists': user.public_gists,
        'url': user.url,
        'updated_at': user.updated_at,
    }
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize an empty list to store repository data
    repos_data = []
    
    # Fetch all repositories of the authenticated user
    repos = user.get_repos()
    
    # Iterate over all repositories
    for repo in repos:
        # Get repository languages
        languages = repo.get_languages()
        languages_str = ', '.join(languages.keys())  # Convert languages to a comma-separated string
        
        # Get contributors
        contributors = repo.get_contributors()
        contributors_list = [contributor.login for contributor in contributors]
        contributors_str = ', '.join(contributors_list)  # Convert contributors to a comma-separated string
        
        # Create a dictionary for each repository
        repo_info = {
            'ID': repo.id,
            'Name': repo.name,
            'Description': repo.description or 'No description',
            'Created at': repo.created_at,
            'Updated at': repo.updated_at,
            'Owner Login': repo.owner.login,
            'License': repo.license.name if repo.license else 'None',
            'Has Wiki': repo.has_wiki,
            'Forks Count': repo.forks_count,
            'Open Issues Count': repo.open_issues_count,
            'Stargazers Count': repo.stargazers_count,
            'Watchers Count': repo.watchers_count,
            'Repository URL': repo.html_url,
            'Commits URL': repo.commits_url,
            'Languages URL': repo.languages_url,
            'Pulls URL': repo.pulls_url,
            'Languages': languages_str,  # Add languages to the repository info
            'Contributors': contributors_str  # Add contributors to the repository info
        }
        
        # Append the dictionary to the list
        repos_data.append(repo_info)
    
    # Convert the list of dictionaries into a DataFrame
    repos_df = pd.DataFrame(repos_data)
    
    # Save repository information to a CSV file
    repos_csv_path = os.path.join(script_dir, 'repos_info.csv')
    repos_df.to_csv(repos_csv_path, index=False)
    print(f"Repository information saved to '{repos_csv_path}'")
    
    # Initialize a list to store commit information
    commits_information = []
    
    # Set up headers for authentication
    headers = {'Authorization': f'token {access_token}'}
    
    # Iterate over the DataFrame to fetch commit information for each repository
    for i in range(repos_df.shape[0]):
        # Fetch the commits URL from the DataFrame
        url = repos_df.loc[i, 'Commits URL'].replace('{/sha}', '')
        page_no = 1
        
        while True:
            # Construct the URL with pagination
            paginated_url = f"{url}?page={page_no}"
            
            # Send GET request to fetch commit information with authentication
            response = requests.get(paginated_url, headers=headers)
            
            # Check if the response is successful
            if response.status_code != 200:
                print(f"Error fetching commits for {repos_df.loc[i, 'Name']}: {response.status_code}")
                break
            
            response_data = response.json()
            
            # Break the loop if no commits are found (end of pagination)
            if not response_data:
                break
            
            # Print the current URL and the number of commits fetched
            # print(f"URL: {paginated_url}, Commits Fetched: {len(response_data)}")
            
            # Iterate over the commits and extract the required information
            for commit in response_data:
                commit_data = [
                    repos_df.loc[i, 'ID'],                      # Repository ID
                    commit['sha'],                              # Commit SHA
                    commit['commit']['committer']['date'],      # Commit Date
                    commit['commit']['message'],                # Commit Message
                    commit['commit']['author']['name'],         # Commit Author Name
                    commit['commit']['author']['email']         # Commit Author Email
                ]
                commits_information.append(commit_data)
            
            # If the current page contains fewer than 30 commits, it means it's the last page
            if len(response_data) < 30:
                break
            
            # Move to the next page
            page_no += 1
    
    # Convert commit information to a DataFrame and save it to a CSV file
    commits_df = pd.DataFrame(commits_information, columns=['Repo Id', 'Commit Id', 'Date', 'Message', 'Author Name', 'Author Email'])
    commits_csv_path = os.path.join(script_dir, 'commits_info.csv')
    commits_df.to_csv(commits_csv_path, index=False)
    print(f"Commit information saved to '{commits_csv_path}'")
    
    # Initialize a list to store pull request information
    pull_requests_information = []
    
    # Iterate over the DataFrame to fetch pull request information for each repository
    for i in range(repos_df.shape[0]):
        # Fetch the pulls URL from the DataFrame
        url = repos_df.loc[i, 'Pulls URL'].replace('{/number}', '')
        page_no = 1
        
        while True:
            # Construct the URL with pagination
            paginated_url = f"{url}?state=all&page={page_no}"
            
            # Send GET request to fetch pull request information with authentication
            response = requests.get(paginated_url, headers=headers)
            
            # Check if the response is successful
            if response.status_code != 200:
                print(f"Error fetching pull requests for {repos_df.loc[i, 'Name']}: {response.status_code}")
                break
            
            response_data = response.json()
            
            # Break the loop if no pull requests are found (end of pagination)
            if not response_data:
                break
            
            # Print the current URL and the number of pull requests fetched
            # print(f"URL: {paginated_url}, Pull Requests Fetched: {len(response_data)}")
            
            # Iterate over the pull requests and extract the required information
            for pr in response_data:
                pr_data = [
                    repos_df.loc[i, 'Name'],        # Repo Name
                    pr['number'],                   # PR Number
                    pr['title'],                    # Title of the pull request
                    pr['user']['login'],            # Author Login
                    pr['state'],                    # State (open/closed)
                    pr['created_at'],               # Creation date
                    pr['updated_at'],               # Last update date
                    pr['merged_at'],                # Merged date
                    pr['issue_url'].split('/')[-1], # Issue Id (Extracting ID from the URL)
                    pr['user'].get('name', 'N/A'),  # PR Author Name, default to 'N/A' if not available
                    pr['user'].get('email', 'N/A')  # PR Author Email, default to 'N/A' if not available
                ]
                pull_requests_information.append(pr_data)
            
            # If the current page contains fewer than 30 pull requests, it means it's the last page
            if len(response_data) < 30:
                break
            
            # Move to the next page
            page_no += 1
    
    # Convert pull request information to a DataFrame and save it to a CSV file
    pull_requests_df = pd.DataFrame(pull_requests_information, columns=['Repo Name', 'PR Number', 'Title', 'Author Login', 'State', 'Created At', 'Updated At', 'Merged At', 'Issue Id', 'Author Name', 'Author Email'])
    pull_requests_csv_path = os.path.join(script_dir, 'pull_requests_info.csv')
    pull_requests_df.to_csv(pull_requests_csv_path, index=False)
    print(f"Pull request information saved to '{pull_requests_csv_path}'")
    
    return user_data, repos_df, commits_df, pull_requests_df
