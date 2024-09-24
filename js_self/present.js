// Get the modal
var modal = document.getElementsByClassName("myModal")[0];

// Get the image and insert it inside the modal
var images = document.getElementsByClassName("gallery-img");
var modalImg = document.getElementById("img01");
var h1text = document.getElementById("modal-h1")

// Loop through all gallery images
for (let i = 0; i < images.length; i++) {
    images[i].onclick = function() {
        modal.style.display = "block";
        modalImg.src = this.src;
        h1text.innerHTML = this.alt
    }
}

// Get the <span> element that closes the modal
var close_button = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
close_button.onclick = function() {
    modal.style.display = "none";
}