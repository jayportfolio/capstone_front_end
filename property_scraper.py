import requests
from bs4 import BeautifulSoup
import json


def get_subscribers(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html)

    # potential_model_list = response.css('script::text').extract()
    for script in soup("script"):
        each = script.extract().text
        if "window.PAGE_MODEL" in each:
            page_model = each
            break

    page_model_json = json.loads(page_model.strip().replace("window.PAGE_MODEL = ", ""))

    # text = soup.select('#rawCount')[0].text
    # return text

    propertyData = page_model_json['propertyData']
    analyticsInfo = page_model_json['analyticsInfo']

    return {
        'bedrooms': propertyData['bedrooms'],
        'bathrooms': propertyData['bathrooms'],
    }


# get_subscribers('https://socialblade.com/youtube/user/pewdiepie/realtime') #PewDiePie
get_subscribers('https://www.rightmove.co.uk/properties/126047489#/?channel=RES_BUY')

'80520035'
