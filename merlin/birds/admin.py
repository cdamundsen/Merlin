from django.contrib import admin
from birds.models import Family, Genus, Order, Species, Location, Event


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'families_count']
    list_filter = ['name',]
    search_fields = ['name',]
    prepopulated_fields = {'slug': ['name',]}
    ordering = ['name',]
    show_facets = admin.ShowFacets.ALWAYS

    def families_count(self, obj):
        return obj.families.count()


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'genuses_count']
    list_filter = ['name',]
    search_fields = ['name',]
    prepopulated_fields = {'slug': ['name',]}
    ordering = ['name',]
    show_facets = admin.ShowFacets.ALWAYS

    def genuses_count(self, obj):
        return obj.genuses.count()


@admin.register(Genus)
class GenusAdmin(admin.ModelAdmin):
    list_display = ['name', 'species_count']
    list_filter = ['name',]
    search_fields = ['name',]
    prepopulated_fields = {'slug': ['name',]}
    ordering = ['name',]
    show_facets = admin.ShowFacets.ALWAYS

    def species_count(self, obj):
        return obj.species.count()


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'genus_name', 'species', 'event_count', 'location_count']
    #list_filter = ['name', 'species', ]
    search_fields = ['name', 'genus_name', 'species']
    prepopulated_fields = {'slug': ['name',]}
    ordering = ['name',]

    def genus_name(self, obj):
        return obj.genus.name

    def event_count(self, obj):
        return obj.events.count()

    def location_count(self, obj):
        events = obj.events.all()
        return len(set([x.location for x in events.all()]))


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'events_count', 'unique_birds']
    list_filter = ['name',]
    serach_fields = ['name',]
    prepopulated_fields = {'slug': ['name',]}
    ordering = ['name',]

    def events_count(self, obj):
        return obj.events.count()

    def unique_birds(self, obj):
        events = obj.events.all()
        event_birds = [e.birds.all() for e in events]
        unique = set()
        for birds in event_birds:
            unique = unique.union(set([b.name for b in birds.all()]))
        return len(unique)




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['location', 'date', 'duration', 'species_count']
    list_filter = ['location', 'date', ]
    search_fields = ['location', 'date']
    prepopulated_fields = {'slug': ['location', 'date',]}
    ordering = ['location', 'date']
    show_facets = admin.ShowFacets.ALWAYS

    def species_count(self, obj):
        return obj.birds.count()

