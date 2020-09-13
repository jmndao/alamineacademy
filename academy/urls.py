from django.urls import path
from . import views as academy_views

urlpatterns = [
    path('', academy_views.HomeView.as_view(), name='homePage'),
    path('about-us/', academy_views.aboutUs, name='aboutUsPage'),
    path('course/', academy_views.course, name='coursePage'),
    # path('course/', academy_views.CoursesView.as_view(), name="coursePage"),
    path('ressource/<str:ressource_name>/', academy_views.RessourceView.as_view(), name="ressourcePage")
]