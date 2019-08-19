from api.models import Schedule
from rest_framework import serializers


class Schedule(object):

	def __init__(self, startday, endday, starttime, endtime):
		self.startday = startday
		self.endday = endday
		self.starttime = starttime
		self.endtime = endtime


# Serializers define the API representation.
class ScheduleSerializer(serializers.Serializer):

	startday = serializers.CharField(max_length=20)
	endday = serializers.CharField(required=False, allow_blank=True, max_length=20)
	starttime = serializers.CharField(max_length=20)
	endtime = serializers.CharField(max_length=20)

	# class Meta:
	# 	model = Schedule
	# 	fields = ('startday', 'endday', 'starttime', 'endtime')

	def create(self, validated_data):

		return Schedule.objects.create(**validated_data)

	def update(self, instance, validated_data):

		instance.startday = validated_data.get('startday', instance.startday)
		instance.endday = validated_data.get('endday', instance.endday)
		instance.starttime = validated_data.get('starttime', instance.starttime)
		instance.endtime = validated_data.get('endtime', instance.endtime)
		instance.save()
		return instance