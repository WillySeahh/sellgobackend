from django.conf.urls import url
from sellgo import views

urlpatterns = [ 
    # URLS for Customers
    url(r'^api/customers$', views.customer_list), #/api/tutorials: GET, POST, DELETE
    url(r'^api/customers/(?P<pk>[0-9]+)$', views.customer_detail), #/api/tutorials/:id: GET, PUT, DELETE

    # URLs for CSV
    url(r'^api/csv/(?P<pk>[0-9]+)$', views.csv_list), #/api/tutorials: GET, POST, DELETE
]