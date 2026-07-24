$(document).ready(function() {
    $('#slider1, #slider2, #slider3').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        
        // Autoplay settings
        autoplay: true,
        autoplayTimeout: 3500,          
        autoplayHoverPause: true,        
        smartSpeed: 1000,                
        slideTransition: 'cubic-bezier(0.25, 1, 0.5, 1)', 

        responsive: {
            0: {
                items: 1,
                nav: false
            },
            600: {
                items: 3,
                nav: true
            },
            1000: {
                items: 5,
                nav: true
            }
        }
    });
});