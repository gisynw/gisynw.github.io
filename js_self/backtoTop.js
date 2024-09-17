
// get the button
const backButton = document.getElementById('backtoTop')
// show the button when scrolled down 20px from the top
window.onscroll = function(){
    if(document.body.scrollTop >20 || document.documentElement.scrollTop >20){
        backButton.style.display = 'block';
    }else{
        backButton.style.display = None
    }
};
// click button
backButton.onclick = function(){
    window.scrollTo({
        top: 0,
        behavior:'smooth'
    })
}
