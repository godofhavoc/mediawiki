import re
import requests

def compute(url):
    link_pops = {}
    title = 'Sachin_Tendulkar'
    for result in query({'prop': 'links', 'pllimit': 'max', 'titles': title}):
        pages = result['pages']
        for key, val in pages.items():
            links = val['links']

        for val2 in links:
            val2['title'] = val2['title'].strip()
            val2['title'] = val2['title'].replace(" ", "_")
            for result2 in query({'prop': 'linkshere', 'lhlimit': 'max', 'titles': val2['title']}):
                pages2 = result2['pages']
                for key3, val3 in pages.items():
                    out_links = val3['links']

                if val2['title'] in link_pops.keys():
                    link_pops[val2['title']] += len(out_links)
                else:
                    link_pops[val2['title']] = len(out_links)

    return max(link_pops, key=lambda key: stats[key])

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
        return result['query']
