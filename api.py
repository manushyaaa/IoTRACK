import requests 

urls = 'https://tle.ivanstanojevic.me/api/tle/25544'
header = {
    'User-Agent': '...',
    'referer': 'https://...'
}

r = requests.get(url = urls, headers=header)
data = r.json()
print(data)