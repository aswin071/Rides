from django.urls import path
from .views import RideCreateView,RideDetailView,RideListView


urlpatterns =[

    path("create-ride/",RideCreateView .as_view(), name="create-ride"),
    path('rides/<int:ride_id>/', RideDetailView.as_view(), name="view-ride"),
    path("all-rides/",RideListView .as_view(), name="all-rides")
    
]