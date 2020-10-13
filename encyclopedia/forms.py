from django import forms

class CreateEntry(forms.Form):
    title = forms.CharField(max_length=10, required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 21, "cols": 65, "placeholder": "Enter Entry Content Here"}))
