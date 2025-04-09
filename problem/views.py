from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import StudentInitialForm, StudentFileForm
from .models import Student, Problem_statement
# Temporary in-memory OTP store
otp_storage = {}
def index(request):
    form = StudentInitialForm()  # 🟢 Define here so it's always available

    if request.method == 'POST':
        if 'team_details' in request.FILES or 'problem_solution' in request.FILES:
            form_file = StudentFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                student_data = request.session.get('student_data')
                if student_data:
                    student = Student(
                        teamleader_name=student_data['teamleader_name'],
                        department=student_data['department'],
                        email=student_data['email'],
                        year=student_data['year'],
                        problem_solution=form_file.cleaned_data['problem_solution'],
                    )
                    student.save()
                    messages.success(request, 'Files submitted successfully!')
                    return redirect('index')
                else:
                    messages.error(request, 'Session expired or invalid. Please fill the form again.')
                    return redirect('index')
        else:
            form = StudentInitialForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                if email.endswith('@karpagamtech.ac.in'):  # Ensure email ends with karpagamtech.ac.in
                    otp = str(random.randint(100000, 999999))
                    otp_storage[email] = otp

                    send_mail(
                        'Your OTP for EPICS Application',
                        f'Hello {form.cleaned_data["teamleader_name"]}, your OTP is: {otp}',
                        'noreply@example.com',
                        [email],
                        fail_silently=False,
                    )

                    request.session['student_data'] = form.cleaned_data
                    messages.info(request, 'OTP sent to your email. Please verify to continue.')
                else:
                    messages.error(request, 'Please use an email ending with @karpagamtech.ac.in.')
                  
    # 🔍 Filters from GET parameters
    title_query = request.GET.get('title', '')
    theme_query = request.GET.get('theme', '')
    category_query = request.GET.get('category', '')

    problems = Problem_statement.objects.select_related('theme', 'created_by')
    if title_query:
        problems = problems.filter(title__icontains=title_query)
    if theme_query:
        problems = problems.filter(theme_theme_iexact=theme_query)
    if category_query:
        problems = problems.filter(category__iexact=category_query)

    # Pagination
    paginator = Paginator(problems, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)            
    problems = Problem_statement.objects.select_related('theme', 'created_by')
    total_problems = Problem_statement.objects.count()
    hardware_count = Problem_statement.objects.filter(category='hardware').count()
    software_count = Problem_statement.objects.filter(category='software').count()
    themes = Problem_statement.objects.values_list('theme__theme', flat=True).distinct()
    categories = Problem_statement.objects.values_list('category', flat=True).distinct()
    total_submissions = Student.objects.count()
   

    context = {
        'total_submissions': total_submissions,
        'total_problems': total_problems,
        'hardware_count': hardware_count,
        'software_count': software_count,
        'problems': problems,
        'form': form,
        'file_form': StudentFileForm(),
        'themes': themes,
        'categories': categories,
        
    }
    return render(request, 'index.html', context)



@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_entered = request.POST.get('otp')

        if otp_storage.get(email) == otp_entered:
            student_data = request.session.get('student_data')
            if student_data:
                # Save partial student record (without files yet)
                student = Student(
                    teamleader_name=student_data['teamleader_name'],
                    department=student_data['department'],
                    email=student_data['email'],
                    year=student_data['year'],
                )
                student.save()
                request.session['student_id'] = student.id  # track student ID for file upload
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})



def guidelines(request):
    return render(request, 'guidelines.html')

def timeline(request):
    return render(request, 'timeline.html')




import openpyxl
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ExcelUploadForm
from .models import Problem_statement, Theme, Faculty
from openpyxl import load_workbook

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            wb = load_workbook(excel_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                theme_id, problem_id, title, description, category, created_by_id = row
                
                # Check if the theme_id and created_by_id are valid integers
                try:
                    theme = Theme.objects.get(id=int(theme_id))
                    created_by = Faculty.objects.get(id=int(created_by_id))

                    # Create a new Problem Statement instance
                    problem_statement = Problem_statement(
                        theme=theme,
                        problem_id=problem_id,
                        title=title,
                        description=description,
                        category=category,
                        created_by=created_by
                    )
                    problem_statement.save()

                except ValueError:
                    messages.error(request, f"Invalid ID in row {row}. Please ensure theme_id and created_by_id are valid numbers.")
                    continue
                except Theme.DoesNotExist:
                    messages.error(request, f"Theme with ID {theme_id} does not exist in row {row}.")
                    continue
                except Faculty.DoesNotExist:
                    messages.error(request, f"Faculty with ID {created_by_id} does not exist in row {row}.")
                    continue
            
            messages.success(request, 'Excel file successfully uploaded!')
            return redirect('upload_excel')  # Redirect after success

    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})


