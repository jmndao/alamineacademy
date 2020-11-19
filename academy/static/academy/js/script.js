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
/*------------ JS for navigation Bar --------------*/

const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.topnav');
    const nav_link = document.querySelectorAll('.nav-link');

    burger.addEventListener('click', () => {
        nav.classList.toggle('nav-active');

        // Animate links
        nav_link.forEach((link, ind) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${ind / 5 + 0.3}s`
            }
        });

        // Animate burger
        burger.classList.toggle('toggle');
    });
}

navSlide();