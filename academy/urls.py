from django.urls import path
from . import views as academy_views

urlpatterns = [
    path('', academy_views.home, name='homePage'),
    path('about-us/', academy_views.aboutUs, name='aboutUsPage'),
    path('course/', academy_views.courses, name="coursePage"),
]