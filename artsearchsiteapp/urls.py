from django.conf.urls import url
from . import views

# This holds the URL patterns that are needed for each different url request.
urlpatterns = [
    url(r'^$', views.display_main_page, name='display_main_page'),
    url(r'results', views.post_results, name ='post_results')
]
