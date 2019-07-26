from api.models import Schedule
from rest_framework import serializers


        # Serializers define the API representation.
class ScheduleSerializer(serializers.ModelSerializer):

	# startday = serializers.CharField(max_length=20)
	# endday = serializers.CharField(required=False, allow_blank=True, max_length=20)
	# starttime = serializers.TimeField()
	# endtime = serializers.TimeField()

	class Meta:
		model = Schedule
		fields = ('startday', 'endday', 'starttime', 'endtime')

	def create(self, validated_data):

		return Schedule.objects.create(**validated_data)

	def update(self, instance, validated_data):

		instance.startday = validated_data.get('startday', instance.startday)
		instance.endday = validated_data.get('endday', instance.endday)
		instance.starttime = validated_data.get('starttime', instance.starttime)
		instance.endtime = validated_data.get('endtime', instance.endtime)
		instance.save()
		return instance