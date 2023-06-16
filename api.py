import requests 

urls = 'https://tle.ivanstanojevic.me/api/tle/25544'
header = {
    'User-Agent': '...',
    'referer': 'https://...'
}

r = requests.get(url = urls, headers=header)
data = r.json()

satName = data['name']

line1 = data['line1']
line2 =  data['line2']

print(satName)
print(line1)
print(line2)
 