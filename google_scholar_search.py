import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to search Google Scholar
def search_scholar(query, year_filter=None, num_results=None):
    url = f'https://scholar.google.com/scholar?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # Loop over all search results
    for item in soup.find_all('div', class_='gs_ri'):
        title = item.find('h3').text
        link = item.find('a')['href']
        snippet = item.find('div', class_='gs_rs').text

        # If year_filter is provided, filter results by year
        if year_filter and year_filter not in snippet:
            continue

        results.append({'title': title, 'link': link, 'snippet': snippet})

        # If num_results is provided, stop after the desired number of results
        if num_results and len(results) >= num_results:
            break
    
    return results

# Streamlit UI setup
st.title("Google Scholar Search")

# Input fields
query = st.text_input("Enter the research topic or name:")
year_filter = st.text_input("Enter the publication year to filter by (optional):")
num_results = st.number_input("Enter the number of search results to return (leave 0 for all)", min_value=0, step=1)

# If query is entered, perform the search
if query:
    # Perform the search with filters
    results = search_scholar(query, year_filter if year_filter else None, num_results if num_results > 0 else None)

    # Display the results
    if results:
        for result in results:
            st.subheader(result['title'])
            st.write(f"[Link to Paper]({result['link']})")
            st.write(f"**Snippet**: {result['snippet']}")
            st.markdown("---")
    else:
        st.write("No results found for the given query and filter.")
