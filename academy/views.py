import re

from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

# For the Youtube API
from googleapiclient.discovery import build
#
# The API Key
api_key = "AIzaSyAqjBZjzRrfFDW69fU33P81qPQnxwtWPtY"
channel_id = 'UCPpjzn8YiOofk97I8NleXeQ'
# Create your views here.

startswith_number = 5


class YoutubeApi:

    def __init__(self, api_key, channel_id, **kwargs):
        self.api_key = api_key
        self.channel_id = channel_id
        self._version = 'v3'
        self._name = 'youtube'

        if self.api_key is not None:
            self._yt_instance = build(self._name,
                                      self._version,
                                      developerKey=self.api_key
                                      )
        # __dict__ that contains videos as k and a list of
        # [__dict__(id, description, url)] as value
        self._videos = {}
        # __dict__ that contains as k : playlistTitle - v: self._videos
        self._playlistTitle_videos = {}
        # __dict__ for tracking videos of a playlist as well the opposite
        self._id_playlistTitle = {}
        self._videoId_playlistId = {}
        self._videoTitle_videoId = {}
        self._videoTitle_playlist = {}
        # __list__ for VideoIds
        self._videoIds = []
        # list() that will contain all title so that search can be
        # make in it.
        # -- Search for a playlist
        self._playlist_titles = []
        # -- Search for a single video
        self._videos_titles = []

    def digest_for_index(self):
        """ Composing request then receiving the response 
            for the indexPage.
        """
        index_context = []
        nextPageToken = None
        
        while True:
            req = self._yt_instance.playlists().list(
                part="snippet, player",
                channelId=self.channel_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            resp = req.execute()
            # Treat the response so that it'll be suitable to
            # put in context
            # index_context : __dict__(kink, id, snippet, channelId,
            #                 title, description, thumbnails, channelTitle,
            #                 localized, player)
            for item in resp["items"]:
                index_context.append(item)
            nextPageToken = resp.get('nextPageToken')
            
            if not nextPageToken:
                break
        return self.add_url(index_context)

    def digest_for_ressource(self):
        ###################################
        video_ids = []

        # playlists = []
        # nextPageToken = None
        
        # while True:
        #     playlist_req = self._yt_instance.playlists().list(
        #         part="snippet, player",
        #         channelId=self.channel_id,
        #         maxResults=5,
        #         pageToken=nextPageToken
        #     )
        #     playlist_res = playlist_req.execute()
        #     # Treat the response so that it'll be suitable to
        #     # put in context
        #     # index_context : __dict__(kink, id, snippet, channelId,
        #     #                 title, description, thumbnails, channelTitle,
        #     #                 localized, player)
        #     for item in playlist_res["items"]:
        #         playlists.append(item)
        #     nextPageToken = playlist_res.get('nextPageToken')
            
        #     if not nextPageToken:
        #         break
        
        ##################################
        
        playlist_req = self._yt_instance.playlists().list(
            part="snippet, player",
            channelId=channel_id,
            maxResults=10,
        )
        playlist_res = playlist_req.execute()
        
        playlists = playlist_res["items"]
            
        
        # Let's pick up ids of playlists so that we can 
        # loop through to get videos from
        
        for playlist in playlists:

            playlistId = playlist["id"]
            playlistTitle = (playlist["snippet"]["title"]).strip()
            self._id_playlistTitle.update({playlistId: playlistTitle})
            self._playlist_titles.append(playlistTitle)

            playlistItems_req = self._yt_instance.playlistItems().list(
                part="contentDetails, snippet",
                playlistId=playlistId,
                
            )
                
                
            playlistItems_res = playlistItems_req.execute()
            playlistItems = playlistItems_res["items"]
            
            
            for playlistItem in playlistItems:
                playlistItem_playlistId = playlistItem["snippet"]["playlistId"]
                playlistItem_videoId = playlistItem["contentDetails"]["videoId"]
                
                self._videoId_playlistId.update(
                    {playlistItem_videoId: playlistItem_playlistId})

                video_ids.append(playlistItem_videoId)
            self._videoIds.append(video_ids)
                        
        for ids in self._videoIds:
            vid_request = self._yt_instance.videos().list(
                        part="snippet, player",
                        id=','.join(ids)
                    )
            vid_response = vid_request.execute()
            videos = vid_response["items"]
        for video in videos:

            videoTitle = (video["snippet"]["title"]).strip()
            videoId = video["id"]
            video_description = (video["snippet"]["description"]).strip()

            self._videos_titles.append(videoTitle)

            self._videoTitle_videoId.update({videoTitle: videoId})

            self._videos.update({
                videoTitle: {'id': videoId,
                             'description': video_description,
                             'url': self.search_url(video)
                             }
            })

        for v_title, _ in self._videos.items():
            id_playlistTitle = self._id_playlistTitle[self._videoId_playlistId[self._videoTitle_videoId[v_title]]]
            self._videoTitle_playlist.update({v_title: id_playlistTitle})
            self._playlistTitle_videos.update({id_playlistTitle: []})

        for v_title, g in self._videos.items():
            id_playlistTitle = self._id_playlistTitle[self._videoId_playlistId[self._videoTitle_videoId[v_title]]]
            current_playlist = self._videoTitle_playlist[v_title]
            (self._playlistTitle_videos[current_playlist]).append(
                {'title': v_title, 'description': g["description"], 'url': g["url"]})

        # Some print statement
        # print("_Videos\n", self._videos, "\n\n")
        # print("PlaylistTitle_videos\n", self._playlistTitle_videos,"\n\n")
        # print("Id_playlistTitle\n", self._id_playlistTitle,"\n\n")
        # print("_VideoId_playlistId\n", self._videoId_playlistId,"\n\n")
        # print("_VideoTitle_videoId\n", self._videoTitle_videoId,"\n\n")
        # print("_VideoTitle_playlist\n", self._videoTitle_playlist,"\n\n")
        # print("_videoIds\n", self._videoIds, "\n\n")
        # print("_playlist_titles\n", self._playlist_titles, "\n\n")
        # print("_videos_title\n", self._videos_titles, "\n\n")

    def search(self, ressource):
        self.digest_for_ressource()
        ressource = ressource.lower()

        for p_title in self._playlist_titles:
            pp_title = p_title.lower()
            if ressource == pp_title or ressource in pp_title or ressource.startswith(pp_title[:startswith_number]):
                response = {"is_video": False,
                            "playlist": p_title,
                            "a_video": self._playlistTitle_videos[p_title][0],
                            "ressource": self._playlistTitle_videos[p_title]}   
                return response
        for v_title in self._videos_titles:
            vv_title = v_title.lower()
            if ressource == vv_title or ressource in vv_title or ressource.startswith(vv_title[:startswith_number]):
                response = {"is_video": True,
                            "playlist": self._playlistTitle_videos[self._videoTitle_playlist[v_title]],
                            "ressource": self._videos[v_title]}
                return response
        
        response = {"is_video": None,
                    "playlist": None,
                    "ressource": None}
        return response

    def search_url(self, d):
        """ 
            Help to extract videos' or playlists' url.
            Then add it to d of (type: __dict__) 
            -- return : __dict__
        """
        iframe = d["player"]["embedHtml"]
        pattern = re.compile('src="([\w\W])+"')
        sthg = re.search(pattern, iframe)
        src_url = re.split('"', sthg.group())
        url = src_url[1]
        # Old and bad way of doing the process below
        # don't uncomment it.
        # src_url = re.split("\s+", iframe)[3]
        # url = "=".join(re.split("=+", src_url)[1:]).replace('"', '')
        d["player"]["url"] = url
        return url

    def add_url(self, data):

        if isinstance(data, list):
            for d in data:
                self.search_url(d)
        else:
            self.search_url(data)

        return data


yt_instance = YoutubeApi(api_key=api_key, channel_id=channel_id)


# class IndexView(ListView):
#     """ Index class """

#     template_name = "academy/index.html"
#     context_object_name = index_list
#     queryset = # Use the Youtube API for videos

#     def

class RessourceView(ListView):

    template_name = 'academy/ressource.html'

    def get_queryset(self):
        self.ressource_name = self.kwargs["ressource_name"]
        self.ressources = yt_instance.search(self.ressource_name)
        return self.ressources

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page")
        if self.ressources["is_video"] == None:
            context = None
        elif self.ressources["is_video"] == False:
            playlistTitle = self.ressources["playlist"]
            a_video = self.ressources["a_video"]
            videos_with_pagination = super().paginator_class(
                self.ressources["ressource"], 2)
            page_num = videos_with_pagination.num_pages
            videos_requested = videos_with_pagination.get_page(page)
            context = {
                'is_video': False,
                'title': playlistTitle,
                'a_video': a_video,
                'videos': videos_requested,
                'page_num': range(1, page_num+1)
            }
        elif self.ressources["is_video"] == True:
            playlistList_with_pagination = super().paginator_class(
                self.ressources["playlist"], 2)
            playlistList_requested = playlistList_with_pagination.get_page(
                page)
            page_num = playlistList_with_pagination.num_pages
            video = self.ressources["ressource"]
            context = {
                'is_video': True,
                'video': video,
                'playlist': playlistList_requested,
                'page_num': range(1, page_num+1)
            }
        return context

    

class HomeView(ListView):
    
    template_name = 'academy/index.html'
    context_object_name = 'playlists'
    
    def get_queryset(self, **kwargs):
        self.playlists = yt_instance.digest_for_index()
        return self.playlists
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['playlists'] = self.playlists
        return context
    
    
# class CoursesView(ListView):
    
#     template_name = 'academy/course.html'
    
def course(request):
    return render(request, 'academy/course.html', context={})

def aboutUs(request):
    return render(request, 'academy/aboutUs.html', context={})
