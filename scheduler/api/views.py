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

from api.help_funcs import check_insect_with_dates_list

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

	list_times = []

	def get(self, request):
		schedule = Schedule.objects.all()
		#schedule.objects.filter(pk=schedule.startday).update(starttime=schedule.starttime, endtime=schedule.endtime)
		serializer = ScheduleSerializer(schedule, many= True, context={'request':request})
		return Response(serializer.data)


	def post(self, request, format=None):
		print("I'm in POST")
		print("Request body: ",request.body)
		print("Request data: ",request.data)
		#delete all jobs get_jobs
		
		serializer = ScheduleSerializer(data=request.data)

		


		if serializer.is_valid():
			
			serializer.save()

			scheduler.pause()

			startday_ = serializer.validated_data.get('startday')
			endday_ = serializer.validated_data.get('endday')
			starttime_ = serializer.validated_data.get('starttime')
			endtime_ = serializer.validated_data.get('endtime')
			if not startday_.startswith('Every'):

				if not endday_:

					startDate = str(startday_)+str(' ')+str(starttime_)+str(':00')
					startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
					startDateEnd = startDate + datetime.timedelta(seconds=1)
	
					# define that if it is a specific day, the end day will be the next day at 00:00
					stopDate = str(startday_)+str(' ')+str(endtime_)+str(':00')
					if stopDate[11:13] == "24":
						stopDate = stopDate.replace("24","00")
						stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
						stopDate = stopDate + datetime.timedelta(days=1)
					else:
						stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
					stopDateEnd = stopDate + datetime.timedelta(seconds=1)
					

				else:

					startDate = str(startday_)+str(' ')+str(starttime_)+str(':00')
					startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
					startDateEnd = startDate + datetime.timedelta(seconds=1)

					stopDate = str(endday_)+str(' ')+str(endtime_)+str(':00')
					if stopDate[11:13] == "24":
						stopDate = stopDate.replace("24","00")
						stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
						stopDate = stopDate + datetime.timedelta(days=1)
					else:
						stopDate = datetime.datetime.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
					
					stopDateEnd = stopDate + datetime.timedelta(seconds=1)

				print("startDate: ", startDate)
				print("startDateEnd: ", startDateEnd)
				print("stopDate: ", stopDate)
				print("stopDate: ", stopDateEnd)
				# The job will be executed on startigDate
				# Store the job in a variable in case we want to cancel it
				jobStart = scheduler.add_job(start_job, 'cron', start_date=startDate, end_date  = startDateEnd, replace_existing=True)
				jobStop = scheduler.add_job(stop_job, 'cron', start_date=stopDate, end_date  = stopDateEnd, replace_existing=True)

				test_range = DateTimeRange(startDate, stopDate)

				# check for intersections of time ranges
				ScheduleList.list_times = check_insect_with_dates_list(ScheduleList.list_times, test_range )
				print("list times api: ", ScheduleList.list_times)

				scheduler.print_jobs()

				#scheduler.add_job(new_job, 'cron', id=startday_, start_date= startingDate, end_date = stopingDate)
				register_events(scheduler)
				scheduler.resume()
				

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



		