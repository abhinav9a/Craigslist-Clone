from bs4 import BeautifulSoup
import requests


def scrapper(base_url, type, query, minPrice, maxPrice):
    query = query.replace(" ", "%20")
    url = f"{base_url}search/{type}?query={query}&min_price={minPrice}&max_price={maxPrice}"
    BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"

    # print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("li", {"class": "result-row"})

    listings = []

    for result in results:
        listing_url = result.a["href"]
        time = result.find("time").text
        title = result.find("a", {"class": "result-title"}).text

        if result.find("span", {"class": "result-price"}):
            price = result.find("span", {"class": "result-price"}).text
        else:
            price = "N/A"

        # If nothing found for the search query then show the results for nearby location
        if result.find("span", {"class": "result-hood"}):
            neighbourhood = result.find("span", {"class": "result-hood"}).text
        elif result.find("span", {"class": "nearby"}):
            neighbourhood = result.find("span", {"class": "nearby"})["title"]
        else:
            neighbourhood = "N/A"

        try:
            image_id = result.a["data-ids"].split(":")[1].split(",")[0]
            image_url = BASE_IMAGE_URL.format(image_id)
        except:
            image_url = "https://craigslist.org/images/peace.jpg"
            

        listings.append({
            "url": listing_url,
            "time": time,
            "title": title,
            "price": price,
            "neighbourhood": neighbourhood,
            "image_url": image_url
        })

    return listings
