import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import csv

class UserInfo:
    def __init__(self, username, url = "https://letterboxd.com/"):
        self.username = username
        self.url = url
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        # Add other headers if necessary
                        }
                        

    def decode_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find the specific div with id="content"
        content_div = soup.find('div', id='content')
        if content_div:
            # Find the div with class="cols-2 js-watchlist-content" inside content_div
            watchlist_div = content_div.find('div', class_='cols-2 js-watchlist-content')
            for wl_div in watchlist_div:

                if wl_div:
                    #print(watchlist)
                    # Find the section with class="section col-17 col-main js-watchlist-main-content"
                    section = watchlist_div.find('section', class_=lambda x: x and 'js-watchlist-main-content' in x.split())
                        
                    if section:
                        # Find the ul element with class="poster-list.-grid.-constrained.-p125"
                        ul = section.find('ul', class_=lambda x: x and 'poster-list' in x)

                        if ul:
                            # Find all the div elements containing the movie information inside the ul
                            movie_divs = ul.find_all('li', class_=lambda x: x and 'poster-container' in x)

                            if movie_divs:
                                print(f"Found {len(movie_divs)} movie divs")
                            # Create lists to store movie names and URLs
                            movie_names = []
                            movie_urls = []

                            # Loop through each movie div and extract the data
                            for div in movie_divs:
                                #print(div)
                                # Extract the movie name from the 'data-film-name' attribute
                                actual_div = div.find("div", class_=lambda x: x and 'film-poster' in x)
                                print(actual_div)
                                movie_name = actual_div.find("img", class_="image").get("alt")


                                # Create full URL by adding the base part
                                full_url = f"https://letterboxd.com/film/{movie_name.replace(' ', '-').lower()}"

                                # Append the extracted data to the lists
                                movie_names.append(movie_name)
                                movie_urls.append(full_url)

                            # Create a DataFrame from the lists
                            df = pd.DataFrame({
                                'Movie Name': movie_names,
                                'Movie URL': movie_urls
                            })

                            return df
                        else:
                            print("No ul with class 'poster-list.-grid.-constrained.-p125' found.")
                    else:
                        print("No section with class 'section col-17 col-main js-watchlist-main-content' found.")
                else:
                    print("No div with class 'cols-2 js-watchlist-content' found.")
            else:
                print("No div with id 'content' found.")

            return pd.DataFrame()

    def get_watchlist(self, genre = ""):
        if genre == "":
            self.watchlist_url = f"https://letterboxd.com/{self.username}/watchlist/"
        else:
            self.watchlist_url = f"https://letterboxd.com/{self.username}/watchlist/genre/{genre}/"
        page = 2
        full_df = pd.DataFrame()
        new_page = self.watchlist_url
        while True:
            with requests.Session() as s:
                download = s.get(new_page, headers = self.headers)
                decoded_content = download.content.decode('utf-8')
                print("truena aqui")
            self.html = decoded_content
            df = self.decode_html(decoded_content)
            if len(df) < 1:
                break
            #print(df)
            full_df = pd.concat([full_df, df], axis = 0)
            new_page = f"{self.watchlist_url}/page/{page}/"
            page = page + 1
            #print(df)
            print(f"running through pages, currently in page {page}")
        print(full_df)
        return full_df


if __name__ == "__main__":
    user = UserInfo("reggieboo")
    user.get_watchlist()



