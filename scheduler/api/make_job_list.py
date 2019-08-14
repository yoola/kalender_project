import datetime
from datetime import date
from datetimerange import DateTimeRange
from api.help_funcs import split_intervall_days, check_insect_with_dates_list
#import arrow --> might be helpful with date conversions



def split_time_range(time_range):

	list_ranges = []
	if "-" in time_range:
		list_ranges = time_range.split(" - ")

		for i in range(0,len(list_ranges)):
			list_ranges[i] = list_ranges[i].replace(" ","")
			list_ranges[i] = list_ranges[i].replace("T"," ")
	return list_ranges



def convert_date_to_number(time_range_str):
	list_ranges = split_time_range(time_range_str)

	date1 =  datetime.datetime.strptime(list_ranges[0][0:10], '%Y-%m-%d')
	date2 =  datetime.datetime.strptime(list_ranges[1][0:10], '%Y-%m-%d')
	delta = date2 - date1

	return [date1.weekday(), date1.weekday()+delta.days]

def convert_every_to_number(day_range_str):

	days_= ["mon","tue","wed","thu","fri","sat","sun"]
	list_splitted = split_intervall_days(day_range_str[0])

	if len(list_splitted) == 2:
		new_list = [days_.index(list_splitted[0]), days_.index(list_splitted[1])]
	else:
		new_list = [days_.index(list_splitted[0]), days_.index(list_splitted[0])]

	return new_list

def get_every_number_list(every_numbers,date_numbers):

	list_every_numbers = []

	if every_numbers[0]>every_numbers[1]:
		every_numbers[1] = every_numbers[1]+7

	list_every_numbers.append([every_numbers[0],every_numbers[1]])

	i = every_numbers[0]
	while i< date_numbers[1]-6:

		every_numbers[0] += 7
		every_numbers[1] += 7
		list_every_numbers.append([every_numbers[0],every_numbers[1]])
		i += 7
	
	return list_every_numbers



def check_intervalls_overlap(date_numbers, every_numbers):

	if date_numbers[0] == every_numbers[0] and date_numbers[1] == every_numbers[1]:
		return "all_the_same"
	if date_numbers[1] == every_numbers[0] and date_numbers[1] < every_numbers[1]:
		return "date_to_the_left" # 2_same_date_to_the_left
	if date_numbers[1] == every_numbers[0] and date_numbers[1] == every_numbers[1]:
		return "date_to_the_left" # 3_same_date_to_the_left
	if date_numbers[0] == every_numbers[1] and every_numbers[0]< date_numbers[0]:
		return "date_to_the_right" # 2_same_date_to_the_right
	if date_numbers[0] == every_numbers[1] and every_numbers[0] == date_numbers[0]:
		return "date_to_the_right" # 3_same_date_to_the_right

	if every_numbers[0] < date_numbers[1] and date_numbers[1] < every_numbers[1] and date_numbers[0]< every_numbers[0]:
		return "date_to_the_left"
	if date_numbers[0] < every_numbers[1] and every_numbers[1] < date_numbers[1] and every_numbers[0]< date_numbers[0]:
		return "date_to_the_right"
	
	if every_numbers[0] < date_numbers[0] and date_numbers[1] < every_numbers[1] and every_numbers[0]<date_numbers[1]:
		return "date_inside"
	if date_numbers[0] < every_numbers[0] and every_numbers[1] < date_numbers[1]:
		return "all_the_same" # date_outside

	if date_numbers[0] == every_numbers[0] and every_numbers[1] < date_numbers[1]:
		return "all_the_same" #start_same_end_date_right
	if date_numbers[0] == every_numbers[0] and date_numbers[1] < every_numbers[1]:
		return "date_to_the_left" #start_same_end_date_left
	if date_numbers[1] == every_numbers[1] and date_numbers[0] < every_numbers[0]:
		return "all_the_same" #end_same_start_date_left
	if date_numbers[1] == every_numbers[1] and every_numbers[0] < date_numbers[0]:
		return "date_to_the_right" #end_same_start_date_right
	

	return "no_intersection"


def process_exception_list(temp_exceptions):

	new_temp_exceptions = [[] for _ in range(len(temp_exceptions))]

	for i in range(0,len(temp_exceptions)):
		print("--new i---")
		for j in range(0,len(temp_exceptions[i])):

			if j == 0:

				new_temp_exceptions[i].append(temp_exceptions[i][j])

			else:

				no_intersection = True
				for k in range(0,len(new_temp_exceptions[i])):

					date_range1 = DateTimeRange(str(temp_exceptions[i][j][0:19]), str(temp_exceptions[i][j][22:41]))
					date_range2 = DateTimeRange(str(new_temp_exceptions[i][k][0:19]), str(new_temp_exceptions[i][k][22:41]))

					if date_range1.is_intersection(date_range2):
						new_range = date_range1.intersection(date_range2)
						new_temp_exceptions[i][k] = str(new_range).replace("T", " ")
						no_intersection = False
				if no_intersection:
					new_temp_exceptions[i].append(temp_exceptions[i][j])

	return new_temp_exceptions


