from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from .models import Student, Course, News, Contact, Registration
from user.bot import send_contact_message, send_registration_message
import logging
from django.utils.timezone import now

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    logger.debug(f"Request GET params: {request.GET}")
    students = Student.objects.all()
    courses = Course.objects.all()
    
    news_items = News.objects.all().order_by('-date')
    logger.debug(f"News items fetched: {list(news_items.values('id', 'title'))}")
    
    student_category = request.GET.get('student_category', 'all')
    search_query = request.GET.get('search', '')
    active_tab = request.GET.get('tab', 'home')
    news_id = request.GET.get('news_id')
    logger.debug(f"Active tab: {active_tab}, News ID: {news_id}")
    
    # Filter students
    if student_category != 'all':
        students = students.filter(course__id=student_category)
    
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(course__title__icontains=search_query)
        )
    
    # Paginate students
    paginator = Paginator(students, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Handle news detail
    selected_news = None
    if active_tab == 'news_detail' and news_id:
        try:
            selected_news = get_object_or_404(News, id=news_id)
            logger.debug(f"Selected news: {selected_news.title}")
        except:
            logger.error(f"News with ID {news_id} not found")
            messages.error(request, f"Yangilik topilmadi (ID: {news_id}).")
            query_params = urlencode({'tab': 'news'})
            return HttpResponseRedirect(f"{reverse('config:index')}?{query_params}")
    
    # Handle form submissions
    if request.method == 'POST':
        if 'contact_form' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            if not all([name, email, phone, subject, message]):
                messages.error(request, "Barcha maydonlarni to'ldiring.")
            else:
                try:
                    contact = Contact.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        subject=subject,
                        message=message
                    )
                    send_contact_message(name, email, phone, subject, message, contact.created_at)
                    messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
                except Exception as e:
                    logger.error(f"Xatolik contact yuborishda: {e}")
                    messages.error(request, "Xabarni yuborishda xatolik yuz berdi.")
            query_params = urlencode({'tab': 'contact'})
            return HttpResponseRedirect(f"{reverse('config:index')}?{query_params}")
        
        elif 'registration_form' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            course_id = request.POST.get('course')
            
            if not all([first_name, last_name, email, phone, course_id]):
                messages.error(request, "Barcha maydonlarni to'ldiring.")
            else:
                try:
                    course = get_object_or_404(Course, id=course_id)
                    registration = Registration.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        course=course
                    )
                    send_registration_message(first_name, last_name, email, phone, course.title, registration.created_at)
                    messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")
                except Exception as e:
                    logger.error(f"Xatolik ro‘yxatdan o‘tishda: {e}")
                    messages.error(request, "Ro'yxatdan o'tishda xatolik yuz berdi.")
            query_params = urlencode({'tab': 'register'})
            return HttpResponseRedirect(f"{reverse('config:index')}?{query_params}")

    logger.debug(f"Rendering template with selected_news: {selected_news}")
    return render(request, 'index.html', {
        'students': students,
        'courses': courses,
        'news_items': news_items,
        'active_tab': active_tab,
        'student_category': student_category,
        'search_query': search_query,
        'page_obj': page_obj,
        'selected_news': selected_news,
        'news_id': news_id,
    })
