import requests 
from textwrap import dedent

def getTLE(NORAD_ID):
    try : 
        urls = f'https://tle.ivanstanojevic.me/api/tle/{NORAD_ID}'
        header = {
            'User-Agent': '...',
            'referer': 'https://...'
        }

        r = requests.get(url=urls, headers=header)

        data = r.json()

        tle1 = """{satname}
{line1}
{line2}""".format(satname=data['name'], line1=data['line1'], line2=data['line2'].strip())


        print(tle1)
        return tle1
    except Exception as e : 
        print("TLE Error encountered : " , e)
  