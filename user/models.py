from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/courses/')
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    rating = models.FloatField()
    birth_year = models.CharField(max_length=4)
    diploma_number = models.CharField(max_length=20)
    diploma_date = models.DateField()
    image = models.ImageField(upload_to='media/students/')
    about = models.TextField()

    def __str__(self):
        return self.name

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    image = models.ImageField(upload_to='media/certificates/')

    def __str__(self):
        return f"{self.student.name} sertifikati"

class News(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='media/news/')
    summary = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.title}"
    

