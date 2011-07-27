import calendar
import datetime
import re
import sys

DATA = []


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

    month_data = dict([(month, 0) for month in calendar.month_name[1:]])
    day_data = dict([(day, 0) for day in calendar.day_name])

    for match in matches:
        date = parseDate(match['date'])
        time_watched = int(match['time_watched'])
        month_data[calendar.month_name[date.month]] += time_watched
        day_data[calendar.day_name[date.weekday()]] += time_watched
    
    for month in calendar.month_name[1:]:
        print "%s: %d:%02d" % (month, 
                               month_data[month] // 60, 
                               month_data[month] % 60)
    print ""

    for day in calendar.day_name:
        print "%s: %d:%02d" % (day, 
                               day_data[day] // 60, 
                               day_data[day] % 60)