# check list_every and sorted list_exceptions for intersections
# if intersection: make all cron jobs during that time to exceptions
# add cron job until first exception day, add exceptions
# get new exception and look again for intersections
# ...
def split_time_ranges_and_make_job_list(list_exceptions, list_every):

	sorted_list_exceptions = sorted(list_exceptions)


	cron_start_stop = [[] for _ in range(len(list_every))]
	temp_exceptions = [[] for _ in range(len(list_every))]
	new_list_exceptions = []
	found_no_intersection = True
	#cron_start_stop[1].append(("endhere","starthere"))



	for i in range(0,len(sorted_list_exceptions)):
		print("\n---new exception: ",sorted_list_exceptions[i]," ---\n")

		for j in range(0,len(list_every)):

			print("new_list_exceptions: ",new_list_exceptions,"\n")
			print("list_every[j]", list_every[j])

			date_numbers = convert_date_to_number(sorted_list_exceptions[i])
			every_numbers = convert_every_to_number(list_every[j])

			print("exceptions0: ",date_numbers)
			print("every0     : ",every_numbers)

			every_numbers_list = get_every_number_list(every_numbers,date_numbers)

			to_do_list = []
			for k in range(0,len(every_numbers_list)):

				to_do = check_intervalls_overlap(date_numbers,every_numbers_list[k])
				to_do_list.append(to_do)

	
			date_time_start = sorted_list_exceptions[i][0:19].replace("T"," ")
			date_time_end = sorted_list_exceptions[i][22:41].replace("T"," ")
			date_start = sorted_list_exceptions[i][0:10].replace("T"," ")
			date_end = sorted_list_exceptions[i][22:32].replace("T"," ")	
			date_starttime = sorted_list_exceptions[i][11:16]
			date_endtime = sorted_list_exceptions[i][33:38]
			every_starttime = list_every[j][1]
			every_endtime = list_every[j][2]	
			every_starttime_hour = every_starttime[0:2]
			every_starttime_minute = every_starttime[3:5]
			every_endtime_hour = every_endtime[0:2]
			every_endtime_minute = every_endtime[3:5]
			date_time_start2 = datetime.datetime.strptime(date_time_start, '%Y-%m-%d %H:%M:%S')
			date_time_end2 = datetime.datetime.strptime(date_time_end, '%Y-%m-%d %H:%M:%S')

		
			if ("all_the_same" in to_do_list or "date_to_the_right" in to_do_list or 
				"date_to_the_left" in to_do_list or "date_inside" in to_do_list):

				found_no_intersection = False
				print("found_no_intersection set to False")

				if to_do_list[0] == "all_the_same":

					if not (date_starttime  == every_starttime or date_endtime == every_endtime):

						print("I'm adding cron and exception in all the same.")
						cron_start_stop[j].append((str(date_start),str(date_end)))
						new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))

						# if date_starttime  == every_starttime or date_endtime == every_endtime 
						# --> do nothing (cron job goes on, since exception matches cron job)

				elif to_do_list[0] == "date_inside" or (to_do_list[0]=="date_to_the_right" and to_do_list[-1]=="date_to_the_left"):

					print("I'm adding cron and exception in date_inside.")

					every_range_left0 = date_time_start2+datetime.timedelta(days=-(date_numbers[0]-every_numbers_list[0][0]))
					every_range_left0 = every_range_left0.replace(hour=int(every_starttime_hour), minute=int(every_starttime_minute))
					every_range_left1 = date_time_start2.replace(hour=00, minute=00)

					every_range_right0 = (date_time_end2+datetime.timedelta(days=1)).replace(hour=00, minute=00)
					every_range_right1 = date_time_end2+datetime.timedelta(days=every_numbers_list[-1][1]-date_numbers[1])
					every_range_right1 = every_range_right1.replace(hour=int(every_endtime_hour), minute=int(every_endtime_minute))


					if date_starttime == "00:00" and date_endtime == "00:00":
						if len(to_do_list)>1:
							temp_exceptions[j].append(str(every_range_left0)+" - "+str(every_range_right1))
							cron_start_stop[j].append((str(every_range_left0)[:-9],str(every_range_right1)[:-9]))

					elif date_starttime == "00:00":
						temp_exceptions[j].append(str(every_range_left0)+" - "+str(date_time_end))
						temp_exceptions[j].append(str(every_range_right0)+" - "+str(every_range_right1))
						cron_start_stop[j].append((str(every_range_left0)[:-9],str(every_range_right1)[:-9]))

					elif date_endtime == "00:00":
						temp_exceptions[j].append(str(every_range_left0)+" - "+str(every_range_left1))
						temp_exceptions[j].append(str(date_time_start)+" - "+str(every_range_right1))
						cron_start_stop[j].append((str(every_range_left0)[:-9],str(every_range_right1)[:-9]))
					else:
						temp_exceptions[j].append(str(every_range_left0)+" - "+str(every_range_left1))
						temp_exceptions[j].append(str(date_time_start)+" - "+str(date_time_end))
						temp_exceptions[j].append(str(every_range_right0)+" - "+str(every_range_right1))
						cron_start_stop[j].append((str(every_range_left0)[:-9],str(every_range_right1)[:-9]))


				elif to_do_list[0] == "date_to_the_left":

					every_range0 = (date_time_end2+datetime.timedelta(days=1)).replace(hour=00, minute=00)
					every_range1 = date_time_end2+datetime.timedelta(days=every_numbers_list[-1][1]-date_numbers[1])
					every_range1 = every_range1.replace(hour=int(every_endtime_hour), minute=int(every_endtime_minute))

					# cron job should end at every_range0 and start again at date_time_end2
					cron_start_stop[j].append((str(date_start),str(every_range1)[:-9]))

					check4_same_day = every_numbers_list[0][0]-date_numbers[1]
					## add only one exception if there is not pause between the jobs
					if date_endtime == "00:00" and not check4_same_day==0:
						temp_exceptions[j].append(str(date_time_start)+" - "+str(every_range1))

					elif date_endtime == "00:00" and check4_same_day==0:
						new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
						every_range0 = date_time_end2.replace(hour=int(every_starttime_hour), minute=int(every_starttime_minute))
						temp_exceptions[j].append(str(every_range0)+" - "+str(every_range1))
					# add two exceptions if there is a break between the jobs
					else:
						new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
						temp_exceptions[j].append(str(every_range0)+" - "+str(every_range1))
						

				elif to_do_list[0] == "date_to_the_right":

					print("I'm adding cron and exception in date_to_the_right.")

					every_range0 = date_time_start2+datetime.timedelta(days=-(date_numbers[0]-every_numbers_list[0][0]))
					every_range0 = every_range0.replace(hour=int(every_starttime_hour), minute=int(every_starttime_minute))
					every_range1 = date_time_start2.replace(hour=00, minute=00)

					# cron job should end at every_range0 and start again at date_time_end2
					cron_start_stop[j].append((str(every_range0)[:-9],str(date_end)))
					check4_same_day = every_numbers_list[-1][1]-date_numbers[0]
					print("CHECK4444444444: ", check4_same_day)

					## add only one exception if there is not pause between the jobs
					if date_starttime == "00:00" and not check4_same_day==0:
						temp_exceptions[j].append(str(every_range0)+" - "+str(date_time_end))

					elif date_starttime == "00:00" and check4_same_day==0:
						new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
						every_range1 = date_time_start2.replace(hour=int(every_endtime_hour), minute=int(every_endtime_minute))
						temp_exceptions[j].append(str(every_range0)+" - "+str(every_range1))
					# add two exceptions if there is a break between the jobs
					else:
						new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
						temp_exceptions[j].append(str(every_range0)+" - "+str(every_range1))

				else:
					print("I'm adding cron and exception in else.")
					new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
					cron_start_stop[j].append((str(date_start),str(date_end)))

		print("found_no_intersection: ", found_no_intersection)
		if(found_no_intersection):
			print("I'm adding exception but there was no intersection.")
			new_list_exceptions.append(sorted_list_exceptions[i].replace("T", " "))
		found_no_intersection = True
				
	print("cron_start_stop: ",cron_start_stop)
	print("new_list_exceptions: ",new_list_exceptions, "\n")
	print("temp_exceptions: ", temp_exceptions, "\n")

	for i in range(0,len(cron_start_stop)):
		cron_start_stop[i] = sorted(list(set(cron_start_stop[i])))

	temp_exceptions = process_exception_list(temp_exceptions)  #only get intersectiing intervall dates for the same every day intervalls
	for i in range(0,len(temp_exceptions)):
		for j in range(0,len(temp_exceptions[i])):
			new_list_exceptions.append(temp_exceptions[i][j])

	new_list_exceptions = sorted(new_list_exceptions)
	print("cron_start_stop setted and sorted: ",cron_start_stop)
	print("new_list_exceptions sorted: ",new_list_exceptions, "\n")
	print("temp_exceptions processed: ", temp_exceptions, "\n")
	return cron_start_stop, new_list_exceptions