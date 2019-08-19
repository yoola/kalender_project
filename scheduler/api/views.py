from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializer import ScheduleSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from datetimerange import DateTimeRange
import datetime

from api.help_funcs import get_day_of_every, change_24_to_00, every_change_24_to_00_end
from api.help_funcs import check_intersect_with_dates_list, check_intersect_with_every_list
from api.make_job_list import split_time_ranges_and_make_job_list
from api.add_my_jobs import add_all_jobs

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


class ScheduleList(APIView):

    def post(self, request):
        print("I'm in POST")
        print("Request body: ", request.body)
        print("Request data: ", request.data)
        # delete all jobs get_jobs

        serializer = ScheduleSerializer(data=request.data, many=True)
        list_exceptions = []
        list_every = []

        if serializer.is_valid():

            print("Data is valid")

            # serializer.save()
            start_day_list = []
            end_day_list = []
            start_time_list = []
            end_time_list = []

            for i in range(0, len(serializer.validated_data)):
                start_day_list.append(serializer.validated_data[i]['startday'])
                end_day_list.append(serializer.validated_data[i]['endday'])
                start_time_list.append(serializer.validated_data[i]['starttime'])
                end_time_list.append(serializer.validated_data[i]['endtime'])

            scheduler.pause()

            for d in range(0, len(start_day_list)):

                if not start_day_list[d].startswith('Every'):

                    if not end_day_list[d]:

                        start_date = str(start_day_list[d]) + str(' ') + str(start_time_list[d]) + str(':00')
                        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

                        # if day ends with 24:00, the end day will be the next day at 00:00
                        stop_date = str(start_day_list[d]) + str(' ') + str(end_time_list[d]) + str(':00')
                        stop_date = change_24_to_00(stop_date)

                        test_range = DateTimeRange(start_date, stop_date)
                        # check for intersections of time ranges
                        list_exceptions = check_intersect_with_dates_list(list_exceptions, test_range)

                    else:

                        start_date = str(start_day_list[d]) + str(' ') + str(start_time_list[d]) + str(':00')
                        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                        start_date_interval = str(end_day_list[d]) + str(' ') + str(start_time_list[d]) + str(':00')

                        stop_date = str(end_day_list[d]) + str(' ') + str(end_time_list[d]) + str(':00')
                        stop_date = change_24_to_00(stop_date)

                        stop_date_interval = str(start_day_list[d]) + str(' ') + str(end_time_list[d]) + str(':00')
                        stop_date_interval = change_24_to_00(stop_date_interval)

                        time_range1 = DateTimeRange(start_date, start_date_interval)
                        time_range2 = DateTimeRange(stop_date_interval, stop_date)

                        # Go in 1 day steps from start date to end date because start and end time is valid for
                        # every date between the interval days
                        for i1, j1 in zip(time_range1.range(datetime.timedelta(days=1)),
                                          time_range2.range(datetime.timedelta(days=1))):
                            test_range = DateTimeRange(i1, j1)

                            # check for intersections of time ranges
                            list_exceptions = check_intersect_with_dates_list(list_exceptions, test_range)

                if start_day_list[d].startswith('Every'):
                    list_every = check_intersect_with_every_list(get_day_of_every(start_day_list[d]),
                                                                 start_time_list[d], end_time_list[d], list_every)

            # process List_days for 24:00 entries and change it to "12 am the next day"
            if list_every:
                for i in range(0, len(list_every)):
                    if list_every[i][2] == "24:00":
                        list_every[i] = every_change_24_to_00_end(list_every[i][0], list_every[i][1], list_every[i][2])

            list_exceptions = [str(i) for i in list_exceptions]
            sorted_exception_list = sorted(list_exceptions)
            cron_start_stop, new_list_exceptions = split_time_ranges_and_make_job_list(sorted_exception_list,
                                                                                       list_every)

            new_list_exceptions = sorted(list(set(new_list_exceptions)))

            add_all_jobs(cron_start_stop, list_every, new_list_exceptions, scheduler)

            scheduler.print_jobs()
            register_events(scheduler)
            scheduler.resume()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
