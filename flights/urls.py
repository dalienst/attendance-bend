from django.urls import path

from flights.views import (
    RouteListCreateView,
    RouteDetailView,
    FlightListCreateView,
    FlightDetailView,
)

urlpatterns = [
    path("route/", RouteListCreateView.as_view(), name="route-list"),
    path("route/<str:id>/", RouteDetailView.as_view(), name="route-detail"),
    path("flight/", FlightListCreateView.as_view(), name="flight-list"),
    path("flight/<str:id>/", FlightDetailView.as_view(), name="flight-detail"),
]
