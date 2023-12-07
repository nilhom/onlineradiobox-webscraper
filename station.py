import requests
import bs4
from datetime import datetime

from song import Song


# This gets an input string such as "07.12" and finds the year for it.
# It picks the year so the date is closest to the current date
def closest_year(input_date):
    current_date = datetime.now()
    input_date = datetime.strptime(input_date, "%d.%m")

    # Set the input date to the current, previous, and next year
    input_date_current_year = input_date.replace(year=current_date.year)
    input_date_previous_year = input_date.replace(year=current_date.year - 1)
    input_date_next_year = input_date.replace(year=current_date.year + 1)

    # Calculate the differences in days between the current date and all three options
    diff_current_year = abs((current_date - input_date_current_year).days)
    diff_previous_year = abs((current_date - input_date_previous_year).days)
    diff_next_year = abs((current_date - input_date_next_year).days)

    # Choose the year with the least difference
    min_diff = min(diff_current_year, diff_previous_year, diff_next_year)

    if min_diff == diff_current_year:
        return input_date_current_year.strftime("%Y")
    elif min_diff == diff_previous_year:
        return input_date_previous_year.strftime("%Y")
    else:
        return input_date_next_year.strftime("%Y")


# Represents a radio station
# url_name: example "classicrockflorida"
# direct_url: complete onlineradiobox url
class Station:
    def __init__(
            self,
            url_name,
            table_name=None,
            land="de",
            direct_url=None,
            custom_char_song_split=" - "
    ):

        self.urlName = url_name
        self.table_name = table_name

        if table_name is None:
            self.table_name = self.urlName

        self.land = land
        self.direct_url = direct_url

        if direct_url is None:
            self.direct_url = f"https://onlineradiobox.com/{self.land}/{self.urlName}/playlist/"

        self.customCharSongSplit = custom_char_song_split

    # This returns a list of all Songs that the website has listed the station has played
    # Web scraping function
    def get_songs(self):
        whole_list = []

        for day_num in range(1,7):
            try:
                r = requests.get(self.direct_url+str(day_num))
                soup = bs4.BeautifulSoup(r.text, 'lxml')

                # Getting the date with overhead
                date = soup.findAll("li", {"class": "active", "role": "menuitem"})

                # Removing overhead
                date = filter(lambda x: "<span>" in str(x) and "<b>" in str(x), date)
                date = str(str(list(date)[0]).split("</b>")[1].split("</span>")[0]).strip()
                date = f"{date}.{closest_year(date)}"

                for x in soup.findAll("tr"):
                    try:
                        time = x.findAll("td")[0].find("span").text
                        song_and_artist = x.findAll("td")[1].find("a").text.split(self.customCharSongSplit)
                        artist = ""
                        if len(song_and_artist) == 2:
                            artist, title = song_and_artist
                        else:
                            title = song_and_artist[0]
                        whole_list.append(Song(date, time, artist, title))
                    except:
                        pass
            except:
                pass
        return whole_list
