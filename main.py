import requests
from bs4 import BeautifulSoup
import random
from user_utils import UserInfo
import pandas as pd
import gradio as gr
    

def get_random_movie(usernames, genre, platform):
    """
    Fetches watchlists for each username, filters by genre and platform, 
    and selects a random movie to recommend.
    
    :param usernames: List of usernames
    :param genre: Selected genre
    :param platform: Selected streaming platform
    :return: Randomly selected movie or a message if no movie found
    """
    selected_movies = pd.DataFrame()
    
    # Iterate through each username and fetch watchlist
    for username in usernames:
        user = UserInfo(username)  # Assuming UserInfo takes a username and provides methods to get data
        watchlist = user.get_watchlist(genre= genre, platform = platform)  # Fetch user's watchlist (a list of movies)
        
        selected_movies = pd.concat([selected_movies, watchlist])
    
    # Check if we have any movies after filtering
    # if selected_movies:
        # Select a random movie from the filtered list
    selected_movie = selected_movies.sample(1)
    print(selected_movie)
    return f"Suggested Movie: {selected_movie['Movie Name']}"
    # else:
    #     return "No movies found matching your criteria."

def movie_suggestion_interface(usernames_input, genre_input, platform_input):
    usernames = [username.strip() for username in usernames_input.split(',')]  # Split usernames by comma
    return get_random_movie(usernames, genre_input, platform_input)

# Create Gradio inputs and outputs
with gr.Blocks() as demo:
    gr.Markdown("## Random Movie Suggestion")
    
    usernames_input = gr.Textbox(label="Usernames (comma-separated)", placeholder="Enter usernames")
    genre_input = gr.Dropdown(choices=["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"], label="Select Genre")
    platform_input = gr.Dropdown(choices=["Netflix", "Hulu", "Amazon Prime", "Disney+"], label="Select Streaming Platform")
    
    submit_btn = gr.Button("Get Movie Suggestion")
    
    output = gr.Textbox(label="Suggested Movie")
    
    submit_btn.click(movie_suggestion_interface, inputs=[usernames_input, genre_input, platform_input], outputs=output)

if __name__ == "__main__":
    # Launch Gradio interface
    demo.launch()
