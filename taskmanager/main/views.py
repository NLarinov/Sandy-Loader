from django.shortcuts import render
from .forms import NameForm
from .selen import TestClass
import os


a = TestClass()


def index(request):
    global a
    your_link = ''
    req = str(request)
    form = NameForm(request.POST or None)
    if form.is_valid():
        your_link = form.cleaned_data.get("your_link")
    context = {'form': form, 'firstname': your_link}

    if 'par' in req:
        link = req[req.index('par')+4:-3]
        a.easy_download(link)

    return render(request, 'main/index.html', context)
