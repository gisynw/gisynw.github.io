// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal
var images = document.getElementsByClassName("gallery-img");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var explanationText = document.getElementById("myModal_caption");
var h1text = document.getElementById("modal-h1")

// Loop through all gallery images
for (let i = 0; i < images.length; i++) {
    images[i].onclick = function() {
        modal.style.display = "block";
        modalImg.src = this.src;
        // captionText.innerHTML = this.alt;
        // explanationText.innerHTML = this.alt
        h1text.innerHTML = "More details about " + this.alt
    }
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}