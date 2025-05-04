from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Student, Certificate, News, Contact, Registration

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'price')
    list_filter = ('category',)
    search_fields = ('title', 'description')

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1
    verbose_name = "SErtifikat rasmlari"
    verbose_name_plural = "Sertifikat rasmlari"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'rating', 'diploma_number')
    list_filter = ('course__category',)
    search_fields = ('name', 'diploma_number')
    inlines = [CertificateInline]


# @admin.register(Certificate)
# class CertificateAdmin(admin.ModelAdmin):
#     list_display = ('student',)
#     search_fields = ('student__name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','id', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'summary')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')