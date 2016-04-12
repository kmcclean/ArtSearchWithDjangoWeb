from django.shortcuts import render
from artsearchsiteapp.models import ArtSearch


# when the user does a search request, this gets the results and sends them to be rendered.
def post_results(request):
    search_term = request.GET.get('search_term')
    amaa_request = request.GET.get('amaa_check')
    mia_request = request.GET.get('mia_check')
    walker_request = request.GET.get('walker_check')

    print(amaa_request)
    print(mia_request)
    print(walker_request)
    print(search_term)

    art_search = ArtSearch()
    search_results = art_search.get_art(search_term)


    return render(request, 'artsearchsiteapp/results.html', {'art_list' : search_results})

# shos the main page.
def display_main_page(request):
    return render(request, 'artsearchsiteapp/main.html')
