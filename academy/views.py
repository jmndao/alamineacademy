from django.shortcuts import render

# Create your views here.



def home(request):

    return render(request, 'academy/index.html', context = {})

def aboutUs(request):
    
    return render(request, 'academy/aboutUs.html', context={})

def courses(request):
    
    return render(request, 'academy/course.html', context= {})