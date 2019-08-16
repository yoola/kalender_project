from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializer import ScheduleSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


import datetime
from datetimerange import DateTimeRange



from api.help_funcs import get_day_of_Every, change_24_to_00, split_intervall_days, join_list_dates
from api.help_funcs import check_intersect_with_dates_list, check_intersect_with_every_list
from api.make_job_list import split_time_ranges_and_make_job_list, process_exception_list
from api.add_my_jobs import start_job, stop_job, randID, add_all_jobs

# If you want all scheduled jobs to use this store by default,
# use the name 'default' instead of 'djangojobstore'.

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


class ScheduleList(APIView):
	"""
	this class does this and this
	"""


    # def get(self, request):
    # 	schedule = Schedule.objects.all()
    # 	#schedule.objects.filter(pk=schedule.startday).update(starttime=schedule.starttime, endtime=schedule.endtime)
    # 	serializer = ScheduleSerializer(schedule, many= True, context={'request':request})
    # 	return Response(serializer.data)

    def post(self, request, format=None):
        print("I'm in POST")
        print("Request body: ", request.body)
        print("Request data: ", request.data)
        # delete all jobs get_jobs

        serializer = ScheduleSerializer(data=request.data, many=True)
        list_exceptions = []
        list_every = []

        # starttime_list = []

        if serializer.is_valid():

            print("Data is valid")

            # serializer.save()

            startday_list = []
            endday_list = []
            starttime_list = []
            endtime_list = []

            for i in range(0, len(serializer.validated_data)):
                startday_list.append(serializer.validated_data[i]['startday'])
                endday_list.append(serializer.validated_data[i]['endday'])
                starttime_list.append(serializer.validated_data[i]['starttime'])
                endtime_list.append(serializer.validated_data[i]['endtime'])

            scheduler.pause()

            for d in range(0, len(startday_list)):

                if not startday_list[d].startswith('Every'):

                    if not endday_list[d]:

                        startDate = str(startday_list[d]) + str(' ') + str(starttime_list[d]) + str(':00')
                        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
                        startDateEnd = startDate + datetime.timedelta(seconds=1)

                        # define that if it is a specific day, the end day will be the next day at 00:00
                        stopDate = str(startday_list[d]) + str(' ') + str(endtime_list[d]) + str(':00')
                        stopDate = change_24_to_00(stopDate)
                        stopDateEnd = stopDate + datetime.timedelta(seconds=1)

                        test_range = DateTimeRange(startDate, stopDate)
                        # check for intersections of time ranges
                        list_exceptions = check_intersect_with_dates_list(list_exceptions, test_range)

                    else:

                        startDate = str(startday_list[d]) + str(' ') + str(starttime_list[d]) + str(':00')
                        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
                        startDate_intervall = str(endday_list[d]) + str(' ') + str(starttime_list[d]) + str(':00')

                        stopDate = str(endday_list[d]) + str(' ') + str(endtime_list[d]) + str(':00')
                        stopDate = change_24_to_00(stopDate)

                        stopDate_intervall = str(startday_list[d]) + str(' ') + str(endtime_list[d]) + str(':00')
                        stopDate_intervall = change_24_to_00(stopDate_intervall)

                        time_range1 = DateTimeRange(startDate, startDate_intervall)
                        time_range2 = DateTimeRange(stopDate_intervall, stopDate)

                        print("!!!!!!!time_range1: ", time_range1)
                        print("!!!!!!!time_range2: ", time_range2)

                        # Go in 1 day steps from start date to end date because start and end time is valid for every date between the intervall days
                        for i1, j1 in zip(time_range1.range(datetime.timedelta(days=1)),
                                          time_range2.range(datetime.timedelta(days=1))):
                            test_range = DateTimeRange(i1, j1)
                            print("!!!!!!!test_range: ", test_range)

                            # check for intersections of time ranges
                            list_exceptions = check_intersect_with_dates_list(list_exceptions, test_range)

                if startday_list[d].startswith('Every'):
                    starthour_ = starttime_list[d][0:2]
                    startminute_ = starttime_list[d][4:6]
                    endhour_ = endtime_list[d][0:2]
                    endminute_ = endtime_list[d][4:6]

                    list_every = check_intersect_with_every_list(get_day_of_Every(startday_list[d]), starttime_list[d],
                                                                 endtime_list[d], list_every)

            list_exceptions = [str(i) for i in list_exceptions]
            sorted_exception_list = sorted(list_exceptions)
            cron_start_stop, new_list_exceptions = split_time_ranges_and_make_job_list(list_exceptions, list_every)

            # new_list_exceptions = sorted(list(set(new_list_exceptions)))

            add_all_jobs(cron_start_stop, list_every, new_list_exceptions, scheduler)

            scheduler.print_jobs()
            register_events(scheduler)
            # scheduler.resume()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
