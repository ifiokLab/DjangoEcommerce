


let element = document.getElementById('sidebar');
function ToggleMobileNavigation(){
    element.classList.toggle('active');
}



var password = document.getElementById('password');
var toggle = document.getElementById('toggle');

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