from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from flights.serializers import (
    RouteSerializer,
    FlightSerializer,
    BookSerializer,
)
from flights.models import Route, Flight, Book


class RouteListCreateView(generics.ListCreateAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Route deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class FlightListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Flight deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class FlightFeaturedView(generics.ListAPIView):
    serializer_class = FlightSerializer
    
    def get_queryset(self):
        return Flight.objects.filter(featured=True)

class BookCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # permission_classes = [IsAdminUser,]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "id"
