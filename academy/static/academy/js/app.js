$('.slick_slider').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 2,
    arrows: true,
    dots: true,
    centerPadding: '60px',
    centerMode: true,
    autoplay: true,
    autoplaySpeed: 2000,
});

/*------- Smooth scrolling behavior ---------*/

$(document).ready(function() {
    // Add smooth scrolling to all links
    $("a").on('click', function(event) {

        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function() {

                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });
        } // End if
    });
});


/*------------ Video playing -------------*/

// CreateVideoNOde

var video_node = document.createElement("VIDEO");
var source_node = document.createElement("SOURCE");
video_node.id = "about_us_video";
source_node.src = "academy/img/video.mp4";
source_node.type = "video/mp4";
video_node.appendChild(source_node);
console.log(video_node);
// Get the video
var video = document.getElementById("about_us_video");

// Get the button
var btn = document.getElementById("play_video");

// Get the btn image
var img_btn = document.getElementById("play_video_img");

// The div where to do the exchange
var div = document.getElementsByClassName("about_us_video_section")[0];
// Get the image to replace
var img = document.getElementById("about_us_image");
// Pause and play the video, and change the button text
function playVideo() {
    if (video_node.paused) {
        div.replaceChild(video_node, img);
        video_node.controls = true;
        btn.removeChild(img_btn);
        video_node.play();
    }
    // } else {
    //     video_node.pause();
    //     img_btn.src = "img/play_video_icon.jpg";
    // }
}

// When the user scrolls the page, execute myFunction
window.onscroll = function() { myFunction() };

function myFunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}