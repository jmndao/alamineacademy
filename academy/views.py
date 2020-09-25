from django.http import Http404
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import render 
from django.core.paginator import Paginator
from .models import (YoutubeVideos,
                     YoutubePlaylistItem,
                     YoutubePlaylist)


def handler404(request, exception):
    context = {}
    response = render(request, "academy/404.html", context=context)
    response.status_code = 404
    return response

class RessourceView(ListView):

    template_name = 'academy/ressource.html'
    context_object_name = "ressource"
    playlistTitle = [(p.title).upper() for p in YoutubePlaylist.objects.all()]

    @staticmethod
    def ressources(program):
        try:
            videos = YoutubeVideos.objects.filter(playlist__title=program.capitalize())
        except Exception as e:
            return None
        return videos


    def get_queryset(self):
        self.topUrl = None
        # -- self.results is a list that contains the result of the request
        self.results = list()
        # -- list that hold videos until they get paginated in self.results
        self.videos = list()
        # We put in upperCase the requested program
        self.program = (self.kwargs['program']).upper()
        # If it is just a playlist we take the videos
        if self.program in RessourceView.playlistTitle:
            self.videos = RessourceView.ressources(self.kwargs['program'].upper())
            if self.videos is not None:
                self.topUrl = self.videos[0].videoUrl
                self.results = Paginator(self.videos, 9)
                
        # Now if it is about plural playlists
        else:
            self.playlists = YoutubePlaylistItem.objects.filter(category=self.program)
            self.count = self.playlists.count()
            if self.count > 1:
                for playlist in self.playlists:
                    p_title = playlist.playlist.title
                    self.videos.append(YoutubeVideos.objects.filter(playlist__title=p_title))
                self.topUrl = self.videos[0][0].videoUrl
                self.results = Paginator([v for vid in self.videos for v in vid], 9)
            elif self.count == 1:
                p_title = self.playlists[0].playlist.title
                videos = YoutubeVideos.objects.filter(playlist__title=p_title)
                self.topUrl = videos[0].videoUrl
                self.results = Paginator(videos, 9)
        return self.results
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program_title'] = self.program
        if self.topUrl:
            context['video_screen_url'] = self.topUrl
        else:
            raise Http404("Problem")
        return context


class HomeView(ListView):

    template_name = 'academy/index.html'
    context_object_name = 'playlists'
    model = YoutubePlaylistItem

    def get_queryset(self, **kwargs):
        result = YoutubePlaylistItem.objects.all()[:10]
        return result


# class CoursesView(ListView):

#     template_name = 'academy/course.html'

def course(request):
    return render(request, 'academy/course.html', context={})


def aboutUs(request):
    return render(request, 'academy/aboutUs.html', context={})
