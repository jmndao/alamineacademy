$('.slick_slider').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 2,
    responsive: [{
            breakpoint: 620,
            settings: {
                arrows: true,
                variableWidth: true,
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        },
        {
            breakpoint: 345,
            settings: {
                arrows: true,
                variableWidth: true,
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        }
    ],
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

var video_node = document.createElement("iframe");
video_node.id = "about_us_video";
video_node.style.border = "none";
var source = "https://www.youtube.com/embed/9ErrIkK9Y_s";
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
    btn.addEventListener("click", () => {
        div.replaceChild(video_node, img);
        video_node.src = source + '?autoplay=1 allowfullscreen';
        btn.removeChild(img_btn);
    }, false);
}

// When the user scrolls the page, execute myFunction
window.onscroll = function() { myFunction() };

function myFunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}


function showSubnavContent() {
    const subnavbtn = document.querySelector('.subnavbtn');
    if (subnavbtn.nextElementSibling.className === "subnav-content") {
        subnavbtn.nextElementSibling.className += " subnav_display";
    } else {
        subnavbtn.nextElementSibling.className = "subnav-content";
    }
}

function showSubnavContentQA() {
    const subnavbtn = document.querySelector('.qa');
    if (subnavbtn.nextElementSibling.className === "subnav-content_qa") {
        subnavbtn.nextElementSibling.className += " subnav_display_qa";
    } else {
        subnavbtn.nextElementSibling.className = "subnav-content_qa";
    }
}


function slickSliderToOne(x) {

    if (x.matches) { // If media queries matches
        $('.slick_slider').slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: true,
            dots: false,
            centerPadding: '60px',
            centerMode: true,
            autoplay: true,
            autoplaySpeed: 2000,
        });
    }
}

var x = window.matchMedia("(max-width: 600px)")
x.addEventListener(slickSliderToOne);
slickSliderToOne(x);