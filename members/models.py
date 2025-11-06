from django.db import models

class Student(models.Model):
    StudentID = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    gender_choices = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    student_image = models.ImageField(upload_to='students/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StudentMark(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam_name = models.CharField(max_length=100, default="10th Public Exam")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.exam_name}"

class SubjectMark(models.Model):
    student = models.ForeignKey(StudentMark, on_delete=models.CASCADE, related_name='subject_marks')
    subject_name = models.CharField(max_length=100)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    pass_fail = models.CharField(
        max_length=10,
        choices=[('Pass', 'Pass'), ('Fail', 'Fail')],
        default='Pass'
    )
    fail_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject_name} - {self.marks_obtained}/{self.max_marks}"
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status_choices = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='Absent')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"