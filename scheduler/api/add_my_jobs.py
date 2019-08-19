import time
import datetime
from datetimerange import DateTimeRange

import string
import random

from api.help_funcs import split_intervall_days


def start_job():
	print("Start job")

def stop_job():
	print("Stop job")


def randID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def add_cron_job(cron_day, stop_date):

	days_= ["mon","tue","wed","thu","fri","sat","sun"]
	cron_day = days_.index(cron_day)
	today_ = datetime.date.today()

	date1 =  datetime.datetime.strptime(str(today_), '%Y-%m-%d')
	date2 =  datetime.datetime.strptime(stop_date, '%Y-%m-%d')-datetime.timedelta(days=1)
	time_range = DateTimeRange(date1, date2)

	for value in time_range.range(datetime.timedelta(days=1)):
		if cron_day == value.weekday():
			return True

	return False

def add_all_jobs(cron_start_stop, list_every, new_list_exceptions,scheduler):

	for i in range(0,len(cron_start_stop)):
		for j in range(0,len(cron_start_stop[i])):
			
			new_start= datetime.datetime.strptime(cron_start_stop[i][j][1], '%Y-%m-%d')
			new_end= datetime.datetime.strptime(cron_start_stop[i][j][0], '%Y-%m-%d')
			new_start = new_start+ datetime.timedelta(days=1)
			new_start = str(new_start)
			new_end = str(new_end)
			cron_start_stop[i][j] = (new_end,new_start)


	print("Final every day list: ", list_every)
	print("cron_start_stop: ", cron_start_stop)
	for i in range(0,len(list_every)):

		print("iiiiii-----------------new i: ",i,", ",list_every[i],"-------------------")
	
		# if  list_every[i][2].startswith("24:00"):
		# 	list_every[i] = every_change_24_to_00_end(list_every[i][0], list_every[i][1], list_every[i][2])

		starttime_ = list_every[i][1]
		endtime_ = list_every[i][2]	
		starthour_ = starttime_[0:2]
		endhour_ = endtime_[0:2]
		startminute_ = starttime_[3:6]
		endminute_ = endtime_[3:6]
		
		#add all other jobs which have only a start_date and  an end_date
		if len(cron_start_stop[i])>=1:


			print("len(cron_start_stop[i]): ",len(cron_start_stop[i]),"\n")

			for j in range(0,len(cron_start_stop[i])):

				print("jjjjj-----------------new j: ",j,", ",cron_start_stop[i][j],"-------------------")
				

				if j == 0:

					stop_here = cron_start_stop[i][j][0]					
					print("stop_here in j=",j, stop_here,"\n")
					sep_list = split_intervall_days(list_every[i][0])

					if(add_cron_job(sep_list[0],stop_here[0:10])): #check if every day job can at least run one time before it already ends

						if "-" in list_every[i][0]:
						
							scheduler.add_job(start_job, 'cron', id = "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[0], hour=starthour_, minute=startminute_, end_date= str(stop_here))
							scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+randID(), day_of_week=sep_list[1], hour=endhour_, minute=endminute_, end_date= str(stop_here))

							print("scheduler add 0 with -: ", "start_job", "id = ", "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[0], "hour=", starthour_, "minute=", startminute_, "end_date=", str(stop_here))
							print("scheduler add 0 with -: ", "stop_job", "id = ", "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[1], "hour=", endhour_, "minute=", endminute_, "end_date=", str(stop_here))
						else:

							scheduler.add_job(start_job, 'cron', id = "start_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=str(list_every[i][0]), hour=starthour_, minute=startminute_, end_date= str(stop_here))
							scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=str(list_every[i][0]), hour=endhour_, minute=endminute_, end_date= str(stop_here))

							print("scheduler add 0: ", "start_job", "id = ", "start_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", starthour_, "minute=", startminute_, "end_date=", str(stop_here))
							print("scheduler add 0: ", "stop_job", "id = ", "stop_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", endhour_, "minute=", endminute_, "end_date=", str(stop_here))
				
				if not (j==0 or j==len(cron_start_stop[i])):

					if(add_cron_job(sep_list[0],stop_here[0:10])):
						stop_here = cron_start_stop[i][j][0]
						start_here = cron_start_stop[i][j-1][1]

						print("start_here in j=", j, start_here)
						print("stop_here in j=", j, stop_here,"\n")
						
						

						if "-" in list_every[i][0]:
							sep_list = split_intervall_days(list_every[i][0])

							scheduler.add_job(start_job, 'cron', id = "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[0], hour=starthour_, minute=startminute_, start_date = start_here, end_date = stop_here)
							scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[1], hour=endhour_, minute=endminute_, start_date = start_here, end_date = stop_here)
						
							print("scheduler add 1 with -: ", "start_job", "id = ", "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[0], "hour=", starthour_, "minute=", startminute_, "start_date =", str(start_here), "end_date=", str(stop_here))
							print("scheduler add 1 with -: ", "stop_job", "id = ", "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[1], "hour=", endhour_, "minute=", endminute_, "start_date =", str(start_here), "end_date=", str(stop_here))

						else:

							scheduler.add_job(start_job, 'cron', id = "start_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=list_every[i][0], hour=starthour_, minute=startminute_, start_date = start_here, end_date = stop_here)
							scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=list_every[i][0], hour=endhour_, minute=endminute_, start_date = start_here, end_date = stop_here)

							print("scheduler add 1: ", "start_job", "id = ", "start_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", starthour_, "minute=", startminute_, "start_date =", str(start_here), "end_date=", str(stop_here))
							print("scheduler add 1: ", "stop_job", "id = ", "stop_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", endhour_, "minute=", endminute_, "start_date =", str(start_here), "end_date=", str(stop_here))

			start_here = cron_start_stop[i][-1][1]
			print("start_here in j=", j, start_here,"\n")
					

			if "-" in list_every[i][0]:
				sep_list = split_intervall_days(list_every[i][0])

				scheduler.add_job(start_job, 'cron', id = "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[0], hour=starthour_, minute=startminute_, start_date = str(start_here))
				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[1], hour=endhour_, minute=endminute_, start_date = str(start_here))
				
				print("scheduler add 2 with -: ", "start_job", "id = ", "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[0], "hour=", starthour_, "minute=", startminute_, "start_date =", str(start_here))
				print("scheduler add 2 with -: ", "stop_job", "id = ", "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[1], "hour=", endhour_, "minute=", endminute_, "start_date =", str(start_here))

			else:
				scheduler.add_job(start_job, 'cron', id = "start_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=list_every[i][0], hour=starthour_, minute=startminute_,  start_date = str(start_here))
				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=list_every[i][0], hour=endhour_, minute=endminute_, start_date = str(start_here))

				print("scheduler add 2: ", "start_job", "id = ", "start_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", starthour_, "minute=", startminute_, "start_date =", str(start_here))
				print("scheduler add 2: ", "stop_job", "id = ", "stop_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", endhour_, "minute=", endminute_, "start_date =", str(start_here))
		else:

			print("Adding cron job \"Every "+str(list_every[i][0])+"\" without intersections of exception days.")

			if "-" in list_every[i][0]:
				sep_list = split_intervall_days(list_every[i][0])

				scheduler.add_job(start_job, 'cron', id = "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[0], hour=starthour_, minute=startminute_)
				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), day_of_week=sep_list[1], hour=endhour_, minute=endminute_)
				
				print("scheduler add 3 with -: ", "start_job", "id = ", "start_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[0], "hour=", starthour_, "minute=", startminute_)
				print("scheduler add 3 with -: ", "stop_job", "id = ", "stop_job_"+str(sep_list[0])+"-"+str(sep_list[1])+"_"+randID(), "day_of_week=",sep_list[1], "hour=", endhour_, "minute=", endminute_)


			else:
				scheduler.add_job(start_job, 'cron', id = "start_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=str(list_every[i][0]), hour=starthour_, minute=startminute_)
				scheduler.add_job(stop_job, 'cron', id = "stop_job_"+str(list_every[i][0])+"_"+randID(), day_of_week=str(list_every[i][0]), hour=endhour_, minute=endminute_)

				print("scheduler add 3: ", "start_job", "id = ", "start_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", starthour_, "minute=", startminute_)
				print("scheduler add 3: ", "stop_job", "id = ", "stop_job_"+str(list_every[i][0])+"_"+randID(), "day_of_week=",list_every[i][0], "hour=", endhour_, "minute=", endminute_)


	print("Final datetimes list: ", new_list_exceptions)

	for i in new_list_exceptions:

		if(len(i)==41):	
			first_ = str(i)[0:19]
			first_ = first_.replace('T', ' ')
			second_ = str(i)[22:42]
			second_ = second_.replace('T', ' ')
		else:
			print("No available time format.")

		first_ = datetime.datetime.strptime(first_, '%Y-%m-%d %H:%M:%S')
		second_ = datetime.datetime.strptime(second_, '%Y-%m-%d %H:%M:%S')
		
		jobStart = scheduler.add_job(start_job, id = "start_job_"+randID(), trigger='date', next_run_time=str(first_))
		jobStop = scheduler.add_job(stop_job, id = "stop_job_"+randID(), trigger='date', next_run_time=str(second_))