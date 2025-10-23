/**
 * Enhanced Carousel Functionality
 * Adds keyboard navigation and improved user experience
 */

$(document).ready(function() {
    // Enhanced carousel functionality
    var $carousel = $('#carousel-example-generic');
    
    // Add keyboard navigation
    $(document).keydown(function(e) {
        if ($carousel.is(':visible')) {
            switch(e.which) {
                case 37: // Left arrow key
                    $carousel.carousel('prev');
                    break;
                case 39: // Right arrow key
                    $carousel.carousel('next');
                    break;
            }
        }
    });
    
    // Add touch/swipe support for mobile
    var startX = 0;
    var startY = 0;
    
    $carousel.on('touchstart', function(e) {
        startX = e.originalEvent.touches[0].clientX;
        startY = e.originalEvent.touches[0].clientY;
    });
    
    $carousel.on('touchend', function(e) {
        if (!startX || !startY) {
            return;
        }
        
        var endX = e.originalEvent.changedTouches[0].clientX;
        var endY = e.originalEvent.changedTouches[0].clientY;
        
        var diffX = startX - endX;
        var diffY = startY - endY;
        
        // Only trigger if horizontal swipe is more significant than vertical
        if (Math.abs(diffX) > Math.abs(diffY)) {
            if (Math.abs(diffX) > 50) { // Minimum swipe distance
                if (diffX > 0) {
                    $carousel.carousel('next');
                } else {
                    $carousel.carousel('prev');
                }
            }
        }
        
        startX = 0;
        startY = 0;
    });
    
    // Add hover pause functionality
    $carousel.hover(
        function() {
            $carousel.carousel('pause');
        },
        function() {
            $carousel.carousel('cycle');
        }
    );
    
    // Add click-to-pause functionality
    $carousel.on('click', function() {
        if ($carousel.data('carousel').interval) {
            $carousel.carousel('pause');
        } else {
            $carousel.carousel('cycle');
        }
    });
    
    // Add visual feedback for controls
    $('.carousel-control').on('click', function() {
        $(this).addClass('clicked');
        setTimeout(function() {
            $('.carousel-control').removeClass('clicked');
        }, 200);
    });
    
    // Add smooth transitions
    $carousel.on('slide.bs.carousel', function() {
        $('.carousel-inner .item').css('transition', 'all 0.6s ease-in-out');
    });
});

// Add CSS for clicked state
var style = document.createElement('style');
style.textContent = `
    .carousel-control.clicked {
        transform: scale(0.95);
        transition: transform 0.1s ease;
    }
    
    .carousel-control {
        cursor: pointer;
    }
    
    .carousel-control:active {
        transform: scale(0.95);
    }
`;
document.head.appendChild(style);
