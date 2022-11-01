from django.shortcuts import render
from .forms import NameForm
from .main_copy import TestClass
import os


start = True


def index(request):
    global start
    your_link = ''

    form = NameForm(request.POST or None)
    if form.is_valid():
        your_link = form.cleaned_data.get("your_link")

    context = {'form': form, 'firstname': your_link}
    print(your_link)

    if start is False:
        a = TestClass()

        def start(login):
            a.easy_download(login)
            if len(os.listdir('C:\Downloads')) == 0:
                a.full_download(login)
            print('ok')

        start('https://pdf.11klasov.net/1825-starlight-5-zvezdnyy-angliyskiy-5-klass-baranova-km-duli-d-kopylova-vv-i-dr.html')

    start = False
    return render(request, 'main/index.html', context)
