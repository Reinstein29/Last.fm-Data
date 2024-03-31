# This script uses https://www.last.fm/ data

import requests
import sys
from time import sleep
import csv
import os

def checkError(response):
    if response.status_code != 200: # 200 status code indicates successful response
        print(response.text)
        sys.exit()

def printProgress(num, totalPages):
    print(f"Processing the data... {str(num)}/{str(totalPages)}")


api_key = "" # Your API key
username = "" # Username 
limit = 800 # Number of tracks on each page (one page per request, max 1000 tracks per page)

url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&format=json&limit={limit}"

response = requests.get(url)

checkError(response)

# Total number of pages to be fetched  
totalPages = int(response.json()["recenttracks"]["@attr"]["totalPages"])


dirname = os.path.dirname(os.path.abspath(__file__))
csvfilename = os.path.join(dirname, f'{username}-Data.csv')


with open(csvfilename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Unix time", "Song mbid", "Song Name", "Album mbid", "Album Name", "Artist mbid", "Artist Name"])


    for i in reversed(range(1, totalPages + 1)):
        sleep(1) # Time between each API call. 

        urlPage = url + f"&page={i}"

        response = requests.get(urlPage)
        checkError(response)

        data = response.json()
        tracks = data["recenttracks"]["track"]
        try:
            for song in reversed(tracks):
                writer.writerow([song["date"]["uts"], song["mbid"], song["name"], song["album"]["mbid"], song["album"]["#text"], song["artist"]["mbid"], song["artist"]["#text"]])
        except: 
            print("Some error")
        # Prints progress in the beginning, end and per 10 pages (You can change the value)
        j = totalPages + 1 - i

        printProgress(j, totalPages)
        # if j == 1 or j == totalPages or j % 10 == 0:
        #     printProgress(j, totalPages)
    print("Done!")
