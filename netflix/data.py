import calendar
import collections


class NetflixData(object):
    def __init__(self):
        self.master_data = collections.defaultdict(int)
        self.month_data = dict([(month, 0) for month in
                                 calendar.month_name[1:]])
        self.dow_data = dict([(day, 0) for day in
                              calendar.day_name])

    def add_viewing(self, date, time_viewed):
        self.master_data[date] += time_viewed
        self.month_data[calendar.month_name[date.month]] += time_viewed
        self.dow_data[calendar.day_name[date.weekday()]] += time_viewed

    def text_tables(self):
        month_text = '\n'.join(
                ["%s: %d:%02d" % (month, 
                                  self.month_data[month] // 60, 
                                  self.month_data[month] % 60)
                 for month in calendar.month_name[1:]])

        dow_text = '\n'.join(
                ["%s: %d:%02d" % (day, 
                                  self.dow_data[day] // 60, 
                                  self.dow_data[day] % 60)
                 for day in calendar.day_name])

        return '\n\n'.join([month_text, dow_text])

    def all_data(self):
        keys = self.master_data.keys()
        keys.sort()
        all_text = '\n'.join(
                ["%s: %d:%02d" % (date,
                                  self.master_data[date] // 60,
                                  self.master_data[date] % 60)
                 for date in keys])

        return all_text

    def line_plot(self):
        try:
            from matplotlib import dates as mdates
            from matplotlib import pyplot
        except ImportError:
            print "matplotlib not installed.  Graphing not possible"

        dates = self.master_data.keys()
        dates.sort()
        values = [self.master_data[date] for date in dates]

        months = mdates.MonthLocator()
        days = mdates.DayLocator()
        monthsFmt = mdates.DateFormatter('%B')

        fig = pyplot.figure()

        ax = fig.add_subplot(111)
        ax.plot(dates, values)
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(days)

        ax.grid(True)
        fig.autofmt_xdate()

        pyplot.show()
