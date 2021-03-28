// Access variables


function playPause(i) {
    var playlist_item = document.getElementsByClassName("playlist-item")[i];
    var fa_play_circle = playlist_item.firstElementChild;
    if (fa_play_circle.className === "fa fa-play-circle fa-lg") {
        fa_play_circle.className = fa_play_circle.className.replace(/\bfa-play-circle\b/g, "fa-pause");
    } else if (fa_play_circle.className === "fa fa-pause fa-lg") {
        fa_play_circle.className = fa_play_circle.className.replace(/\bfa-pause\b/g, "fa-play-circle");
    }

}
/*------------ JS for video_gallery in ressource-file --------------*/
var bigScreen = document.getElementById('video-screen');

[...document.querySelectorAll('.frameDummy')].forEach(function(item) {
    item.addEventListener('click', function() {
        var src_to_play = item.previousElementSibling.src;
        console.log(src_to_play);
        bigScreen.src = src_to_play;
    });
});