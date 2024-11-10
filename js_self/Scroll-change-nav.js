var cbpAnimatedHeader = (function() {

    var docElem = document.documentElement,
        header = document.querySelector('.navbar-fixed-top'),
        didScroll = false,
        changeHeaderOn = 100;

    function init() {
        window.addEventListener('scroll', function() {
            if (!didScroll) {
                didScroll = true;
                setTimeout(scrollPage, 250);
            }
        });
    }

    function scrollPage() {
        var sy = scrollY();
        if (sy >= changeHeaderOn) {
            header.classList.add('navbar-shrink');
        } else {
            header.classList.remove('navbar-shrink');
        }
        didScroll = false;
    }

    function scrollY() {
        return window.pageYOffset || docElem.scrollTop;
    }

    init();

})();

