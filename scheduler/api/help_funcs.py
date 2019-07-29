import datetime
from datetimerange import DateTimeRange
from itertools import cycle

def check_insect_with_dates_list(list_times,test_range):

	print("list_times 0: ",list_times)

	not_set = True
	index_set = 0
	no_intersection = True  
	indices_to_del = []

	if not list_times:
		print("List was empty.\n")
		list_times.append(test_range)
		print("list_times 01: ",list_times)
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

	print("list_times 1: ",list_times)

	for i in indices_to_del:
		del list_times[i]

	print("list_times 2: ",list_times)

	return list_times


def change_24_to_00(end_time):

	if end_time[11:13] == "24":
		end_time = end_time.replace("24","00")

	end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
	end_time = end_time + datetime.timedelta(days=1)

	return end_time

def get_day_of_Every(everyday):

	if everyday == "Every Monday":
		return "mon"
	if everyday == "Every Tuesday":
		return "tues"
	if everyday == "Every Wednesday":
		return "wed"
	if everyday == "Every Thursday":
		return "thurs"
	if everyday == "Every Friday":
		return "fri"
	if everyday == "Every Saturday":
		return "sat"
	if everyday == "Every Sunday":
		return "sun"

def is_intersection_every(day, test_day):

	list_days = cycle(["mon","tues","wed","thurs","fri","sat","sun"])

	day_i = list_days.index(day)
	test_day_i = list_days.index(test_day)

	if day_i == test_day_[i-1]:
		print(" day_i == test_day_i-1")
	if day_i == test_day_i+1:
		print(" day_i == test_day_i+1")
	if day_i == test_day_i:
		print(" day_i == test_day_i")
	else:
		print("No proceeding days")

is_intersection_every("mon","tues")
is_intersection_every("sun","mon")
is_intersection_every("tues", "sat")


# time_range3 = DateTimeRange("2015-03-22 15:03:00", "2015-03-22 16:07:00")

# time_range4 = DateTimeRange("2015-03-22 14:03:00", "2015-03-22 17:07:00")

# time_range5 = DateTimeRange("2015-04-22 14:03:00", "2015-04-22 17:07:00")

# time_range6 = DateTimeRange("2015-04-22 12:03:00", "2015-04-22 14:07:00")

# ["2015-03-22T10:00:00 - 2015-03-22T17:07:00", 
# "2015-04-22T12:03:00 - 2015-04-22T17:07:00", 
# "2015-04-22T12:03:00 - 2015-04-22T14:07:00"]



#list_times = [((time_range1.encompass(time_range2)).encompass(time_range4)).encompass(time_range3), time_range5]
# test_range = time_range6

# print("list times 0: ",list_times)
# print("test_range: ",test_range)


