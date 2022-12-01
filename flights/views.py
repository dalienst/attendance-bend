from rest_framework import generics, status
from rest_framework.response import Response

from flights.serializers import (
    RouteSerializer,
    FlightSerializer,
)
from flights.models import Route, Flight


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
