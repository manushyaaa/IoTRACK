from api import getTLE
from beyond.frames import create_station
from beyond.io.tle import Tle
from beyond.dates import Date, timedelta
import numpy as np

NORAD_ID = 25544
prefix = 'BPL'
latNS = 23.2599333
logEW = 77.4126149
MSL =  495.23
azims, elevs = [], []  

satData = Tle(getTLE(NORAD_ID)).orbit()
station = create_station(prefix, (latNS,  logEW, MSL))

for orb in station.visibility(satData, start=Date.now(), stop=timedelta(hours=24), step=timedelta(seconds=30), events=True):
    elev = np.degrees(orb.phi)
    # Radians are counterclockwise and azimuth is clockwise
    azim = np.degrees(-orb.theta) % 360

    # Archive for plotting
    azims.append(azim)
    # Matplotlib actually force 0 to be at the center of the polar plot,
    # so we trick it by inverting the values
    elevs.append(90 - elev)

    r = orb.r / 1000
    print("{event:7} {orb.date} {azim:7.2f} {elev:7.2f} {r:10.2f} {orb.r_dot:10.2f}".format(
        orb=orb, r=r, azim=azim, elev=elev, event=orb.event.info if orb.event is not None else ""
    ))

    if orb.event and orb.event.info.startswith("LOS"):
        # We stop at the end of the first pass
        print()
        break