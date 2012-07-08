import calendar
import collections
import copy


def init_year():
    return dict([(month, 0) for month in
                calendar.month_name[1:]])


class NetflixData(object):
    def __init__(self):
        self.master_data = collections.defaultdict(int)

    def add_viewing(self, date, time_viewed):
        self.master_data[date] += time_viewed

    def viewings_by_month(self):
        month_data = {}
        for date, time_viewed in self.master_data.iteritems():
            if date.year not in month_data:
                month_data[date.year] = init_year()

            year_dict = month_data[date.year]
            year_dict[calendar.month_name[date.month]] += time_viewed

        return month_data

    def viewings_by_dow(self):
        dow_data = dict([(day, 0) for day in
                              calendar.day_name])

        for date, time_viewed in self.master_data.iteritems():
            dow_data[calendar.day_name[date.weekday()]] += time_viewed

        return dow_data

    def active_days(self, hour_threshold=8):
        active_days = {}

        for date, time_watched in self.master_data.iteritems():
            if time_watched >= hour_threshold * 60:
                active_days[date] = time_watched

        return active_days


# don't currently have time of day info
#    def viewings_by_time_of_day(self):
#        tod_data = collections.defaultdict(int)
#
#        for date, time_viewed in self.master_data.iteritems():
#            tod_data[date.hour % 24 // 6]
#
#        return dict(latenight=tod_data[0],
#                    morning=tod_data[1],
#                    afternoon=tod_data[2],
#                    evening=tod_data[3])

    def text_tables(self):
        out_list = []

        month_data = self.viewings_by_month()
        for year in month_data:
            for month in calendar.month_name[1:]:
                if month_data[year][month] == 0:
                    continue
                out_list.append(
                "%s %d: %d:%02d" % (month, year,
                                  month_data[year][month] // 60,
                                  month_data[year][month] % 60))

        month_text = '\n'.join(out_list)

        dow_data = self.viewings_by_dow()
        dow_text = '\n'.join(
                ["%s: %d:%02d" % (day,
                                  dow_data[day] // 60,
                                  dow_data[day] % 60)

                 for day in calendar.day_name])

        total_time = sum(self.master_data.values())
        total_days = total_time // (24 * 60)
        partial_day = total_time - (total_days * 24 * 60)
        total_text = "Total Time: %d days, %d:%02d hours" % (
                    total_days, partial_day // 60, partial_day % 60)

        return '\n\n'.join([month_text, dow_text, total_text])

    def unusual_days(self):
        active_days = self.active_days()

        active_table = '\n'.join(
                ["%s: %d:%02d" % (day, time_viewed // 60, time_viewed % 60)
                 for day, time_viewed in sorted(active_days.iteritems())])

        active_text = '\n'.join(("Wow, you watched a lot of netflix on "
                                "these days:\n",
                                active_table))

        return '\n\n'.join([active_text])

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
