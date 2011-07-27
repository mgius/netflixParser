import calendar
import datetime
import re
import sys

from netflix import data as n_data


def parseDate(dateString):
    '''
    Takes in a datestring and pumps out a date object
    12/10/2010 -> Dec 10 2010 -> dateetime.date(2010, 12, 10)
    assumes two digit years are 20XX
    '''
    (month, day, year) = dateString.split('/')
    if len(year) == 2:
        year = '20' + year
    return datetime.date(int(year), int(month), int(day))


def parseData(data):
    ''' Parses html data and returns a NetflixData object '''
    historyFileData = data.read()

    tablePattern = re.compile('(?P<tableData><table>.*?</table>)', re.DOTALL)
    try:
        tableData = tablePattern.search(historyFileData).group('tableData')
    except AttributeError:
        print "Probably couldn't find <table></table> in the filename"
        sys.exit(1)

    rowPattern = '<tr>.*?<a.*?>(?P<title>.*?)</a>.*?' \
                 '<td>(?P<date>\d+/\d+/\d+)</td>.*?' \
                 '<label>(?P<time_watched>\d+)m</label>'

    rowPatternCompiled = re.compile(rowPattern, re.DOTALL)

    matches = [match.groupdict() for match in \
               rowPatternCompiled.finditer(tableData)]

    data = n_data.NetflixData()
    data_add_viewing = data.add_viewing
    for match in matches:
        date = parseDate(match['date'])
        time_watched = int(match['time_watched'])
        data_add_viewing(date, time_watched)

    return data
