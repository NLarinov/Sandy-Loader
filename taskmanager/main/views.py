from django.shortcuts import render
from .forms import NameForm
from .selen import TestClass

# a = TestClass()
#

def index(request):
    global a
    req = str(request)
    form = NameForm(request.POST or None)
    if form.is_valid():
        with open('result.txt') as line:
            context = {'list': [(i[:i.find('link: ')] + i[i.find(' status:'):],
                                 i[i.find('link: ') + 6:i.find(', status:')]) for i in line.readlines()]}
            return render(request, 'main/index.html', context)

    if 'par' in req:
        link = req[req.index('par')+4:-2]
        a.easy_download(link, request)

    with open('result.txt') as line:
        context = {'list': [(i[:i.find('link: ')] + i[i.find(' status:'):],
                             i[i.find('link: ')+6:i.find(', status:')]) for i in line.readlines()]}
        return render(request, 'main/index.html', context)
