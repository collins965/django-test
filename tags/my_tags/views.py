from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import mark_safe

import markdown

from my_tags.models import Blog  
# Home view
def index(request): 
    return render(request, 'index.html', {"message": "Welcome to Django"})

# About page
def about(request):
    return render(request, 'about.html')

# Contact page
def contact(request):
    return render(request, 'contact.html')

# Footer (optional view — normally included in base template)
def footer(request):
    return render(request, 'footer_page.html')

# Filter demo page
def filter_demo(request):
    context = {
        "my_string": "hello world",
        "my_date": datetime(2025, 6, 18),
        "long_string": "This is a very long string used for demonstration purposes.",
        "missing_value": None,
        "words_string": "Django templates are powerful and flexible.",
        "list_items": ["Django", "is", "awesome"],
        "multiline_text": "This is line one.\nThis is line two.\nThis is line three.",
    }
    return render(request, 'filters.html', context)

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

# Sign Up
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'signup.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Blog List View with Markdown Rendering
def blog_list(request):
    blogs = Blog.objects.prefetch_related('editors').all()
    for blog in blogs:
        blog.rendered_text = mark_safe(markdown.markdown(blog.text))
    return render(request, 'blog_list.html', {'blogs': blogs})
