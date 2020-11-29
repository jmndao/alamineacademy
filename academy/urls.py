from django.urls import path
from . import views as academy_views

urlpatterns = [
    path('', academy_views.HomeView.as_view(), name='homePage'),
    path('about-us/', academy_views.aboutUs, name='aboutUsPage'),
    path('qa/', academy_views.qa, name='qaPage'),
    path('course/<str:feed>', academy_views.CoursesView.as_view(), name='coursePage'),
    # path('course/', academy_views.CoursesView.as_view(), name="coursePage"),
    path('ressource/<str:program>/', academy_views.RessourceView.as_view(), name="ressourcePage"),
]