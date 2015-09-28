from django.shortcuts import render

import requests

from .forms import SubmitURL
from .popular_link import compute

def find_popular(request):

    if request.method == "POST":
        form = SubmitURL(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            pop_link = compute(url);
