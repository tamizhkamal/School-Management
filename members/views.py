from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login,logout
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import pandas as pd

from members.models import Student, StudentMark, SubjectMark
# Create your views here.

def home_page(request):
    return render(request, 'index.html')

def topics_detail(request):
    return render(request, 'topics-detail.html')

def topics_list(request):
    return render(request, 'topics-listing.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        password = request.POST.get('pass1')
        # print(email, "<---------------- email")
        # print(password, "<---------------- password")
        
        if User.objects.filter(email = email).exists():
            user = User.objects.filter(email=email).first()
            # print(user, "<---------------- user")
            if check_password(password, user.password):
                
                # print(user.is_superuser, "<------------------------------n is_superuser")                                
                if user.is_superuser:
                    # print("User login !")
                    login(request, user)
                    return redirect('admin_dash')
                
                else:
                    # print("Admin Not approved")
                    messages.error(request, 'Admin Not approved')
                    return redirect('home_page')
                
            else:
                # print("Invalid username or password.")
                messages.error(request, 'Invalid username or password.')
                return redirect('home_page')
        else:
            # print("Username or password does not exist!")
            messages.error(request, 'Username or password does not exist!')
            return redirect('home_page')                   
    return render(request, "login.html")



def logout_view(request):
    logout(request)
    return redirect('home_page')

def admin_dash(request):
    return render(request, 'admin/admin_dash.html')

from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student

def Student_create(request):
    students_list = Student.objects.all().order_by('-id')  # latest first

    # ✅ Handle rows per page dynamically
    try:
        per_page = int(request.GET.get('per_page', 5))
    except ValueError:
        per_page = 5

    page_number = request.GET.get('page')
    paginator = Paginator(students_list, per_page)
    students = paginator.get_page(page_number)

    if request.method == 'POST':
        name = request.POST.get('student_name')
        father_name = request.POST.get('father_name')
        email = request.POST.get('email_id')
        password = request.POST.get('pass1')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        student_image = request.FILES.get('student_image')

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('Student_create')

        student = Student(
            name=name,
            father_name=father_name,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            gender=gender,
            student_image=student_image
        )
        student.save()
        messages.success(request, 'Student created successfully.')
        return redirect('Student_create')

    context = {
        'students': students,
        'per_page': per_page,  # send this to template for dropdown
    }
    return render(request, 'admin/student_create.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student, StudentMark, SubjectMark

def Mark_Management(request):
    query = request.GET.get('q', '')

    marks_list = StudentMark.objects.select_related('user').all()

    if query:
        marks_list = marks_list.filter(
            Q(user__name__icontains=query) |
            Q(user__phone_number__icontains=query) |
            Q(user__email__icontains=query) |
            Q(exam_name__icontains=query)
        )

    # ✅ Handle rows per page dynamically
    try:
        per_page = int(request.GET.get('per_page', 5))
    except ValueError:
        per_page = 5

    page_number = request.GET.get('page')
    paginator = Paginator(marks_list, per_page)
    marks = paginator.get_page(page_number)

    # ✅ Handle POST (create marks)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        exam_name = request.POST.get('exam_name')

        student = get_object_or_404(Student, id=user_id)
        student_mark = StudentMark.objects.create(user=student, exam_name=exam_name)

        subjects = request.POST.getlist('subject_name[]')
        marks_obtained = request.POST.getlist('marks_obtained[]')
        pass_fail = request.POST.getlist('pass_fail[]')
        fail_reason = request.POST.getlist('fail_reason[]')

        for i in range(len(subjects)):
            SubjectMark.objects.create(
                student=student_mark,
                subject_name=subjects[i],
                marks_obtained=marks_obtained[i],
                pass_fail=pass_fail[i],
                fail_reason=fail_reason[i] if pass_fail[i] == 'Fail' else ''
            )

        return redirect('Mark_Management')

    users = Student.objects.all()

    return render(request, 'admin/mark_management.html', {
        'marks': marks,
        'users': users,
        'query': query,
        'per_page': per_page
    })


from django.core.paginator import Paginator
from django.utils import timezone

def Addendance_Management(request):
    students = Student.objects.all()
    today = timezone.now().date()
    

    if request.method == "POST":
        student_name = request.POST.get('student_name')
        attendance_date = request.POST.get('attendance_date') or today
        status = request.POST.get('status')

        # Create attendance only for entered student name
        student_obj = Student.objects.filter(name=student_name).first()
        if student_obj:
            Attendance.objects.create(student=student_obj, date=attendance_date, status=status)

        return redirect('Addendance_Management')

    # Pagination
    attendance_data = Attendance.objects.all().order_by('-id')
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(attendance_data, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/Addendance_Management.html', {
        "data": page_obj,  # Loop variable in template is `data`
        "students": page_obj,  # For pagination controls
        "per_page": per_page,
        'users':students,
        'today': today,
    })

def Student_list(request):
    students_list = Student.objects.all().order_by('-id')  # latest first

    # ✅ Handle rows per page dynamically
    try:
        per_page = int(request.GET.get('per_page', 5))
    except ValueError:
        per_page = 5

    page_number = request.GET.get('page')
    paginator = Paginator(students_list, per_page)
    students = paginator.get_page(page_number)

    return render(request, 'admin/student_list.html', { 'students': students,'per_page': per_page, })

def Student_details(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Get dropdown value (default 5)
    per_page = request.GET.get("per_page", 5)
    try:
        per_page = int(per_page)
    except:
        per_page = 5

    marks_list = StudentMark.objects.filter(user=student).prefetch_related('subject_marks')

    paginator = Paginator(marks_list, per_page)
    page_number = request.GET.get("page")
    marks = paginator.get_page(page_number)

    return render(request, 'admin/student_details.html', {
        'student': student,
        'marks': marks,
        'per_page': per_page,
    })

def import_marks_from_excel_view(request):
    print(">>> import_marks_from_excel_view TRIGGERED <<<")
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            student_id = row.get('Student_ID')
            exam_name = row.get('Test_type', 'Test')

            student = Student.objects.filter(id=student_id).first()
            if not student:
                print(f"Student ID {student_id} not found, skipping row.")
                continue

            student_mark = StudentMark.objects.create(
                user=student,
                exam_name=exam_name
            )

            subjects = ['Tamil', 'English', 'Maths', 'Science', 'Social Science']

            for subject in subjects:
                marks_obtained = row.get(subject, 0)
                status = row.get('Status', 'Pass')
                reason = row.get('Reason', '')

                SubjectMark.objects.create(
                    student=student_mark,
                    subject_name=subject,
                    marks_obtained=marks_obtained,
                    pass_fail=status,
                    fail_reason=reason if status.lower() == 'fail' else ''
                )

        print("Excel import complete!")
        return redirect('Mark_Management')
    
    return render(request, 'Mark_Management.html')

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from .models import StudentMark

def export_marks(request):
    ids = request.GET.get("ids", "")
    export_type = request.GET.get("type", "")

    if not ids:
        return HttpResponse("No records selected", status=400)

    id_list = ids.split(",")
    marks = StudentMark.objects.filter(id__in=id_list).select_related("user").prefetch_related("subject_marks")

    # ✅ EXCEL export already working, so skip
    if export_type == "excel":
        return export_marks_excel(marks)

    # ✅ PDF export section
    if export_type == "pdf":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_marks.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Student Marks Report")
        y -= 30

        pdf.setFont("Helvetica", 10)

        for m in marks:
            pdf.drawString(50, y, f"Student: {m.user.name}  |  Phone: {m.user.phone_number}  |  Exam: {m.exam_name}")
            y -= 20

            pdf.drawString(70, y, "Subject")
            pdf.drawString(220, y, "Marks")
            pdf.drawString(320, y, "Status")
            pdf.drawString(400, y, "Fail Reason")
            y -= 15
            pdf.line(50, y, 550, y)
            y -= 10

            for sub in m.subject_marks.all():
                pdf.drawString(70, y, sub.subject_name)
                pdf.drawString(220, y, f"{sub.marks_obtained} / {sub.max_marks}")
                pdf.drawString(320, y, sub.pass_fail)
                pdf.drawString(400, y, sub.fail_reason or "-")
                y -= 18

                if y < 100:  # auto new page
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 10)

            y -= 10
            pdf.line(50, y, 550, y)
            y -= 25

            if y < 120:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 10)

        pdf.save()
        return response

    return HttpResponse("Invalid export type", status=400)


