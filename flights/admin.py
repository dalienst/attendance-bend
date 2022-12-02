from django.contrib import admin
from flights.models import Route, Flight, Book


class RouteAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "start",
        "end",
    ]
    list_filter = [
        "name",
    ]


admin.site.register(Route, RouteAdmin)


class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "route",
        "capacity",
        "status",
        "description",
        "featured",
        "departure",
        "arrival",
        "price",
    ]

    list_filter = [
        "name",
        "route",
        "status",
    ]


admin.site.register(Flight, FlightAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "contact",
        "email",
        "flight",
        "date",
    ]
    list_filter = [
        "date",
        "flight",
    ]

admin.site.register(Book, BookAdmin)
