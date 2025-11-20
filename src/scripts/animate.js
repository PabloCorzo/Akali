var images = ['static/imagenes/casino_raccoon.jpg', 'static/imagenes/pergamino.jpeg'];

var pic = images[0]
var pic2 = images[1]


function TimerSwitch(pic) {
TimerRunning=true;
var timer = setTimeout(SwitchPic(pic), 4000);
}
function SwitchPic(pic) {
pic.src = pic2.jpg;
}
