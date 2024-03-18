from django import forms

class UserPreferenceForm(forms.Form):
    amplify_user_id = forms.CharField(max_length=255)
    age = forms.IntegerField(required=False)
    location = forms.CharField(max_length=255, required=False)
    education = forms.CharField(max_length=255, required=False)
    profession = forms.CharField(max_length=255, required=False)
    height = forms.CharField(max_length=255, required=False)
    weight = forms.CharField(max_length=255, required=False)
