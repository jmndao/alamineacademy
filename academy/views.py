from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import YoutubeVideos


class RessourceView(ListView):
    
    template_name = 'academy/ressource2.html'
    context_object_name = 'videos'
    model = YoutubeVideos
    paginate_by = 9
    
    
    def get_queryset(self):
        ressource_name = self.kwargs['ressource_name']
        
        if YoutubeVideos.objects.get(playlist__title__iexact=ressource_name):
            result = YoutubeVideos.objects.filter(playlist__title__iexact=ressource_name)
        elif YoutubeVideos.objects.get(playlist__title__contains=ressource_name):
            result = YoutubeVideos.objects.filter(playlist__title__contains=ressource_name)
        elif YoutubeVideos.objects.get(title__iexact=ressource_name):
            playlist_title = YoutubeVideos.objects.get(title__iexact=ressource_name)['playlist']
            result = YoutubeVideos.objects.filter(playlist__title=playlist_title)
        elif YoutubeVideos.object.get(title__contains=ressource_name):
            playlist_title = YoutubeVideos.objects.get(title__contains=ressource_name)
            result = YoutubeVideos.objects.filter(playlist__title=playlist_title)
        
        return result
    
    
    
class HomeView(ListView):
    
    template_name = 'academy/index.html'
    context_object_name = 'videos'
    model = YoutubeVideos
    
    def get_queryset(self, **kwargs):
        result = YoutubeVideos.objects.all()[:10]
        return result
    
    
    
    
# class CoursesView(ListView):
    
#     template_name = 'academy/course.html'
    
def course(request):
    return render(request, 'academy/course.html', context={})

def aboutUs(request):
    return render(request, 'academy/aboutUs.html', context={})
