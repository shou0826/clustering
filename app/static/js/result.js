var btn1 = document.getElementById('btn1');
var btn2 = document.getElementById('btn2');
var btn3 = document.getElementById('btn3');
var btn4 = document.getElementById('btn4');
var btn5 = document.getElementById('btn5');

var cluster1 = document.getElementById('cluster1');
var cluster2 = document.getElementById('cluster2');
var cluster3 = document.getElementById('cluster3');
var cluster4 = document.getElementById('cluster4');
var cluster5 = document.getElementById('cluster5');

btn1.setAttribute('class', 'clicked');
cluster1.classList.remove('hide');

$(document).ready(function(){
    btn1.onclick = function(){
        cluster1.classList.remove('hide')
        cluster2.setAttribute('class', 'hide')
        cluster3.setAttribute('class', 'hide')
        cluster4.setAttribute('class', 'hide')
        cluster5.setAttribute('class', 'hide')
        
        btn1.setAttribute('class', 'clicked')
        btn2.classList.remove('clicked')
        btn3.classList.remove('clicked')
        btn4.classList.remove('clicked')
        btn5.classList.remove('clicked')
    };
})


$(document).ready(function(){
    btn2.onclick = function(){
        cluster2.classList.remove('hide')
        cluster1.setAttribute('class', 'hide')
        cluster3.setAttribute('class', 'hide')
        cluster4.setAttribute('class', 'hide')
        cluster5.setAttribute('class', 'hide')
        
        btn2.setAttribute('class', 'clicked')
        btn1.classList.remove('clicked')
        btn3.classList.remove('clicked')
        btn4.classList.remove('clicked')
        btn5.classList.remove('clicked')
    };
})


$(document).ready(function(){
    btn3.onclick = function(){
        cluster3.classList.remove('hide')
        cluster1.setAttribute('class', 'hide')
        cluster2.setAttribute('class', 'hide')
        cluster4.setAttribute('class', 'hide')
        cluster5.setAttribute('class', 'hide')
        
        btn3.setAttribute('class', 'clicked')
        btn1.classList.remove('clicked')
        btn2.classList.remove('clicked')
        btn4.classList.remove('clicked')
        btn5.classList.remove('clicked')
    };
})


$(document).ready(function(){
    btn4.onclick = function(){
        cluster4.classList.remove('hide')
        cluster1.setAttribute('class', 'hide')
        cluster2.setAttribute('class', 'hide')
        cluster3.setAttribute('class', 'hide')
        cluster5.setAttribute('class', 'hide')
        
        btn4.setAttribute('class', 'clicked')
        btn1.classList.remove('clicked')
        btn2.classList.remove('clicked')
        btn3.classList.remove('clicked')
        btn5.classList.remove('clicked')
    };
})


$(document).ready(function(){
    btn5.onclick = function(){
        cluster5.classList.remove('hide')
        cluster1.setAttribute('class', 'hide')
        cluster2.setAttribute('class', 'hide')
        cluster3.setAttribute('class', 'hide')
        cluster4.setAttribute('class', 'hide')
        
        btn5.setAttribute('class', 'clicked')
        btn1.classList.remove('clicked')
        btn2.classList.remove('clicked')
        btn3.classList.remove('clicked')
        btn4.classList.remove('clicked')
    };
})
