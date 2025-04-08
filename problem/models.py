from django.db import models

# Create your models here.
class Theme(models.Model):
    theme=models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.theme


class Faculty(models.Model):
    name=models.CharField(max_length=225)
    department=models.CharField(max_length=225)
    email=models.EmailField()
    phone=models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Problem_statement(models.Model):
    theme= models.ForeignKey(Theme, on_delete=models.CASCADE)
    problem_id = models.CharField(unique=True, max_length=10)
    title = models.CharField(max_length=225)
    description = models.TextField()
    category = models.CharField(
        choices=[
            ('hardware', 'Hardware'),
            ('software', 'Software')
        ],max_length=20
    )
    created_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
    
class Student(models.Model):
    teamleader_name=models.CharField(max_length=225)
    department=models.CharField( choices=[
            ('AD&DS', 'AI&DS'),
            ('IT', 'IT'),
            ('CSE', 'CSE'),
            ('ECE', 'ECE'),
            ('EEE', 'EEE'),
            ('MECH', 'MECH')
        ],max_length=20)
    email=models.EmailField()
    year=models.CharField( choices=[
            ('1 year', '1 year'),
            ('2 year', '2 year'),
            ('3 year', '3 year'),
            ('4 year', '4 year')
          
        ],max_length=20)
    
    problem_solution=models.FileField(upload_to='problem_solution/')
    
    def __str__(self):
        return self.teamleader_name

