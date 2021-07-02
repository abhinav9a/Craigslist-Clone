from .utils import scrapper
from django.conf.urls import url
from django.urls.conf import path
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Search

# Create your views here.

types = [
    ["ccc", "Community"],
    ["eee", "Events"],
    ["sss", "For Sale"],
    ["ggg", "Gigs"],
    ["hhh", "Housing"],
    ["jjj", "Jobs"],
    ["rrr", "Resumes"],
    ["bbb", "Services"],
]

locations = [
    ["auburn", "https://auburn.craigslist.org/"],
    ["birmingham", "https://birmingham.craigslist.org/"],
    ["dothan", "https://dothan.craigslist.org/"],
    ["mobile", "https://mobile.craigslist.org/"],
    ["montgomery", "https://montgomery.craigslist.org/"],
    ["tuscaloosa", "https://tuscaloosa.craigslist.org/"],
    ["los angeles", "https://losangeles.craigslist.org/"],
    ["mendocino county", "https://mendocino.craigslist.org/"],
    ["monterey bay", "https://monterey.craigslist.org/"],
    ["orange county", "https://orangecounty.craigslist.org/"],
    ["palm springs", "https://palmsprings.craigslist.org/"],
]


def index(request):
    return render(request, "index.html", {
        "types": types,
        "locations": locations,
    })


def search(request):
    search_query = request.POST.get("search")
    minPrice = request.POST.get("minPrice")
    maxPrice = request.POST.get("maxPrice")
    listing_type = request.POST.get("listingType")
    location = request.POST.get("location")

    if not Search.objects.all().filter(search=search_query):
        Search.objects.create(search=search_query)

    listings = scrapper(location, listing_type, search_query, minPrice, maxPrice)

    return render(request, "index.html", {
        "types": types,
        "locations": locations,
        "listings": listings
    })


def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        search_qs = Search.objects.filter(search__icontains=q)
        results = []
        print(q)
        for r in search_qs:
            results.append(r.search)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
