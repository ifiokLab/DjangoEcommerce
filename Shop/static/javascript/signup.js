

var password = document.getElementById('password1');
var toggle = document.getElementById('toggle');


var password2 = document.getElementById('password2');
var toggle2 = document.getElementById('toggle2');

function ShowHide(){
    if(password.type === 'password'){
        password.setAttribute('type','text');
        toggle.classList.add('hide');
    }
    else{
        password.setAttribute('type','password');
        toggle.classList.remove('hide');
    }
}

function ShowHide2(){
    if(password2.type === 'password'){
        password2.setAttribute('type','text');
        toggle2.classList.add('hide2');
    }
    else{
        password2.setAttribute('type','password');
        toggle2.classList.remove('hide2');
    }
}