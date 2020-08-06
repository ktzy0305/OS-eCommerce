$(document).ready(function () {
    var swiper = new Swiper('.swiper-container', {
        slidesPerView: 6,
        spaceBetween: 0,
        freeMode: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            0: {
                slidesPerView: 2,
            },
            360: {
                slidesPerView: 3,
            },
            640: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 4,
            },
            992: {
                slidesPerView: 5,
            },
            1024: {
                slidesPerView: 6,
            },
        }
    });
});