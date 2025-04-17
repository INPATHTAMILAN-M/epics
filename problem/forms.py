# forms.py
from django import forms
from .models import Student

class StudentInitialForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['teamleader_name', 'department', 'email', 'year']

from django import forms
from .models import Student

# forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'teamleader_name',
            'department',
            'email',
            'year',
            'problem_solution',
        ]
        widgets = {
            'teamleader_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'department':        forms.Select    (attrs={'class': 'form-select'}),
            'email':             forms.EmailInput(attrs={'class': 'form-control'}),
            'year':              forms.Select    (attrs={'class': 'form-select'}),
            'problem_solution':  forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
