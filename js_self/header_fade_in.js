window.onload = function() {
    // Get headers and subheaders
    const header1 = document.querySelector(".nav_bar_header1");
    const header2 = document.querySelector(".nav_bar_header2");

    let isHeader1Visible = true; // Initialize the variable

    // Function to toggle between headers
    function toggleHeaders() {
        if (isHeader1Visible) {
            // Show header1, hide header2
            header1.classList.add("show");
            header2.classList.remove("show");
        } else {
            // Show header2, hide header1
            header2.classList.add("show");
            header1.classList.remove("show");
        }

        // Switch between headers after a delay
        isHeader1Visible = !isHeader1Visible;

        // Set up the cycle to repeat every 4 seconds (1s fade + 2s visible)
        setTimeout(toggleHeaders, 4000);
    }

    // Start the toggle cycle after a short delay
    toggleHeaders();
};
