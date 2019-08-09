from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import ScheduleSerializer
from api.models import Schedule

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

import time
import datetime
from datetimerange import DateTimeRange

import string
import random

from api.help_funcs import get_day_of_Every, change_24_to_00, every_change_24_to_00, split_intervall_days
from api.help_funcs import check_insect_with_dates_list, check_insect_with_every_list
from api.make_job_list import split_time_ranges_and_add_job
# If you want all scheduled jobs to use this store by default,
# use the name 'default' instead of 'djangojobstore'.

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()

def start_job():
	print("Start job")

def stop_job():
	print("Stop job")




def randID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


    # raise ValueError("Olala!")




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
		list_exceptions = []
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

			scheduler.pause()


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
						stopDate = change_24_to_00(stopDate)
						stopDateEnd = stopDate + datetime.timedelta(seconds=1)

						test_range = DateTimeRange(startDate, stopDate)
						# check for intersections of time ranges
						list_exceptions = check_insect_with_dates_list(list_exceptions, test_range )					

					else:

						startDate = str(startday_list[d])+str(' ')+str(starttime_list[d])+str(':00')
						startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
						startDate_intervall = str(endday_list[d])+str(' ')+str(starttime_list[d])+str(':00')

						stopDate = str(endday_list[d])+str(' ')+str(endtime_list[d])+str(':00')
						stopDate = change_24_to_00(stopDate)
						

						stopDate_intervall = str(startday_list[d])+str(' ')+str(endtime_list[d])+str(':00')

						time_range1 = DateTimeRange(startDate, startDate_intervall)
						time_range2 = DateTimeRange(stopDate_intervall, stopDate)


						for i1, j1 in zip(time_range1.range(datetime.timedelta(days=1)), time_range2.range(datetime.timedelta(days=1))):						

							test_range = DateTimeRange(i1, j1)

							# check for intersections of time ranges
							list_exceptions = check_insect_with_dates_list(list_exceptions, test_range )

				if startday_list[d].startswith('Every'):

					starthour_ = starttime_list[d][0:2]
					startminute_ = starttime_list[d][4:6]
					endhour_ = endtime_list[d][0:2]
					endminute_ = endtime_list[d][4:6]

					list_every = check_insect_with_every_list(get_day_of_Every(startday_list[d]), starttime_list[d], endtime_list[d], list_every)


			list_exceptions = [str(i) for i in list_exceptions]
			sorted_exception_list = sorted(list_exceptions)
			cron_start_stop, new_list_exceptions = split_time_ranges_and_add_job(list_exceptions, list_every)

			# add one day to start dates
			# cut out times

			for i in range(0,len(cron_start_stop)):
				for j in range(0,len(cron_start_stop[i])):
					
					new_start= datetime.datetime.strptime(cron_start_stop[i][j][1]+":00", '%Y-%m-%d %H:%M:%S')
					new_end= datetime.datetime.strptime(cron_start_stop[i][j][0]+":00", '%Y-%m-%d %H:%M:%S')
					new_start = new_start+ datetime.timedelta(days=1)
					new_start = str(new_start)
					new_end = str(new_end)
					cron_start_stop[i][j] = (new_end[0:10],new_start[0:10])

			for i in range(0,len(cron_start_stop)):
				place_holder = str(datetime.datetime.strptime("2019-01-01", '%Y-%m-%d'))


				cron_start_stop[i].insert(0,(place_holder[0:10],place_holder[0:10]))
				cron_start_stop[i].append((place_holder[0:10],place_holder[0:10]))

			seperate_days_list = split_intervall_days(list_every[0][0])

			# starttime_ = list_every[0][1]
			# endtime_ = list_every[0][2]	
			# starthour_ = starttime_[0:2]
			# endhour_ = endtime_[0:2]
			# startminute_ = starttime_[3:6]
			# endminute_ = endtime_[3:6]

			# print("CRON LIST: ", cron_start_stop)

			scheduler.add_job(start_job, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-06-02')

			print("Final every day list: ", list_every)
			print("cron_start_stop: ", cron_start_stop)
			for i in range(0,len(list_every)):
			
				if  list_every[i][2].startswith("24:00"):
					list_every[i] = every_change_24_to_00(list_every[i][0], list_every[i][1], list_every[i][2])

				starttime_ = list_every[i][1]
				endtime_ = list_every[i][2]	
				starthour_ = starttime_[0:2]
				endhour_ = endtime_[0:2]
				startminute_ = starttime_[3:6]
				endminute_ = endtime_[3:6]

				print("i: ",i)
				print("cron_start_stop[i][1][0]: ",cron_start_stop[i][1][0])
				
				
				#add all other jobs which have only a start_date and  an end_date

				# if len(cron_start_stop)>2:

				# 	print("len(cron_start_stop[i]): ",len(cron_start_stop[i]))

				# 	for j in range(0,len(cron_start_stop[i])-1):
						
						
				# 		start_here = cron_start_stop[i][j][1]
				# 		stop_here = cron_start_stop[i][j+1][0]

				# 		print("start_here: ", start_here)
				# 		print("stop_here: ", stop_here)

				# 		if j == 0:					

				# 			print("stop_here: ", stop_here)

				# 			if "-" in list_every[i][0]:
				# 				seperate_days_list = split_intervall_days(list_every[i][0])

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=seperate_days_list[0], hour=starthour_, minute=startminute_, end_date = str(stop_here))
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=seperate_days_list[1], hour=endhour_, minute=endminute_, end_date = str(stop_here))
				# 			else:

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=list_every[i][0], hour=starthour_, minute=startminute_,  end_date = str(stop_here))
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=list_every[i][0], hour=endhour_, minute=endminute_, end_date = str(stop_here))

				# 		if j == (len(cron_start_stop)-1):


				# 			print("start_here: ", start_here)
							

				# 			if "-" in list_every[i][0]:
				# 				seperate_days_list = split_intervall_days(list_every[i][0])

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=seperate_days_list[0], hour=starthour_, minute=startminute_, start_date = str(start_here))
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=seperate_days_list[1], hour=endhour_, minute=endminute_,start_date = str(start_here))
				# 			else:

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=list_every[i][0], hour=starthour_, minute=startminute_,  start_date = str(start_here))
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=list_every[i][0], hour=endhour_, minute=endminute_, start_date = str(start_here))

				# 		if not (j==0 or j == 1 or j == len(cron_start_stop)-1 or j==len(cron_start_stop)):

				# 			if "-" in list_every[i][0]:
				# 				seperate_days_list = split_intervall_days(list_every[i][0])

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=seperate_days_list[0], hour=starthour_, minute=startminute_, start_date = start_here, end_date = stop_here)
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=seperate_days_list[1], hour=endhour_, minute=endminute_, start_date = start_here, end_date = stop_here)
				# 			else:

				# 				scheduler.add_job(start_job, 'cron', id = "start_job_"+randID(), day_of_week=list_every[i][0], hour=starthour_, minute=startminute_, start_date = start_here, end_date = stop_here)
				# 				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+randID(), day_of_week=list_every[i][0], hour=endhour_, minute=endminute_, start_date = start_here, end_date = stop_here)




			# print("Final datetimes list: ", list_exceptions)

			# for i in list_exceptions:

			# 	first_ = str(i)[0:19]
			# 	first_ = first_.replace('T', ' ')
			# 	second_ = str(i)[22:42]
			# 	second_ = second_.replace('T', ' ')

			# 	print("first_ :", first_)
			# 	print("second_: ", second_)
			
			# 	first_ = datetime.datetime.strptime(first_, '%Y-%m-%d %H:%M:%S')
			# 	second_ = datetime.datetime.strptime(second_, '%Y-%m-%d %H:%M:%S')
				
			# 	jobStart = scheduler.add_job(start_job, id = "start_job_"+randID(), trigger='date', next_run_time=str(first_))
			# 	jobStop = scheduler.add_job(stop_job, id = "stop_job_"+randID(), trigger='date', next_run_time=str(second_))

								
			#scheduler.print_jobs()
			#register_events(scheduler)
			#scheduler.resume()
				

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)