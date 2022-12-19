

let element = document.getElementById('sidebar');
function ToggleMobileNavigation(){
    element.classList.toggle('active');
}


function show1(){
    let element = document.getElementById('extra-nav-items');
    let icon = document.getElementById('user-chev1');
    if(icon.classList.contains('fa-chevron-down')){
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-up');
    }
    else{
      icon.classList.remove('fa-chevron-up');
      icon.classList.add('fa-chevron-down');
  
    }
   
    element.classList.toggle('active');
  }
  function show2(){
    let element = document.getElementById('extra-nav-items2');
    let icon = document.getElementById('user-chev2');
    if(icon.classList.contains('fa-chevron-down')){
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-up');
    }
    else{
      icon.classList.remove('fa-chevron-up');
      icon.classList.add('fa-chevron-down');
  
    }
   
    element.classList.toggle('active');
  }
  
  