from django.contrib import admin

from .models import Schedule

admin.site.register(Schedule)

# def next_run_time_sec(self, obj):
# 	try:
# 		return obj.next_run_time.strftime("%Y-%m-%d")
# 	except AttributeError:
# 		return None
