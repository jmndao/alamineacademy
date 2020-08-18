import re 

from django.views.generic import ListView, DetailView
from django.shortcuts import render

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
        #__dict__ for tracking videos of a playlist as well the opposite
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
        req = self._yt_instance.playlists().list(
            part="snippet, player",
            channelId=self.channel_id
        )
        resp = req.execute()
        # Treat the response so that it'll be suitable to
        # put in context
        # index_context : __dict__(kink, id, snippet, channelId,
        #                 title, description, thumbnails, channelTitle,
        #                 localized, player)
        index_context = resp["items"]
        return self.add_url(index_context)
    
    def digest_for_ressource(self, ressource):
        ressource = ressource.lower()
        video_ids = []
        
        playlist_req = self._yt_instance.playlists().list(
            part="snippet, player",
            channelId=channel_id
        )
        playlist_res = playlist_req.execute()
        playlists = playlist_res["items"]
        # Let's pick up ids of playlists so that we can 
        # loop through to get videos from
        for playlist in playlists:
            
            playlistId = playlist["id"]
            playlistTitle = (playlist["snippet"]["title"]).strip()
            
            playlistItems_req = self._yt_instance.playlistItems().list(
                part="contentDetails, snippet",
                playlistId=playlistId
            )
            
            self._id_playlistTitle.update({playlistId: playlistTitle})
            
            playlistItems_res = playlistItems_req.execute()
            playlistItems = playlistItems_res["items"]
            
            self._playlist_titles.append(playlistTitle)
            
            for playlistItem in playlistItems:
                playlistItem_playlistId = playlistItem["snippet"]["playlistId"]
                playlistItem_videoId = playlistItem["contentDetails"]["videoId"]
                
                self._videoId_playlistId.update({playlistItem_videoId: playlistItem_playlistId})
                
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
                videoTitle : {'id' : videoId,
                              'description' : video_description,
                              'url' : self.search_url(video)
                             }
                })
        

        for v_title, _ in self._videos.items():
            id_playlistTitle = self._id_playlistTitle[self._videoId_playlistId[self._videoTitle_videoId[v_title]]]
            self._videoTitle_playlist.update({v_title: id_playlistTitle})
            self._playlistTitle_videos.update({id_playlistTitle: []})
            
        for v_title, g in self._videos.items():
            id_playlistTitle = self._id_playlistTitle[self._videoId_playlistId[self._videoTitle_videoId[v_title]]]
            current_playlist = self._videoTitle_playlist[v_title]
            (self._playlistTitle_videos[current_playlist]).append({'title':v_title, 'description':g["description"], 'url':g["url"]})
        
        print("playlistTitle: ",self._playlistTitle_videos)
        print()
        
        for (v_title, p_title) in zip(self._videos_titles, self._playlist_titles):
            vv_title, pp_title = v_title.lower(), p_title.lower()
            if ressource == pp_title or ressource in pp_title \
                or ressource.startswith(pp_title[:startswith_number]):
                return {"is_video" : False,
                        "playlist" : p_title,
                        "ressource": self._playlistTitle_videos[p_title]}
            elif ressource == vv_title or ressource in vv_title \
                or ressource.startswith(vv_title[:startswith_number]):
                # Playlist in which the videos is contained
                # pl =  self._video_playlist[v_title]
                # for vds in self._playlist_video[pl]:
                #     if vds["title"] == v_title:
                return {"is_video" : True, 
                        "playlist": self._videoTitle_playlist[v_title],
                        "ressource" : self._videos[v_title]}
            return {"is_video" : None,
                    "playlist" : None,
                    "ressource" : None}
            
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
    
# class IndexView(ListView):
#     """ Index class """ 
    
#     template_name = "academy/index.html"
#     context_object_name = index_list 
#     queryset = # Use the Youtube API for videos
    
#     def 
    
    
yt_instance = YoutubeApi(api_key=api_key, channel_id=channel_id)

def home(request):

    playlists = yt_instance.digest_for_index()    
    context = {'playlists': playlists}
    return render(request, 'academy/index.html', context)

def aboutUs(request):
    
    return render(request, 'academy/aboutUs.html', context={})

def courses(request):
    
    return render(request, 'academy/course.html', context= {})