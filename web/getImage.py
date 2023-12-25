from bing_image_urls import bing_image_urls

def getImage(query: str):
    link = bing_image_urls(query, limit=1)
    if link:
        return link[0]
    else:
        return "Not found"
