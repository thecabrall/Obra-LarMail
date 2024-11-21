from django import forms

class CSVUploadForm(forms.Form):
    arquivo_csv = forms.FileField()