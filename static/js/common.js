$(document).ready(function () {
    $(".carousel").carousel({
        interval: 7500
    });
    $(".owl-carousel").owlCarousel({
        margin: 10,
        responsiveClass: true,
        responsive: {
            0: {
                items: 2,
                nav: false,
                loop: false,
            },
            576: {
                items: 3,
                nav: false,
                loop: false,
            },
            768: {
                items: 4,
                nav: false,
                loop: false,
            },
            992: {
                items: 4,
                nav: false,
                loop: false,
            },
            1200: {
                items: 6,
                nav: false,
                loop: false,
            },
        },
    });
});