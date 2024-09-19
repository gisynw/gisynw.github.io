function myFunction(){
    const myTopnav = document.getElementById('nav_bar_ul');
    if (myTopnav.className.includes("responsive")) {
        myTopnav.className = myTopnav.className.replace(" responsive", "");
    } else {
        myTopnav.className += " responsive";
    }
}