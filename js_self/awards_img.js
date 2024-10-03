const listItems = document.querySelectorAll('li[data-image]')

listItems.forEach(item =>{
    item.addEventListener('click', function(){
        const image = item.getAttribute('data-image');
        openPopup(title, image);
    });
});

function openPopup(image){
    document.getElementById('pop-img').src = image;
    document.getElementById('award_pic').style.display = 'block';
}

var close_button = document.getElementsByClassName("close_award")[0];

close_button.onclick = function(){
    award_pic.style.display = "none"
}

