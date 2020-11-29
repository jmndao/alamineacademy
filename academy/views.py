from django.http import Http404
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404 
from django.core.paginator import Paginator
from .models import (YoutubeVideos,
                     YoutubePlaylistItem,
                     YoutubePlaylist,
                     SupportSingle,
                     SupportCollection,
                     AcademyModel)


def handler404(request, exception):
    context = {}
    response = render(request, "academy/404.html", context=context)
    response.status_code = 404
    return response

class RessourceView(ListView):

    template_name = 'academy/ressource.html'
    context_object_name = "ressource"
    playlistTitle = [(p.title).upper() for p in YoutubePlaylist.objects.all()]
    category = [it[0] for it in YoutubePlaylistItem.CATEGORY_TYPE]

    @staticmethod
    def ressources(program):
        try:
            videos = YoutubeVideos.objects.filter(playlist__title=program.capitalize())
        except Exception as e:
            return None
        return videos


    def get_queryset(self):
        try: 
            page_num = self.request.GET.get("page")
        except Exception as e:
            pass
        self.topUrl = None
        self.results_paginated = None
        # -- self.results is a list that contains the result of the request
        self.results = list()
        # -- list that hold videos until they get paginated in self.results
        self.videos = list()
        # We put in upperCase the requested program
        self.program = (self.kwargs['program']).upper()
        # We have to reassure that if self.program is from category
        # We'd better take videos that belong in the category as it
        # is more general
        if self.program not in RessourceView.category:
            # If it is just a playlist we take the videos
            if self.program in RessourceView.playlistTitle:
                self.videos = RessourceView.ressources(self.kwargs['program'].upper())
                self.topUrl = self.videos[0].videoUrl
                self.results_paginated = Paginator(self.videos, 9)
        else:
            # Now if it is about plural playlists
            self.playlists = YoutubePlaylistItem.objects.filter(category=self.program)
            self.count = self.playlists.count()
            if self.count > 1:
                for playlist in self.playlists:
                    p_title = playlist.playlist.title
                    temp = YoutubeVideos.objects.filter(playlist__title=p_title)
                    for video in temp:
                        self.videos.append(video)
                self.topUrl = self.videos[0].videoUrl
                self.results_paginated = Paginator(self.videos, 9)
            elif self.count == 1:
                p_title = self.playlists[0].playlist.title
                videos = YoutubeVideos.objects.filter(playlist__title=p_title)
                self.topUrl = videos[0].videoUrl
                self.results_paginated = Paginator(videos, 9)
            else:
                raise Http404("No item Founded for %s" %(self.program))
        
        self.results = self.results_paginated.get_page(page_num)
        return self.results
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program_title'] = self.program
        context['nav'] = True
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


class CoursesView(ListView):

    template_name = 'academy/course.html'
    context_object_name = 'courses'
    model = AcademyModel
    
    def get_queryset(self):
        self.feed = None
        self.ind = False
        checklist = AcademyModel.objects.all()
        req_feed = (self.kwargs['feed']).upper()
        if req_feed in AcademyModel.CATEGORY_TYPE:
            try:
                self.feed = AcademyModel.objects.filter(category=req_feed)
            except Exception as e:
                pass
        else:
            self.ind = True
            self.feed = get_object_or_404(AcademyModel, title=self.kwargs['feed'])
        return self.feed
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['feed'] = self.feed
        context['indicative'] = self.ind
        context['this_page'] = True
        return context
            
    

def aboutUs(request):
    return render(request, 'academy/aboutUs.html', context={})

    
def qa(request):
    return render(request, 'academy/qa.html', context={"nav": True})
