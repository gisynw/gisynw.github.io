
const changebutton = document.querySelector(".change_bk");
const past_experience =  document.querySelectorAll("#p_intro p a");

let back_g = true;

changebutton.onclick = function(){
    past_experience.forEach(link => {
        if (back_g){
            link.classList.add("highlight_e");
        } else{
            link.classList.remove("highlight_e");
        }
    })
    back_g = !back_g;
}