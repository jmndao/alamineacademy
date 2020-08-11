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