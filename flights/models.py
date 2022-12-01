from django.db import models
from users.abstracts import TimeStampedModel, UniversalIdModel


class Route(TimeStampedModel, UniversalIdModel):
    """
    Create routes for flights
    """

    name = models.CharField(max_length=400)
    start = models.CharField(max_length=400)
    end = models.CharField(max_length=400)

    class Meta:
        ordering = [
            "start",
            "end",
        ]


class Flight(TimeStampedModel, UniversalIdModel):
    name = models.CharField(max_length=400)
    status = models.BooleanField(default=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure = models.TimeField(auto_now=False, auto_now_add=False)
    arrival = models.TimeField(auto_now=False, auto_now_add=False)
    capacity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=400)
    price = models.FloatField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = [
            "name",
            "route",
            "capacity",
            "description",
            "featured",
            "departure",
            "arrival",
            "price",
        ]
