from django.urls import path

from flights.views import (
    RouteListCreateView,
    RouteDetailView,
    FlightListCreateView,
    FlightDetailView,
    FlightFeaturedView,
    BookCreateView,
    BookDetailView,
    BookListView,
)

urlpatterns = [
    path("route/", RouteListCreateView.as_view(), name="route-list"),
    path("route/<str:id>/", RouteDetailView.as_view(), name="route-detail"),
    path("flight/", FlightListCreateView.as_view(), name="flight-list"),
    path("flight/<str:id>/", FlightDetailView.as_view(), name="flight-detail"),
    path("featured/", FlightFeaturedView.as_view(), name="featured-flight"),
    path("book/", BookCreateView.as_view(), name="book-create"),
    path("book/list/", BookListView.as_view(), name="book-list"),
    path("book/<str:id>/", BookDetailView.as_view(), name="book-detail"),
]
