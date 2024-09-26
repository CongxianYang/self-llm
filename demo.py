import requests
response_image = requests.get("https://m.media-amazon.com/images/G/28/AS/AGS/images/news/240812/4.webp")
with open('news.jpg', 'wb') as f:
    f.write(response_image.content)