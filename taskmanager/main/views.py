from django.shortcuts import render
from .forms import NameForm
from .main import TestClass
import os


def index(request):
    your_link = ''
    req = str(request)
    form = NameForm(request.POST or None)
    if form.is_valid():
        your_link = form.cleaned_data.get("your_link")
    context = {'form': form, 'firstname': your_link}

    if 'par' in req:
        link = req[req.index('par')+4:-3]
        print(link, 'SUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
    #     a = TestClass()
    #
    #     def start(login):
    #         a.easy_download(login)
    #         if len(os.listdir('C:\Downloads')) == 0:
    #             a.full_download(login)
    #         print('ok')
    #
    #     start('https://pdf.11klasov.net/1825-starlight-5-zvezdnyy-angliyskiy-5-klass-baranova-km-duli-d-kopylova-vv-i-dr.html')

    return render(request, 'main/index.html', context)
