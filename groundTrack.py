
import sys
import numpy as np
import matplotlib.pyplot as plt

from beyond.dates import Date, timedelta
from beyond.io.tle import Tle
from beyond.frames import create_station
from beyond.config import config


tle = Tle("""ISS (ZARYA)
1 25544U 98067A   23166.18443237  .00010989  00000+0  19492-3 0  9994
2 25544  51.6399 338.4530 0005180  82.1865 277.9712 15.50766000401487""").orbit()

# Station definition
station = create_station('BPL', ( 37.8059,144.9514, 0))
azims, elevs = [], []

print("                Time                      Azim    Elev    Distance   Radial Velocity")
print("====================================================================================")

for orb in station.visibility(tle, start=Date.now(), stop=timedelta(hours=24), step=timedelta(seconds=30), events=True):
    elev = np.degrees(orb.phi)
    # Radians are counterclockwise and azimuth is clockwise
    azim = np.degrees(-orb.theta) % 360

    # Archive for plotting
    azims.append(azim)
    # Matplotlib actually force 0 to be at the center of the polar plot,
    # so we trick it by inverting the values
    elevs.append(90 - elev)

    r = orb.r / 1000.
    print("{event:7} {orb.date} {azim:7.2f} {elev:7.2f} {r:10.2f} {orb.r_dot:10.2f}".format(
        orb=orb, r=r, azim=azim, elev=elev, event=orb.event.info if orb.event is not None else ""
    ))

    if orb.event and orb.event.info.startswith("LOS"):
        # We stop at the end of the first pass
        print()
        break

plt.figure()
ax = plt.subplot(111, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
plt.plot(np.radians(azims), elevs, '.')
ax.set_yticks(range(0, 90, 20))
ax.set_yticklabels(map(str, range(90, 0, -20)))
ax.set_rmax(90)

if "no-display" not in sys.argv:
    plt.show()
    print(Date.now())
    print(station)
     