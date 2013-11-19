__author__ = 'avi'

import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import emphem


# Input: strings for latitude, month, year
# Output: BeautifulSoup object
def get_soup(month="1", year="2013", lat="43"):

    #'http://www.timeanddate.com/worldclock/astronomy.html?n=43&month=1&year=2013&obj=sun&afl=-11&day=1'
    target = "http://www.timeanddate.com/worldclock/astronomy.html?n="
    suffix = '&obj=sun&afl=-11&day=1'
    soup = BeautifulSoup(urllib2.urlopen(target + lat + '&month=' + str(month) + '&year=' + year + suffix).read())
    return soup


# Input: a BeautifulSoup object
# Output: a dict with date as key and tuple sunrise/sunset time as value
def parse_soup(soup):
    sundata = {}
    for row in soup('table', {'class': 'spad'})[0].tbody('tr'):
        tds = row('td')
        # tds[0] is date (Mon DD, YYYY)
        # tds[1] is sunrise (H:MM AM)
        # tds[2] is sunset (H:MM PM)
        #print tds[0].string, "_", tds[1].string, "_", tds[2].string
        # will print date and sunrise as Jan 31, 2013 6:59 AM 4:57 AM or (tds[0]+tds[1])[-3] = %m %d, %Y %H:%M
        date = convert_to_datetime(tds[0].string + ' ' + tds[1].string).date()
        print(date)
        sunrise = convert_to_datetime(tds[0].string + ' ' + tds[1].string).time()
        sunset = convert_to_datetime(tds[0].string + ' ' + tds[2].string).time()
        sundata[date] = (sunrise, sunset)
    return sundata


# Input: a date string from the Soup (Mon DD, YYY H:MM AM)
# Output: a datetime string (YYYY-MM-DD HH:MM:SS)
def convert_to_datetime(soupy_date):
    return datetime.strptime(soupy_date[:-3], "%b %d, %Y %H:%M")


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


def main():
    sundata = {}
    month = 3
    while month < 13:
        sundata.update(parse_soup(get_soup(month)))
        month+=1


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

    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(m2hm))

    # woooo
    plt.show()


if __name__ == "__main__":
    main()