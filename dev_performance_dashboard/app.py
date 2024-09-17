import streamlit as st
import sys
import os
import subprocess
import threading
import time
import requests


# Adding the parent directory to the path to import the metrics and data_collection modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.calculator import get_metrics
from data_collection.github_api import fetch_data
from visualization.dashboard import run_dash_app, get_dash_url
from query_interface.nlp_processor import process_query

# Function to check if the Dash app is running
def is_dash_app_running(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Start the Dash app in a separate thread
def start_dash_app():
    run_dash_app()

# Start the Dash app thread
dash_thread = threading.Thread(target=start_dash_app)
dash_thread.start()

# Wait for the Dash app to start
time.sleep(5)

# Streamlit app title
st.title('GitHub Data Fetcher & Developer performance dashboard')

# Input field for GitHub access token
access_token = st.text_input('Enter your GitHub Access Token:', type='password')

# Button to fetch data
if st.button('Fetch Data'):
    if access_token:
        with st.spinner('Fetching data...'):
            try:
                user_data, repos_df, commits_df, pull_requests_df = fetch_data(access_token)

                st.subheader('User Data')
                if user_data.get('avatar_url'):
                    st.image(user_data['avatar_url'], width=150)
                st.markdown(f"**Name:** {user_data.get('name', 'N/A')}")
                st.markdown(f"**Login:** {user_data.get('login', 'N/A')}")
                st.markdown(f"**Bio:** {user_data.get('bio', 'N/A')}")
                st.markdown(f"**Email:** {user_data.get('email', 'N/A')}")
                st.markdown(f"**Location:** {user_data.get('location', 'N/A')}")
                st.markdown(f"**Company:** {user_data.get('company', 'N/A')}")
                st.markdown(f"**Blog:** {user_data.get('blog', 'N/A')}")
                st.markdown(f"**Followers:** {user_data.get('followers', 'N/A')}")
                st.markdown(f"**Following:** {user_data.get('following', 'N/A')}")
                st.markdown(f"**Public Repositories:** {user_data.get('public_repos', 'N/A')}")
                st.markdown(f"**Public Gists:** {user_data.get('public_gists', 'N/A')}")
                st.markdown(f"**Account Created At:** {user_data.get('created_at', 'N/A')}")
                st.markdown(f"**Last Updated At:** {user_data.get('updated_at', 'N/A')}")

                st.subheader('Repositories Data')
                st.write(repos_df)

                st.subheader('Commits Data')
                st.write(commits_df)

                st.subheader('Pull Requests Data')
                st.write(pull_requests_df)

                with st.spinner('Calculating metrics...'):
                    try:
                        result = subprocess.run(['python', 'metrics/calculator.py'], capture_output=True, text=True)
                        if result.returncode == 0:
                            st.success("Metrics have been calculated successfully.")
                        else:
                            st.error(f"Error in calculations script:\n{result.stderr}")
                    except Exception as e:
                        st.error(f"An error occurred while running the calculations script:\n{str(e)}")

                st.subheader('Development Performance Dashboard')
                if is_dash_app_running(get_dash_url()):
                    st.markdown(f'<iframe src="{get_dash_url()}" width="100%" height="800px" frameborder="0"></iframe>', unsafe_allow_html=True)
                else:
                    st.error("Dash app is not running. Please check the logs for errors.")

            except Exception as e:
                st.error(f"An error occurred while fetching data:\n{str(e)}")
    else:
        st.error('Please enter a valid GitHub Access Token.')

# Add a section for processing queries
st.subheader('Query Processor')

query = st.text_input('Enter your query (e.g., "Show me the daily commits for John Doe"):')
if st.button('Process Query'):
    if query:
        with st.spinner('Processing query...'):
            figure = process_query(query)
            if figure:
                st.plotly_chart(figure)  # Display the Plotly chart
            else:
                st.error("No data available for the specified query.")
    else:
        st.error("Please enter a query.")
