const listItems = document.querySelectorAll('li[data-image]')
var modal = document.getElementsByClassName("award_pic")[0];
var image = document.getElementById('pop-img')

for (let i = 0; i < listItems.length; i++) {
    listItems[i].onclick = function() {
        modal.style.display = "block";

        const imageSrc = this.getAttribute('data-image');

        image.src =  imageSrc;
    }
}

var close_button = document.getElementsByClassName("close_award")[0];

close_button.onclick = function(){
    modal.style.display = "none"
}

