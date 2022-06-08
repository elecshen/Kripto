from django.shortcuts import render
from django.http import HttpResponse

from .models import Patterns
from .pattern import parse_patterns


def index(request):
    return render(request, "index.html", {'articles': Patterns.objects.order_by("-datetime")})


def parse_channel(request):
    parse_patterns()
    return HttpResponse("Parsed!")
