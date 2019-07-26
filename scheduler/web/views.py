from django.shortcuts import render
from api.models import Schedule
from api.forms import ScheduleForm
from api import serializer
from api.serializer import ScheduleSerializer
from rest_framework.viewsets import GenericViewSet


class WebViewSet(GenericViewSet):

	#queryset=Schedule.objects.all()

	def list(self,request):

		if request.method == 'POST':

			serializer = ScheduleSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		else:
			return render(request, 'web.html', {'request':request})