from flights.models import Route, Flight
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RouteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )
    name = serializers.CharField(
        max_length=400,
        min_length=2,
        validators=[UniqueValidator(Route.objects.all())],
    )
    start = serializers.CharField(
        max_length=400,
        min_length=2,
    )
    end = serializers.CharField(
        max_length=400,
        min_length=2,
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "name",
            "start",
            "end",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


# write a validate function to prevent


class FlightSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )
    name = serializers.CharField(
        max_length=400,
        min_length=2,
        validators=[UniqueValidator(Flight.objects.all())],
    )
    status = serializers.BooleanField(default=False)
    route = serializers.SlugRelatedField(
        queryset=Route.objects.all(), slug_field="name"
    )
    departure = serializers.TimeField()
    arrival = serializers.TimeField()
    capacity = serializers.IntegerField()
    description = serializers.CharField(
        max_length=400,
        min_length=2,
    )
    price = serializers.FloatField(default=1)
    featured = serializers.BooleanField(default=False)

    class Meta:
        model = Flight
        fields = (
            "id",
            "name",
            "route",
            "capacity",
            "status",
            "description",
            "featured",
            "departure",
            "arrival",
            "price",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


# validate
