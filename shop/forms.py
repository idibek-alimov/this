from django import forms

class SearchForm(forms.Form):
    query = forms.CharField()

class LikeForm(forms.Form):
	like = forms.BooleanField(required=True,
		                      initial=True)
