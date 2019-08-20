import datetime
from datetimerange import DateTimeRange
import string
import random

from api.help_funcs import split_interval_days


def start_job():
    print("Start job")


def stop_job():
    print("Stop job")


def randID(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_cron_job(cron_day, stop_date):
    days_ = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cron_day = days_.index(cron_day)
    today_ = datetime.date.today()

    date1 = datetime.datetime.strptime(str(today_), '%Y-%m-%d')
    date2 = datetime.datetime.strptime(stop_date, '%Y-%m-%d') - datetime.timedelta(days=1)
    time_range = DateTimeRange(date1, date2)

    for value in time_range.range(datetime.timedelta(days=1)):
        if cron_day == value.weekday():
            return True

    return False


def get_day_from_number(number):
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    return days[number]


def add_all_jobs(cron_start_stop, list_every, new_list_exceptions, scheduler):
    for i in range(0, len(cron_start_stop)):
        for j in range(0, len(cron_start_stop[i])):
            new_start = datetime.datetime.strptime(cron_start_stop[i][j][1], '%Y-%m-%d')
            new_end = datetime.datetime.strptime(cron_start_stop[i][j][0], '%Y-%m-%d')
            new_start = new_start + datetime.timedelta(days=1)
            new_start = str(new_start)
            new_end = str(new_end)
            cron_start_stop[i][j] = (new_end, new_start)

    for i in range(0, len(list_every)):

        start_time_ = list_every[i][1]
        end_time = list_every[i][2]
        start_hour = start_time_[0:2]
        end_hour = end_time[0:2]
        start_minute = start_time_[3:6]
        end_minute = end_time[3:6]

        # add all other jobs which have only a start_date and  an end_date
        if len(cron_start_stop[i]) >= 1:

            for j in range(0, len(cron_start_stop[i])):

                if j == 0:

                    stop_here = cron_start_stop[i][j][0]
                    sep_list = split_interval_days(list_every[i][0])

                    # check if every day job can at least run one time before it already ends
                    if add_cron_job(sep_list[0], stop_here[0:10]):

                        if "-" in list_every[i][0]:

                            scheduler.add_job(start_job, 'cron', id="start_job_" + str(sep_list[0]) + "-" + str(
                                sep_list[1]) + "_" + randID(), day_of_week=sep_list[0], hour=start_hour,
                                              minute=start_minute, end_date=str(stop_here))
                            scheduler.add_job(stop_job, 'cron',
                                              id="stop_job_" + str(sep_list[0]) + "-" + str(sep_list[1]) + randID(),
                                              day_of_week=sep_list[1], hour=end_hour, minute=end_minute,
                                              end_date=str(stop_here))

                        else:

                            scheduler.add_job(start_job, 'cron',
                                              id="start_job_" + str(list_every[i][0]) + "_" + randID(),
                                              day_of_week=str(list_every[i][0]), hour=start_hour, minute=start_minute,
                                              end_date=str(stop_here))
                            scheduler.add_job(stop_job, 'cron', id="stop_job_" + str(list_every[i][0]) + "_" + randID(),
                                              day_of_week=str(list_every[i][0]), hour=end_hour, minute=end_minute,
                                              end_date=str(stop_here))

                if not (j == 0 or j == len(cron_start_stop[i])):

                    stop_here = cron_start_stop[i][j][0]
                    start_here = cron_start_stop[i][j - 1][1]
                    sep_list = split_interval_days(list_every[i][0])

                    if add_cron_job(sep_list[0], stop_here[0:10]):

                        if "-" in list_every[i][0]:
                            
                            scheduler.add_job(start_job, 'cron', id="start_job_" + str(sep_list[0]) + "-" + str(
                                sep_list[1]) + "_" + randID(), day_of_week=sep_list[0], hour=start_hour,
                                              minute=start_minute, start_date=start_here, end_date=stop_here)
                            scheduler.add_job(stop_job, 'cron', id="stop_job_" + str(sep_list[0]) + "-" + str(
                                sep_list[1]) + "_" + randID(), day_of_week=sep_list[1], hour=end_hour,
                                              minute=end_minute, start_date=start_here, end_date=stop_here)

                        else:

                            scheduler.add_job(start_job, 'cron',
                                              id="start_job_" + str(list_every[i][0]) + "_" + randID(),
                                              day_of_week=list_every[i][0], hour=start_hour, minute=start_minute,
                                              start_date=start_here, end_date=stop_here)
                            scheduler.add_job(stop_job, 'cron', id="stop_job_" + str(list_every[i][0]) + "_" + randID(),
                                              day_of_week=list_every[i][0], hour=end_hour, minute=end_minute,
                                              start_date=start_here, end_date=stop_here)

            start_here = cron_start_stop[i][-1][1]

            if "-" in list_every[i][0]:
                sep_list = split_interval_days(list_every[i][0])

                scheduler.add_job(start_job, 'cron',
                                  id="start_job_" + str(sep_list[0]) + "-" + str(sep_list[1]) + "_" + randID(),
                                  day_of_week=sep_list[0], hour=start_hour, minute=start_minute,
                                  start_date=str(start_here))
                scheduler.add_job(stop_job, 'cron',
                                  id="stop_job_" + str(sep_list[0]) + "-" + str(sep_list[1]) + "_" + randID(),
                                  day_of_week=sep_list[1], hour=end_hour, minute=end_minute, start_date=str(start_here))

            else:
                scheduler.add_job(start_job, 'cron', id="start_job_" + str(list_every[i][0]) + "_" + randID(),
                                  day_of_week=list_every[i][0], hour=start_hour, minute=start_minute,
                                  start_date=str(start_here))
                scheduler.add_job(stop_job, 'cron', id="stop_job_" + str(list_every[i][0]) + "_" + randID(),
                                  day_of_week=list_every[i][0], hour=end_hour, minute=end_minute,
                                  start_date=str(start_here))

        else:

            if "-" in list_every[i][0]:
                sep_list = split_interval_days(list_every[i][0])

                scheduler.add_job(start_job, 'cron',
                                  id="start_job_" + str(sep_list[0]) + "-" + str(sep_list[1]) + "_" + randID(),
                                  day_of_week=sep_list[0], hour=start_hour, minute=start_minute)
                scheduler.add_job(stop_job, 'cron',
                                  id="stop_job_" + str(sep_list[0]) + "-" + str(sep_list[1]) + "_" + randID(),
                                  day_of_week=sep_list[1], hour=end_hour, minute=end_minute)

            else:
                scheduler.add_job(start_job, 'cron', id="start_job_" + str(list_every[i][0]) + "_" + randID(),
                                  day_of_week=str(list_every[i][0]), hour=start_hour, minute=start_minute)
                scheduler.add_job(stop_job, 'cron', id="stop_job_" + str(list_every[i][0]) + "_" + randID(),
                                  day_of_week=str(list_every[i][0]), hour=end_hour, minute=end_minute)

    for i in new_list_exceptions:

        if len(i) == 41:
            first = str(i)[0:19]
            first = first.replace('T', ' ')
            second = str(i)[22:42]
            second = second.replace('T', ' ')

            first = datetime.datetime.strptime(first, '%Y-%m-%d %H:%M:%S')
            second = datetime.datetime.strptime(second, '%Y-%m-%d %H:%M:%S')

            day1 = get_day_from_number(first.weekday())
            day2 = get_day_from_number(second.weekday())

            if not day1 == day2:
                day1 = day1 + "-" + day2
            
            scheduler.add_job(start_job, id="start_job_" + day1 + "_" + randID(), trigger='date', next_run_time=str(first))
            scheduler.add_job(stop_job, id="stop_job_" + day1 + "_" + randID(), trigger='date', next_run_time=str(second))
        else:
            print("No available time format.")