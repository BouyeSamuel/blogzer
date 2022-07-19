from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    body = forms.forms.CharField(widget=forms.Textarea)
