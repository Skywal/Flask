
var referenceTextToPrint = document.getElementById('referenceTextToPrint');
var printedCorrectText = document.getElementById('printedCorrectText');

var output = document.getElementById('javascriptOutput');

var currentCartPosition = 0;
var startTime = 0;
var keyPressTime = [];
var pressedSymbols = [];
var textRefference = Array.from(referenceTextToPrint.textContent);
var textProgress = [];
var tmElapsed = null;

output.innerHTML = "Ok element was recognized   <br>" + referenceTextToPrint.textContent.length + " your text length <br>";
output.innerHTML = output.innerHTML + textRefference + "<br><br>";
output.innerHTML = output.innerHTML + textRefference.join('');

// https://stackoverflow.com/questions/26329900/how-do-i-display-millisecond-in-my-stopwatch
var timer = document.getElementById("timer");
var timeBegan = null
    , started = null;

function start() {
    if (timeBegan === null){
        timeBegan = new Date();
    }

    started = setInterval(clockRunning, 10);
}

function stopTimer(){
    clearInterval(started);
}

function clockRunning(){
    var currentTime = new Date()
        , timeElapsed = new Date(currentTime - timeBegan)
        , hour = timeElapsed.getUTCHours()
        , min = timeElapsed.getUTCMinutes()
        , sec = timeElapsed.getUTCSeconds()
        , ms = timeElapsed.getUTCMilliseconds();

        timer.innerHTML = 
        (hour > 9 ? hour : "0" + hour) + ":" +
        (min > 9 ? min : "0" + min) + ":" +
        (sec > 9 ? sec : "0" + sec) + ":" +
        (ms > 99 ? ms : ms > 9 ? "0" + ms : "00" + ms);

        tmElapsed = timeElapsed;
}


document.addEventListener('keydown', function(event) {

    output.innerHTML = event.key + "<br>";
    
    if(event.key == textRefference[0]){
        textProgress.push(textRefference.shift());
        pressedSymbols.push(event.key);
        
        keyPressTime.push(tmElapsed);
        
        referenceTextToPrint.innerHTML = textRefference.join('');
        printedCorrectText.innerHTML = textProgress.join('');
    }

    output.innerHTML = output.innerHTML + "<br>" + keyPressTime.at(-1).getUTCHours() +":"+ keyPressTime.at(-1).getUTCMinutes() +":"+ keyPressTime.at(-1).getUTCSeconds() +":"+ keyPressTime.at(-1).getUTCMilliseconds();
});
