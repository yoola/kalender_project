import datetime
from datetimerange import DateTimeRange

def check_intersect_with_dates_list(list_times,test_range):

	print("list_times 0: ",list_times)

	not_set = True
	index_set = 0
	no_intersection = True  
	indices_to_del = []

	if not list_times:
		print("List was empty.\n")
		list_times.append(test_range)
	else:

		for i in range(0,len(list_times)):

			if list_times[i].is_intersection(test_range):
				no_intersection = False
				print("This is an intersection.\n")

				if not_set:
					print("First intersection.\n")
					list_times[i] = list_times[i].encompass(test_range)
					test_range = list_times[i]
					not_set = False 
					index_set = i
					print("First intersect test_range: ", test_range)

				else:
					print("More intersections.\n")
					list_times[index_set] = list_times[i].encompass(test_range)
					test_range = list_times[index_set]
					indices_to_del.append(i)

		if(no_intersection):
			print("No intersection\n")
			list_times.append(test_range)

	for i in indices_to_del:
		del list_times[i]

	print("list_times: ",list_times)

	return list_times


def join_list_dates(list_exceptions):

	for i in list_exceptions:
		print(i)

	print("list_exceptions: ", list_exceptions)

	return list_exceptions
	

def split_intervall_days(day):
	if "-" in day:
		list_days = day.split("-")
		for i in range(0,len(list_days)):
			list_days[i] = list_days[i].replace(" ","")
		return list_days
	return [day]

def change_24_to_00(date1):

	if date1[11:13] == "24":
		date1 = date1.replace("24","00")
		date1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
		date1 = date1 + datetime.timedelta(days=1)
	else:
		date1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
	return date1


def every_change_24_to_00_end(test_day,test_day_start, test_day_end):

	list_days = ["mon","tue","wed","thu","fri","sat","sun","mon"]
	splitted_day = split_intervall_days(test_day)

	if len(splitted_day) == 2:
		test_day = splitted_day[1]
		index = list_days.index(test_day)
		test_day = splitted_day[0] +"-"+ list_days[index+1]
		test_day_end = "00:00"
	else:
		test_day = splitted_day[0]
		index = list_days.index(test_day)
		test_day = test_day +"-"+ list_days[index+1]
		test_day_end = "00:00"

	return (test_day, test_day_start, test_day_end)



# Also remember to cancel it in add_my_jobs

#print(every_change_24_to_00_end("mon","08:00","24:00"))



def get_day_of_Every(everyday):

	if everyday == "Every Monday":
		return "mon"
	if everyday == "Every Tuesday":
		return "tue"
	if everyday == "Every Wednesday":
		return "wed"
	if everyday == "Every Thursday":
		return "thu"
	if everyday == "Every Friday":
		return "fri"
	if everyday == "Every Saturday":
		return "sat"
	if everyday == "Every Sunday":
		return "sun"

def are_proceeding_days(test_day, day):

	#print("test_day: ", test_day)
	# if isinstance(day, list):
	# 	day = day[0]
	#print("day: ", day)
	
	if test_day == "mon":
		if day == "sun":
			return "proceeding"
		if day == "tue":
			return "previous"
		if day == "mon":
			return "same"

	if test_day == "tue":
		if day == "mon":
			return "proceeding"
		if day == "wed":
			return "previous"
		if day == "tue":
			return "same"

	if test_day == "wed":
		if day == "tue":
			return "proceeding"
		if day == "thu":
			return "previous"
		if day == "wed":
			return "same"

	if test_day == "thu":
		if day == "wed":
			return "proceeding"
		if day == "fri":
			return "previous"
		if day == "thu":
			return "same"

	if test_day == "fri":
		if day == "thu":
			return "proceeding"
		if day == "sat":
			return "previous"
		if day == "fri":
			return "same"

	if test_day == "sat":
		if day == "fri":
			return "proceeding"
		if day == "sun":
			return "previous"
		if day =="sat":
			return "same"

	if test_day == "sun":
		if day == "sat":
			return "proceeding"
		if day == "mon":
			return "previous"
		if day == "sun":
			return "same"
	return None


def is_same_day_intersection(test_day_start, test_day_end, day_start, day_end):

	if day_start <= test_day_end and test_day_end <= day_end and test_day_start<= day_start:
		return True
	if test_day_start <= day_end and day_end <= test_day_end and day_start<= test_day_start:
		return True
	if test_day_start <= day_start and day_end <= test_day_end:
		return True
	if day_start <= test_day_start and test_day_end <= day_end:
		return True
	return False


def encompass_same_day(test_day_start, test_day_end, day_start, day_end):

	if day_start <= test_day_end and test_day_end <= day_end and test_day_start<= day_start:
		return test_day_start, day_end
	if test_day_start <= day_end and day_end <= test_day_end and day_start<= test_day_start:
		return day_start, test_day_end
	if test_day_start <= day_start and day_end <= test_day_end:
		return test_day_start, test_day_end
	if day_start <= test_day_start and test_day_end <= day_end:
		return day_start, day_end
	else:
		return "Case not listed"



