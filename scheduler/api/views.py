from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import ScheduleSerializer
from api.models import Schedule

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

import time
import datetime
from datetimerange import DateTimeRange

import string
import random

from api.help_funcs import check_insect_with_dates_list, get_day_of_Every

# If you want all scheduled jobs to use this store by default,
# use the name 'default' instead of 'djangojobstore'.

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()




def randID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


    # raise ValueError("Olala!")

def start_job():
	print("Start job")

def stop_job():
	print("Stop job")


class ScheduleList(APIView):


	# def get(self, request):
	# 	schedule = Schedule.objects.all()
	# 	#schedule.objects.filter(pk=schedule.startday).update(starttime=schedule.starttime, endtime=schedule.endtime)
	# 	serializer = ScheduleSerializer(schedule, many= True, context={'request':request})
	# 	return Response(serializer.data)


	def post(self, request, format=None):
		print("I'm in POST")
		print("Request body: ",request.body)
		print("Request data: ",request.data)
		#delete all jobs get_jobs
		
		serializer = ScheduleSerializer(data=request.data, many= True)
		list_times = []
		list_every = []
		
		#starttime_list = []

		if serializer.is_valid():

			print("Data is valid")

			#serializer.save()

			startday_list = []
			endday_list = []
			starttime_list = []
			endtime_list = []

			for i in range(0,len(serializer.validated_data)):
				startday_list.append(serializer.validated_data[i]['startday'])
				endday_list.append(serializer.validated_data[i]['endday'])
				starttime_list.append(serializer.validated_data[i]['starttime'])
				endtime_list.append(serializer.validated_data[i]['endtime'])

			# scheduler.pause()


			# print("startday_list", startday_list)
			# print("endday_list", endday_list)
			# print("starttime_list", starttime_list)
			# print("endtime_list", endtime_list)


			for d in range(0,len(startday_list)):



				if not startday_list[d].startswith('Every'):

					if not endday_list[d]:

						startDate = str(startday_list[d])+str(' ')+str(starttime_list[d])+str(':00')
						startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
						startDateEnd = startDate + datetime.timedelta(seconds=1)
		
						# define that if it is a specific day, the end day will be the next day at 00:00
						stopDate = str(startday_list[d])+str(' ')+str(endtime_list[d])+str(':00')
						if stopDate[11:13] == "24":
							stopDate = stopDate.replace("24","00")
							stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
							stopDate = stopDate + datetime.timedelta(days=1)
						else:
							stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
						stopDateEnd = stopDate + datetime.timedelta(seconds=1)

						test_range = DateTimeRange(startDate, stopDate)
						# check for intersections of time ranges
						list_times = check_insect_with_dates_list(list_times, test_range )					

					else:

						startDate = str(startday_list[d])+str(' ')+str(starttime_list[d])+str(':00')
						startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
						startDate_intervall = str(endday_list[d])+str(' ')+str(starttime_list[d])+str(':00')

						stopDate = str(endday_list[d])+str(' ')+str(endtime_list[d])+str(':00')
						if stopDate[11:13] == "24":
							stopDate = stopDate.replace("24","00")
							stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
							stopDate = stopDate + datetime.timedelta(days=1)
						else:
							stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
						

						stopDate_intervall = str(startday_list[d])+str(' ')+str(endtime_list[d])+str(':00')

						time_range1 = DateTimeRange(startDate, startDate_intervall)
						time_range2 = DateTimeRange(stopDate_intervall, stopDate)


						for i1, j1 in zip(time_range1.range(datetime.timedelta(days=1)), time_range2.range(datetime.timedelta(days=1))):						

							test_range = DateTimeRange(i1, j1)

							# check for intersections of time ranges
							list_times = check_insect_with_dates_list(list_times, test_range )

				if startday_list[d].startswith('Every'):

					starthour_ = starttime_list[d][0:2]
					startminute_ = starttime_list[d][4:6]
					endhour_ = endtime_list[d][0:2]
					endminute_ = endtime_list[d][4:6]
					print("hour: ", hour_)

					scheduler.add_job(start_job, 'cron', day_of_week=get_day_of_Every(startday_list[d]), hour=starthour_, minute= startminute_)
					scheduler.add_job(stop_job, 'cron', day_of_week=get_day_of_Every(startday_list[d]), hour=endhour_, minute= endminute_)

					#print(" Ok, this starts with Every: ", get_day_of_Every(startday_list[d]))



			# print("Final datetimes list: ", list_times)

			# for i in list_times:

			# 	first_ = str(i)[0:19]
			# 	first_ = first_.replace('T', ' ')
			# 	second_ = str(i)[22:42]
			# 	second_ = second_.replace('T', ' ')
			
			# 	first_ = datetime.datetime.strptime(first_, '%Y-%m-%d %H:%M:%S')
			# 	second_ = datetime.datetime.strptime(second_, '%Y-%m-%d %H:%M:%S')
				
			# 	jobStart = scheduler.add_job(start_job, id = "start_job_"+randID(), trigger='date', next_run_time=str(first_))
			# 	jobStop = scheduler.add_job(stop_job, id = "stop_job_"+randID(), trigger='date', next_run_time=str(second_))
								
			# scheduler.print_jobs()
			# register_events(scheduler)
			# scheduler.resume()
				

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)