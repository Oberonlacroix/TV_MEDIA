from django import forms

class UploadFileForm(forms.Form):
    custom_filename = forms.CharField(label='File Name', max_length=100)
    file = forms.FileField(label='Upload File', widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 20px;'}))
    
