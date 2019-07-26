from django.conf.urls import url, include
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter(trailing_slash=False)
#router.register(r'schedule', views.APIViewSet, base_name='api')



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^schedule/', views.ScheduleList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)


# from django.urls import path, include

# from rest_framework import routers

# from . import views


# router = routers.SimpleRouter(trailing_slash=False)
# router.register(r'schedule', views.ScheduleList, base_name='api')


# urlpatterns = [
#     path('', include(router.urls))
# ]