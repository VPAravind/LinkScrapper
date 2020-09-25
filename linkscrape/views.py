from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
import requests
from .models import Link


def scrape(request):
    if request.method == "POST":

        site = request.POST.get('site', '')

        if not (site.startswith('http://') or site.startswith('https://')):
            if not (site.startswith('www.')) :
                site = 'www.' + site
            site = 'https://'+site

        print(site)

        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = (link.get('href'))
            link_text = link.string
            if link_address is not '#':
                Link.objects.create(address=link_address, name=link_text)

        return HttpResponseRedirect('/')
    else:

        data = Link.objects.all()

        return render(request,'linkscrape/result.html', {'data':data})


def clear(request):
    Link.objects.all().delete()
    return render(request, 'linkscrape/result.html')