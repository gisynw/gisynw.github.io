document.addEventListener('DOMContentLoaded', function() {
    const heading1 = document.querySelector('.fade_in h1');
    const heading2 = document.querySelector('.fade_in h2');

    // Show h1 first
    setTimeout(function() {
        heading1.classList.add('show');
    }, 2.5); // Delay before showing h1 (0.5 seconds)

    // Show h2 after h1
    setTimeout(function() {
        heading2.classList.add('show');
    }, 2500); // Delay before showing h2 (2.5 seconds after page load)
});