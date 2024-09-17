// Back To Top Button
// get the button
const backButton = document.getElementById('backtoTop');
// show the button when scrolled down 20px from the top
// window.onscroll = function(){
//     if(document.body.scrollTop >20 || document.documentElement.scrollTop >20){
//         backButton.style.display = 'block';
//     }else{
//         backButton.style.display = 'none';
//     }
// };
// click button
backButton.onclick = function(){
    window.scrollTo({
        top: 0,
        behavior:'smooth'
    })
};


// Display location
const city = 'Worcester';
const state = 'MA';

function displayLocation() {
    document.getElementById("myloc").innerHTML = 'my location is ' + city + ', ' + state;
}
displayLocation();

// Print function
function greet(){
    document.write("hello JS")
    }
greet();

// get luck words
function getmessage(){
    document.getElementById('lucky').textContent = 'best one';
}