import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student

def import_student_from_excel_view(request):
    print(">>> import_student_from_excel_view TRIGGERED <<<")
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)

            required_columns = [
                'Name', 'Father_Name', 'Mother_Name',
                'Email_ID', 'Phone', 'Gender', 'Address',
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            print(missing_columns, "<-------------------------------- missing_columns")

            if missing_columns:
                messages.error(request, f"Missing columns in Excel: {', '.join(missing_columns)}")
                return redirect('Student_create')

            created_count = 0
            skipped_count = 0

            # 🔢 Find last used StudentID (auto-increment logic)
            last_student = Student.objects.order_by('-id').first()
            start_id = int(last_student.StudentID) + 1 if last_student and last_student.StudentID.isdigit() else 1

            # Loop through Excel rows
            for index, row in df.iterrows():
                student_id = str(start_id + index)  # Auto Student_ID (1,2,3,...)

                email = str(row.get('Email_ID')).strip()

                # Skip if already exists
                if Student.objects.filter(email=email).exists():
                    print(f"Skipping existing student: {email}")
                    skipped_count += 1
                    continue

                # Create new student
                Student.objects.create(
                    StudentID=student_id,
                    name=row.get('Name', ''),
                    father_name=row.get('Father_Name', ''),
                    mother_name=row.get('Mother_Name', ''),
                    email=email,
                    password=row.get('Password', ''),  # you can hash later
                    phone_number=str(row.get('Phone', '')),
                    address=row.get('Address', ''),
                    gender=str(row.get('Gender', '')).lower(),
                )
                created_count += 1

            messages.success(
                request,
                f"✅ {created_count} students imported successfully! ({skipped_count} skipped)"
            )
            print("Excel import complete!")
            return redirect('Student_create')

        except Exception as e:
            print("Error importing Excel:", e)
            messages.error(request, f"Error importing Excel: {e}")
            return redirect('Student_create')

    return redirect('Student_create')
    # return render(request, 'admin/student_create.html')

def import_attendance_from_excel_view(request):
    print(">>> import_attendance_from_excel_view TRIGGERED <<<")
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)

            # Make column names lowercase and strip spaces
            df.columns = df.columns.str.strip().str.lower()

            required_columns = ['student_id', 'date', 'status']
            missing_columns = [col for col in required_columns if col not in df.columns]


            if missing_columns:
                print("Missing columns in Excel: {', '.join(missing_columns)}")
                messages.error(request, f"Missing columns in Excel: {', '.join(missing_columns)}")
                return redirect('Addendance_Management')

            created_count = 0
            skipped_count = 0

            # Loop through Excel rows
            for index, row in df.iterrows():
                
                student_id = str(row.get('student_id')).strip()
                date = row.get('date')
                status = str(row.get('status')).strip()

                # ✅ Check if student exists
                try:
                    student = Student.objects.get(StudentID=student_id)
                except Student.DoesNotExist:
                    print(f"Student not found: {student_id}")
                    skipped_count += 1
                    continue

                # ✅ Avoid duplicate attendance
                # if Attendance.objects.filter(student=student, date=date).exists():
                #     print(f"Skipping existing attendance for: {student_id} on {date}")
                #     skipped_count += 1
                #     continue

                # ✅ Create attendance record
                Attendance.objects.create(
                    student=student,
                    date=date,
                    status=status,
                )
                created_count += 1

            messages.success(
                request,
                f"✅ {created_count} attendance records imported successfully! ({skipped_count} skipped)"
            )
            print("Attendance Excel import complete!")
            return redirect('Addendance_Management')

        except Exception as e:
            print("Error importing Excel:", e)
            messages.error(request, f"❌ Error importing Excel: {e}")
            return redirect('Addendance_Management')

    return redirect('Addendance_Management')



from django.shortcuts import render, redirect
from .models import Student, Attendance
from django.utils import timezone

def attendance_view(request):
    students = Student.objects.all()
    today = timezone.now().date()

    if request.method == "POST":
        for student in students:
            student_data = request.POST.get('student_name')
            attendance_date = request.POST.get('attendance_date')
            status = request.POST.get('status')
            status_d = request.POST.get(f'status_{student.id}')

            print(student_data,attendance_date,status,status_d,"<-0----------------------------- student_data,attendance_date,status,status_d")
            # Check if attendance already marked
            attendance, created = Attendance.objects.get_or_create(student=student, date=today)
            attendance.status = status
            attendance.save()
        return redirect('attendance')  # redirect back to the same page

    # Get today's attendance if exists
    attendance_data = Attendance.objects.filter(date=today)
    attendance_dict = {att.student.id: att.status for att in attendance_data}

    context = {
        'students': students,
        'attendance_dict': attendance_dict,
        'today': today,
    }
    return render(request, 'attendance.html', context)