def join_days(test_day, test_day_start, test_day_end, list_day, day_start, day_end):

	to_do = "dont_join"

	if are_proceeding_days(test_day, list_day) == "previous":
		if test_day_end == "24:00" and day_start == "00:00":
			to_do = "join_with_proceeding_day"
			print("to do: ", to_do)

	if are_proceeding_days(test_day, list_day) == "proceeding":
		if test_day_start == "00:00" and day_end == "24:00":
			to_do = "join_with_previous_day"
			print("to do: ", to_do)

	if are_proceeding_days(test_day, list_day) == "same":
		if is_same_day_intersection(test_day_start, test_day_end, day_start, day_end):
			to_do = "join_same_day"
			print("to do: ", to_do)
	return to_do




def join_intervall_days(test_day, test_day_start, test_day_end, list_days, day_start, day_end):

	if len(list_days) == 2:
		print("len: ", len(list_days))
		if join_days(test_day, test_day_start, test_day_end, list_days[0], day_start, day_end) == "join_with_proceeding_day":
			list_days[0] = test_day
			day_start = test_day_start
			list_days = list_days[0]+"-"+list_days[1]
		
		if join_days(test_day, test_day_start, test_day_end, list_days[1], day_start, day_end) == "join_with_previous_day":
			list_days[1] = test_day
			day_end = test_day_end
			list_days = list_days[0]+"-"+list_days[1]


		if join_days(test_day, test_day_start, test_day_end, list_days[0], day_start, day_end) == "join_same_day":
			day_start, day_end = encompass_same_day(test_day_start, test_day_end, day_start, day_end)
			list_days = list_days[0]+"-"+list_days[1]

		if join_days(test_day, test_day_start, test_day_end, list_days[1], day_start, day_end) == "join_same_day":
			day_start, day_end = encompass_same_day(test_day_start, test_day_end, day_start, day_end)
			list_days = list_days[0]+"-"+list_days[1]

			
	if len(list_days) == 1:

		if join_days(test_day, test_day_start, test_day_end, list_days[0], day_start, day_end) == "join_with_proceeding_day":
			list_days.insert(0, test_day)
			day_start = test_day_start
			list_days = list_days[0]+"-"+list_days[1]

		if join_days(test_day, test_day_start, test_day_end, list_days[0], day_start, day_end) == "join_with_previous_day":
			list_days.append(test_day)
			day_end = test_day_end
			list_days = list_days[0]+"-"+list_days[1]

		if join_days(test_day, test_day_start, test_day_end, list_days[0], day_start, day_end) == "join_same_day":
			day_start, day_end = encompass_same_day(test_day_start, test_day_end, day_start, day_end)
			list_days = list_days[0]

	return (list_days, day_start, day_end)



def check_intersect_with_every_list(test_day, test_day_start, test_day_end, List_days):

	not_set = True
	index_set = 0
	no_intersection = True  
	indices_to_del = []

	if not List_days:
		print("List was empty.\n")
		List_days.append((test_day, test_day_start, test_day_end))
	else:

		for i in range(0,len(List_days)):

			list_days = split_intervall_days(List_days[i][0])

			print("Splitted days: ", list_days)
			if len(list_days) == 2:

				if not (join_days(test_day, test_day_start, test_day_end, list_days[0], List_days[i][1], List_days[i][2])=="dont_join"
					and join_days(test_day, test_day_start, test_day_end, list_days[1], List_days[i][1], List_days[i][2])=="dont_join"):


					no_intersection = False

					print("This is an intersection.\n")
					print("The intersecting days are: ")
					print("Test day: ", test_day, test_day_start, test_day_end)
					print("List days: ", list_days, List_days[i][1], List_days[i][2])

					if not_set:
						print("First intersection.\n")
						List_days[i] = join_intervall_days(test_day, test_day_start, test_day_end, list_days, List_days[i][1], List_days[i][2])
						test_day = List_days[i][0]
						test_day_start = List_days[i][1]
						test_day_end = List_days[i][2]
						not_set = False 
						index_set = i
						#print("First intersect test_range: ", test_range)

					else:
						print("More intersections.\n")
						List_days[index_set] = join_intervall_days(test_day, test_day_start, test_day_end, list_days, List_days[i][1], List_days[i][2])
						test_day = List_days[index_set][0]
						test_day_start = List_days[index_set][1]
						test_day_end = List_days[index_set][2]
						indices_to_del.append(i)

			if len(list_days) == 1:

				if not join_days(test_day, test_day_start, test_day_end, list_days[0], List_days[i][1], List_days[i][2])=="dont_join":

					no_intersection = False
					print("This is an intersection.\n")

					if not_set:
						print("First intersection.\n")
						List_days[i] = join_intervall_days(test_day, test_day_start, test_day_end, list_days, List_days[i][1], List_days[i][2])
						test_day = List_days[i][0]
						test_day_start = List_days[i][1]
						test_day_end = List_days[i][2]
						not_set = False 
						index_set = i
						#print("First intersect test_range: ", test_range)

					else:
						print("More intersections.\n")
						List_days[index_set] = join_intervall_days(test_day, test_day_start, test_day_end, list_days, List_days[i][1], List_days[i][2])
						test_day = List_days[index_set][0]
						test_day_start = List_days[index_set][1]
						test_day_end = List_days[index_set][2]
						indices_to_del.append(i)

		if(no_intersection):
			print("No intersection\n")
			List_days.append((test_day,test_day_start, test_day_end))

	for i in indices_to_del:
		del List_days[i]

	return List_days