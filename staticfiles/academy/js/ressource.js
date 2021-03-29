var video_urls = document.getElementsByClassName("box_video");
var video_screen = document.getElementById("video-screen");


function drag_up(me) {
    video_screen.src = me.src;
    console.log("Run ! Run ! Run !");
    console.log(me.src);
}