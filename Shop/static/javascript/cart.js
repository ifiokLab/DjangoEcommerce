 
var num = document.getElementById('num');
var link = document.getElementById('plus').addEventListener('click',cartPlus);
var minus = document.getElementById('minus').addEventListener('click',cartMinus);



function cartPlus(event){
    event.preventDefault();
    val = parseInt(num.value);
    if(val < 100){
    num.value = val + 1;
    }
    else{
    num.value = 100;
    }
}
function cartMinus(event){
   event.preventDefault();
   val = parseInt(num.value);
   if(val > 0){
    num.value = val - 1;
   }
   else{
    num.value = 0;
   }
}
