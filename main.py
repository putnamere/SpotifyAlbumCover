import spotipy
from io import BytesIO
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
from PIL import Image
import requests

CLIENT_ID=""
CLIENT_SECRET=""

colors = []
lastUrl = ""

def isInRange(num1, num2, target):
    return abs(num1 - num2) <= target
    
def getImg(url):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    return img

def updateColors(url):
    global colors
    colors = []
    img = getImg(url=url)
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            curColors = [r, g, b]
            if len(colors) == 0:
                colors.append([r, g, b])
            else:
                count = 0
                for i in range(len(colors)):
                    cCount = 0
                    for c in range(len(colors[i])):
                        if not isInRange(num1=curColors[c], num2=colors[i][c], target=60):
                            cCount = cCount + 1
                    if cCount > 0:
                        count = count + 1
                if count == len(colors) and count > 0:
                    colors.append(curColors)
    print("Updated Colors!")
    imgSave = Image.new('RGB', (len(colors), 1), color='red')
    imgSavePixles = imgSave.load()
    for x in range(len(colors)):
        imgSavePixles[x, 0] = (colors[x][0], colors[x][1], colors[x][2])
    imgSave.save('colorPallete.png')






                

while True:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost/redirect",
                                                       scope="user-read-currently-playing"))
        while True:
            albumCoverUrl = sp.current_user_playing_track()["item"]["album"]["images"][2]["url"]
            if albumCoverUrl != lastUrl:
                lastUrl = albumCoverUrl
                updateColors(url=albumCoverUrl)
            sleep(2)


    except Exception as e:
        print(e)
        pass
