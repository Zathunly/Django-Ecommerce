document.addEventListener("DOMContentLoaded", function () {
    const carousel = new bootstrap.Carousel(document.querySelector("#bannerCarousel"), {
        interval: 3000, // Set duration in milliseconds
        ride: "carousel", // Enable auto-slide
    });
});
