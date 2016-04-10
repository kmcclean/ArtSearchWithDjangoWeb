from django.db import models
from artsearcher.artsearchmain import ArtSearcher
# Create your models here.


class ArtSearch:

    def get_art(self, search_term):
        searcher = ArtSearcher()
        search_results = searcher.art_search(search_term)
        return search_results
