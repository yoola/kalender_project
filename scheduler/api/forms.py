from django import forms

from api.models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('startday', 'endday', 'starttime','endtime',)