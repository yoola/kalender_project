import datetime
from datetimerange import DateTimeRange
from help_funcs import split_intervall_days



list_exceptions =  ["2019-08-08T03:20:00 - 2019-08-08T12:10:00", "2019-08-09T08:00:00 - 2019-08-09T17:15:00"]

list_every = [('mon-thu', '05:10', '16:20'), ('fri', '10:20', '18:10'), ('sat-sun', '12:25', '24:00')]

print("list_exceptions: ",sorted(list_exceptions))
print("list_every: ",list_every)

sorted_exception_list = sorted(list_exceptions)


def split_time_range(time_range):

	list_ranges = []
	if "-" in time_range:
		list_ranges = time_range.split(" - ")

		#print("list ranges: ",list_ranges)
		for i in range(0,len(list_ranges)):
			list_ranges[i] = list_ranges[i].replace(" ","")
			list_ranges[i] = list_ranges[i].replace("T"," ")
	return list_ranges



def convert_date_to_number(time_range_str):
	list_ranges = split_time_range(time_range_str)

	for i in range(0,len(list_ranges)):
		list_ranges[i] = datetime.datetime.strptime(list_ranges[i],'%Y-%m-%d %H:%M:%S').weekday()

	if list_ranges[0] > list_ranges[1]:
		list_ranges[0] = list_ranges[0]-7

	return list_ranges


def convert_every_to_number(day_range_str):

	days_= ["mon","tue","wed","thu","fri","sat","sun"]
	list_splitted = split_intervall_days(day_range_str[0])


	if len(list_splitted) == 2:
		new_list = [days_.index(list_splitted[0]), days_.index(list_splitted[1])]
	else:
		new_list = [days_.index(list_splitted[0]), days_.index(list_splitted[0])]


	if new_list[0] > new_list[1]:
		new_list[0] = new_list[0]-7

	return new_list


# date_numbers = convert_date_to_number(sorted_exception_list[0])
# every_numbers = convert_every_to_number(list_every[0])

# print(date_numbers)
# print(every_numbers)


def check_intervalls_overlap(date_numbers, every_numbers):

	if date_numbers[0] == every_numbers[0] and date_numbers[1] == every_numbers[1]:
		return "all_the_same"
	if date_numbers[1] == every_numbers[0] and date_numbers[1] < every_numbers[1]:
		return "2_same_start_date_left"
	if date_numbers[1] == every_numbers[0] and date_numbers[1] == every_numbers[1]:
		return "3_same_start_date_left"
	if date_numbers[0] == every_numbers[1] and every_numbers[0]< date_numbers[0]:
		return "2_same_end_date_right"
	if date_numbers[0] == every_numbers[1] and every_numbers[0] == date_numbers[0]:
		return "3_same_end_date_right"
	if date_numbers[0] < every_numbers[1] and every_numbers[1] < date_numbers[1] and every_numbers[0]< date_numbers[0]:
		return "date_to_the_right"
	if every_numbers[0] < date_numbers[1] and date_numbers[1] < every_numbers[1] and date_numbers[0]< every_numbers[0]:
		return "date_to_the_left"
	if every_numbers[0] < date_numbers[0] and date_numbers[1] < every_numbers[1]:
		return "date_inside"
	if date_numbers[0] < every_numbers[0] and every_numbers[1] < date_numbers[1]:
		return "date_outside"
	if date_numbers[0] == every_numbers[0] and every_numbers[1] < date_numbers[1]:
		return "start_same_end_date_right"
	if date_numbers[0] == every_numbers[0] and date_numbers[1] < every_numbers[1]:
		return "start_same_end_date_left"
	if date_numbers[1] == every_numbers[1] and date_numbers[0] < every_numbers[0]:
		return "end_same_start_date_left"
	if date_numbers[1] == every_numbers[1] and every_numbers[0] < date_numbers[0]:
		return "end_same_start_date_right"
	
	return "no_intersection"

# print("date_numbers: ", date_numbers)
# print("every_numbers: ", every_numbers)
# print(check_intervalls_overlap(date_numbers,every_numbers))


# check list_every and sorted list_exceptions for intersections
# if intersection: make all cron jobs during that time to exceptions
# add cron job until first exception day, add exceptions
# get new exception and look again for intersections
# ...
def split_time_ranges_and_add_job(list_exceptions, list_every):

	sorted_list_exceptions = sorted(list_exceptions)


	cron_start_stop = [[] for _ in range(3)]
	new_list_exceptions = []
	#cron_start_stop[1].append(("endhere","starthere"))



	for i in range(0,len(sorted_list_exceptions)):
		print("\n---new exception---\n")
		for j in range(0,len(list_every)):

			print("list_every[j]", list_every[j])

			print("exceptions: ",convert_date_to_number(sorted_list_exceptions[i]))
			print("every     : ",convert_every_to_number(list_every[j]))

			date_numbers = convert_date_to_number(sorted_list_exceptions[i])
			every_numbers = convert_every_to_number(list_every[j])

			to_do = check_intervalls_overlap(date_numbers,every_numbers)

			if not to_do == "no_intersection":

				date_time_start = sorted_list_exceptions[i][0:16].replace("T"," ")
				date_time_end = sorted_list_exceptions[i][22:38].replace("T"," ")

				date_start = sorted_list_exceptions[i][0:10].replace("T"," ")
				date_end = sorted_list_exceptions[i][22:32].replace("T"," ")

				date_starttime = sorted_list_exceptions[i][11:16]
				date_endtime = sorted_list_exceptions[i][33:38]
				every_starttime = list_every[j][1]
				every_endtime = list_every[j][2]

				date_time_start = datetime.datetime.strptime(date_time_start+":00", '%Y-%m-%d %H:%M:%S')
				date_time_end = datetime.datetime.strptime(date_time_end+":00", '%Y-%m-%d %H:%M:%S')

				print("date_time_start: ", date_time_start)
				print("date_time_end: ", date_time_end)

				print("date_starttime: ",sorted_list_exceptions[i][11:16])
				print("date_endtime: ",sorted_list_exceptions[i][33:38])
				print("date_start: ",date_start )
				print("date_end: ",date_end )
				print("every_starttime: ",list_every[j][1])
				print("every_endtime: ",list_every[j][2])
				print("to_do: ", to_do)

				if to_do == "all_the_same":

					if not (date_starttime  == every_starttime or date_endtime == every_endtime):

						cron_start_stop[j].append((date_start,date_end))
						new_list_exceptions.append(sorted_list_exceptions[i])

					# if date_starttime  == every_starttime or date_endtime == every_endtime --> do nothing (cron job goes on)


				if to_do == "2_same_start_date_left":
					print("Intersection with first day of invervall job - 2 exceptions added.")

					#"2019-08-08T03:20:00 - 2019-08-08T12:10:00"

					days_to_add = every_numbers[1] - date_numbers[1]

					new_list_exceptions.append(sorted_list_exceptions[i])
					new_list_exceptions.append((date_time_end+datetime.timedelta(days=days_to_add)))

					cron_start_stop[j].append((date_time_start,date_time_end+datetime.timedelta(days=1)))



				if to_do == "3_same_start_date_left":
					print("Intersection with first and last day of invervall job.")

					new_list_exceptions.append(sorted_list_exceptions[i])
					cron_start_stop[j].append((date_time_start,date_time_end+datetime.timedelta(days=1)))

				
	print("cron_start_stop: ",cron_start_stop)
	print("new_list_exceptions: ",new_list_exceptions)


split_time_ranges_and_add_job(list_exceptions, list_every)
