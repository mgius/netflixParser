import xml.dom.minidom as minidom

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

def parseData(filename):
    historyFile = open(filename)
    historyFileData = historyFile.read()

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
    
#    for match in rowPatternCompiled.finditer(tableData):
#        mInfo = match.groupdict()
#        title = mInfo['title'].strip()
#        date = parseDate(mInfo['date'])
#        time_watched = mInfo['time_watched'])
#    cutoff_date = datetime.date(2011, 6, 1)

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


#    print sum([int(match['time_watched']) for match in \
#               matches \
#               if cutoff_date < parseDate(match['date'])])
    
if __name__ == '__main__':
    parseData(sys.argv[1])
