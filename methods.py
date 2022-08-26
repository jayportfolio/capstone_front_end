import requests, json
from bs4 import BeautifulSoup


def scrape_website_by_property_id(html):
    soup = BeautifulSoup(html)
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
    # return {
    #     'bedrooms': propertyData['bedrooms'],
    #     'bathrooms': propertyData['bathrooms'],
    # }
    bedrooms = propertyData['bedrooms']
    bathrooms = propertyData['bathrooms']
    # bathrooms = request.form['bathrooms']
    # if not title:
    #     title = 'default title'
    #
    # if not content:
    #     content = 'default content'
    # if not something_is_missing:
    #     messages.append({'title': title, 'content': content})
    #     return redirect(url_for('index'))
    return bathrooms, bedrooms
