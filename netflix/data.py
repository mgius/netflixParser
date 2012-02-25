import calendar
import collections
import copy


def init_year():
    return dict([(month, 0) for month in
                calendar.month_name[1:]])


class NetflixData(object):
    def __init__(self):
        self.master_data = collections.defaultdict(int)
        self.month_data = init_year()
        self.month_year_data = {}
        self.dow_data = dict([(day, 0) for day in
                              calendar.day_name])

    def add_viewing(self, date, time_viewed):
        self.master_data[date] += time_viewed
        if date.year not in self.month_year_data:
            self.month_year_data[date.year] = init_year()
        self.month_year_data[date.year][calendar.month_name[date.month]] += \
                time_viewed
        self.month_data[calendar.month_name[date.month]] += time_viewed
        self.dow_data[calendar.day_name[date.weekday()]] += time_viewed

    def text_tables(self):
        out_list = []
        for year in self.month_year_data:
            for month in calendar.month_name[1:]:
                out_list.append(
                "%s %d: %d:%02d" % (month, year,
                                  self.month_year_data[year][month] // 60,
                                  self.month_year_data[year][month] % 60))

        month_text = '\n'.join(out_list)

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

        master_data_copy = copy.copy(self.master_data)

        dates = master_data_copy.keys()
        dates.sort()
        values = [master_data_copy[date] for date in dates]

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
