// Back To Top Button
// get the button
const backButton = document.getElementById('backtoTop');
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