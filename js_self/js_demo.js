document.write("Hello Class");

let city = 'Worcester';
city = 'Boston'
document.write(city);

const city2 = 'Boston';
// city2 = 'Dallas'
document.write(city2)

let name = "Nancy";
let age = 18;
let isok = true;
let emptyvalue = null;

let car = {
    name: 'Fiat',
    year:2023,
};

document.write(car.name);

let classes = ['web', 'python'];
document.write(classes[0]);

let seasons = new Array('Spring', 'Summer')
document.write(seasons[1])

function greet(){
    return "good job";
}
document.getElementById('msg').innerHTML = greet();