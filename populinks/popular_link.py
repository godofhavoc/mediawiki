import re
import requests
from .models import QueryLinks

def compute(url):
    pop_links =[]
    tot_links = {}
    title = 'Sachin_Tendulkar'

    for result in query({'prop': 'links', 'pllimit': 'max', 'titles': title}):
        pages = result['pages']
        for key, val in pages.items():
            links = val['links']

        for val2 in links:
            #link_pops = 0
            title2 = val2['title']
            title2 = title2.strip()
            title2 = title2.replace(" ", "_")
            pop_links.append(title2)

    for x in range(len(pop_links)):

        try:
            q = QueryLinks.objects.get(title=pop_links[x])
            tot_links[pop_links[x]] = q.count
        except:
            print(pop_links[x])
            for result in query(
                {'prop': 'linkshere', 'lhlimit': 'max', 'titles': pop_links[x]}
            ):
                pages = result['pages']
                for key, val in pages.items():
                    links = val['linkshere']
                    if pop_links[x] in tot_links:
                        tot_links[pop_links[x]] += len(links)
                    else:
                        tot_links[pop_links[x]] = len(links)
            q = QueryLinks(title=pop_links[x], count=tot_links[pop_links[x]])
            q.save()

    print(max(tot_links, key=lambda key: tot_links[key]))

def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    lastContinue = {'continue': ''}
    while True:
        req = request.copy()
        req.update(lastContinue)
        result = requests.get('http://en.wikipedia.org/w/api.php', params=req).json()
        if 'error' in result: raise Error(result['error'])
        if 'warnings' in result: print(result['warning'])
        if 'query' in result: yield result['query']
        if 'continue' not in result: break
        lastContinue = result['continue']
