# forms.py
from django import forms
from .models import Student

class StudentInitialForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['teamleader_name', 'department', 'email', 'year']

class StudentFileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'problem_solution']



from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
