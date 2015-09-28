from django import forms

class SubmitURL(forms.Form):
    url = forms.URLField()
