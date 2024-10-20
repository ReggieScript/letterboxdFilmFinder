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

            if watchlist_div:
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

                            # Extract the movie URL from the 'data-film-link' attribute
                            movie_url = div.get('data-target-link')

                            # Create full URL by adding the base part
                            full_url = f"https://www.example.com{movie_url}"

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
        with requests.Session() as s:
            download = s.get(self.watchlist_url, headers = self.headers, )
            decoded_content = download.content.decode('utf-8')
        #cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #my_list = list(cr)
        #print(my_list)
        #self.watchlist_df = pd.DataFrame(my_list[1:], columns=my_list[0])  # First row as headers
        self.html = decoded_content
        df = self.decode_html(self.html)
        print(df)


if __name__ == "__main__":
    user = UserInfo("reggieboo")
    user.get_watchlist()



