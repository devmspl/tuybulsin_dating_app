from django import forms

from .models import UserPreference

# class UserPreferenceForm(forms.Form):
#     age_min = forms.IntegerField(required=False)
#     age_max = forms.IntegerField(required=False)
#     location = forms.CharField(max_length=255, required=False)
#     education = forms.CharField(max_length=255, required=False)
#     profession = forms.CharField(max_length=255, required=False)
#     height = forms.CharField(max_length=255, required=False)
#     weight = forms.CharField(max_length=255, required=False)

class UserPreferenceForm(forms.Form):
    class Meta:
        model = UserPreference
        fields = ['user', 'age_min', 'age_max', 'location', 'education', 'profession', 'height', 'weight']
