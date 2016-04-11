from django.db import models
from artsearcher.artsearchmain import ArtSearcher
# Create your models here.



class ArtSearch:

    # this is the go-between for the client-side and the web scraper.
    def get_art(self, search_term):
        searcher = ArtSearcher()
        search_results = searcher.art_search(search_term)
        return search_results
