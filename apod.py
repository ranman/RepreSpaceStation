import re
import urllib
from PIL import Image
import cStringIO
import requests
from requests_oauthlib import OAuth1Session

# This is the APOD index page
apodbaseurl = 'http://apod.nasa.gov/apod/{}'
# This is how we look for the image on the page
regex = r'a href="(image.*)"'
# You can adjust this but twitter only allows 800k uploads
imgsize = 900, 900
# This our twitter API endpoint for changing the background
twitter_endpoint = 'http://api.twitter.com/1/account/update_profile_background_image.json'


def get_apod_image():
    # grab the mainpage
    apodpage = urllib.urlopen(apodbaseurl.format('astropix.html')).read()
    # find image url
    apodurl = re.search(regex, apodpage).group(1)
    # open the image file
    imgfile = urllib.urlopen(apodbaseurl.format(apodurl))
    # parse it into memory (cStringIO is faster than StringIO)
    imgstr = cStringIO.StringIO(imgfile.read())
    img = Image.open(imgstr)
    img.convert("RGB")
    # resize preserving aspect ratio
    img.thumbnail(imgsize, Image.ANTIALIAS)
    # save it in the smallest size possible
    img.save("apod.png", "PNG", optimize=True)


def update_twitter():
    image = open('apod.png', 'rb')
    # create an oauth thingy called "client"
    response = client.post(twitter_endpoint, '', params={'tile': True},
                           files={'image': ('apod.png', image)})
    # lets print and return some info for troubleshooting
    print response.text
    return response

if __name__ == '__main__':
    get_apod_image()
    update_twitter()
