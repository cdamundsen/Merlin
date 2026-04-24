from django.shortcuts import get_object_or_404, render
from .models import Event, Family, Genus, Location, Order, Species
import time
from sortedcontainers import SortedDict


def home(request):
    return render(request, 'base.html')


def order_list(request):
    return render(
        request,
        'birds/order_list.html',
        context={
            'title': "Orders",
            'things': Order.objects.all(),
        }
    )


def order_detail(request, order_slug):
    order = get_object_or_404(Order, slug=order_slug)
    families = order.families.all()
    return render(
        request,
        'birds/ofg_detail.html',
        context={
            'parent_title': 'Order',
            'parent': order,
            'children_title': 'Families',
            'children': families,
        }
    )


def family_detail(request, family_slug):
    family = get_object_or_404(Family, slug=family_slug)
    genuses = family.genuses.all()
    return render(
        request,
        'birds/ofg_detail.html',
        context={
            'parent_title': 'Family',
            'parent': family,
            'children_title': 'Genuses',
            'children': genuses,
        }
    )


def genus_detail(request, genus_slug):
    genus = get_object_or_404(Genus, slug=genus_slug)
    species = genus.species.all()
    return render(
        request,
        'birds/ofg_detail.html',
        context={
            'parent_title': 'Genus',
            'parent': genus,
            'children_title': 'Species',
            'children': species,
        }
    )


def species_detail(request, species_slug):
    species = get_object_or_404(Species, slug=species_slug)
    locations = sorted(list(set([(ev.location.name, ev.location) for ev in species.events.all()])))
    locations = [loc[1] for loc in locations]
    return render(
        request,
        'birds/species_detail.html',
        context={
            'species': species,
            'locations': locations,
        }
    )


def location_list(request):
    locations = Location.objects.all()
    return render(
        request,
        'birds/order_list.html',
        context={
            'title': 'Locations',
            'things': locations,
        }
    )


def location_detail(request, location_slug):
    location = get_object_or_404(Location, slug=location_slug)
    events = location.events.all()
    return render(
        request,
        'birds/location_detail.html',
        context={
            'location': location,
            'events': events,
        }
    )


def event_list(request, year=None, month=None):
    events = Event.objects.all()
    if not year and not month:
        year, month = time.localtime()[:2]
    this_month = []
    other_dates = SortedDict()

    for event in events:
        e_year = event.date.year
        e_month = event.date.month
        if e_year == year and e_month == month:
            this_month.append(event)
        else:
            if e_year not in other_dates:
                other_dates[e_year] = SortedDict()
            if e_month not in other_dates[e_year]:
                other_dates[e_year][e_month] = event.date.strftime("%B")

    return render(
        request,
        'birds/event_list.html',
        context={
            'this_month': this_month,
            'other_dates': other_dates,
        }
    )


def event_detail(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    return render(
        request,
        'birds/event_detail.html',
        context={
            'event': event,
        }
    )


def all_birds(request):
    all_species = Species.objects.all().order_by('genus__family__order', 'genus__family', 'genus', 'species')
    sp_dict = {}
    for bird in all_species:
        order = bird.genus.family.order
        family = bird.genus.family
        genus = bird.genus

        if order not in sp_dict:
            sp_dict[order] = {}
        if family not in sp_dict[order]:
            sp_dict[order][family] = {}
        if genus not in sp_dict[order][family]:
            sp_dict[order][family][genus] = []
        sp_dict[order][family][genus].append(bird)

    return render(
        request,
        'birds/all_birds.html',
        context={
            'all_birds': sp_dict,
        }
    )
