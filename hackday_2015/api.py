import sys
import urllib
import json
from datetime import date, timedelta

inputJson = "{\"location\":[{\"type\":\"country\",\"country\":\"US\",\"state\":\"\",\"city\":\"\"}],\"topic\":[\"barack obama\",\"politics\"], \"dateBack\": {\"unit\": \"hours\", \"quantity\": 24}}" #sys.argv[1]
#inputJson = sys.argv[1]
inputs = json.loads(inputJson)

inputLocation = inputs['location']
inputTopic = inputs['topic']

inputLocationArray = []
for location in inputLocation:
    if location['country']:
        inputLocationArray.append(location['country'])
    elif location['state']:
        inputLocationArray.append(location['state'])
    elif location['city']:
        inputLocationArray.append(location['city'])

#create topic string
inputTopic = [urllib.quote(topic) for topic in inputTopic]
inputTopicString = ','.join(inputTopic)

#just add the location as another topic, it's the same thing to the upstream source api for now
if len(inputLocationArray) > 0:
    inputTopicString = inputTopicString + ',' + ','.join(inputLocationArray)

gUrl = ('https://ajax.googleapis.com/ajax/services/search/news?' +
        'v=1.0&q=' + inputTopicString)

response = urllib.urlopen(gUrl)
body = response.read()
gArticleResponse = json.loads(body)

articles = []
for gArticle in gArticleResponse['responseData']['results']:
    title = gArticle['titleNoFormatting']
    description = gArticle['content']
    geo = { 'coords': { 'lat': '', 'lng': ''}, 'location': {'country': '', 'state': '', 'city': ''}}
    publishDate = gArticle['publishedDate']
    url = gArticle['unescapedUrl']
    try:
        imageUrl = gArticle['image']['url']
    except KeyError:
        imageUrl = ''

    topics = inputTopic
    source = 'Google News'

    articles.append({'title': title, 'description': description, 'geo': geo, 'publishDate': publishDate, 'url': url, 'imageUrl': imageUrl, 'topics': topics, 'source': source})

articles = {"articles": articles}

print(json.dumps(articles))

#print(json.dumps(inputJson))

sys.stdout.flush()