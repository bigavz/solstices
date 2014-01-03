__author__ = 'avi'

import urllib2
from BeautifulSoup import BeautifulSoup
import datetime
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import ephem


class EST(datetime.tzinfo):
    #define subclass for converting ephem UTC to EST
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5)

    def dst(self, dt):
        return datetime.timedelta(0)


class UTC(datetime.tzinfo):
    #define subclass to later instantiate ephem UTC as ephem does not provide tzinfo
    def utcoffset(self, dt):
        return datetime.timedelta(hours=0)

    def dst(self, dt):
        return datetime.timedelta(0)


# Input: desired lat and lon coordinates (as strings??)
# Output: a dict with date as key and tuple sunrise/sunset time as value with tzinfo
def get_sundata(lat="42", lon="-71"):
    utc = UTC()
    est = EST()
    sundata = {}
    obs = ephem.Observer()
    obs.lat = '42'
    obs.lon = '-71'


    start_date = datetime.datetime(2013, 1, 1)
    end_date = datetime.datetime(2013, 12, 31)
    deltat = datetime.timedelta(days=1)

    sun = ephem.Sun()

    date = start_date
    while date < end_date:
        date += deltat
        obs.date = date
        rise_time = obs.next_rising(sun).datetime()
        set_time = obs.next_setting(sun).datetime()
        rise_time = rise_time.replace(tzinfo=utc)
        set_time = set_time.replace(tzinfo=utc)

        sundata[date] = (rise_time.astimezone(est), set_time.astimezone(est))
    return sundata


# Input: a date string from the Soup (Mon DD, YYY H:MM AM)
# Output: a datetime string (YYYY-MM-DD HH:MM:SS)
def convert_to_datetime(soupy_date):
    return datetime.datetime.strptime(soupy_date[:-3], "%b %d, %Y %H:%M")


# Input: an integer, minutes
# Output: a string, minutes into hour:minute format
def m2hm(x, i):
    h = int(x / 60)
    m = int(x % 60)
    return '%(h)02d:%(m)02d' % {'h': h, 'm': m}


#input: datetime objects of just times
#output: integers!

def dt2m(dt):
    return (dt.hour*60) + dt.minute

#return graphable values for solstice times
def soldate(stringdate):
    return datetime.datetime.strptime(stringdate, "%b %d %Y")


def soltime(stringtime):
    return dt2m(datetime.datetime.strptime(stringtime, "%H:%M %p"))


def main():
    sundata = {}
    #one could prompt for location data too
    sundata = get_sundata()

    # separate the data into individual arrays to graph.
    # convert to relevant format (date only, integer only).
    dates, sunrise, sunset = [], [], []
    for key in sundata:
        dates.append(key)
        sunrise.append(dt2m(sundata[key][0]))
        sunset.append(dt2m(sundata[key][1]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, sunrise)
    ax.plot_date(dates, sunset)
    #draw vertical and horizontal lines
    ax.axvline(x=soldate("Dec 21 2013"))
    ax.axvline(x=soldate("Jun 21 2013"))
    ax.axhline(y=soltime("5:04 AM"))
    ax.axhline(y=soltime("5:11 PM"))

    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(m2hm))

    # woooo
    plt.show()


if __name__ == "__main__":
    main()