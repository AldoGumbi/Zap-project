document.getElementById("registra_usuario").addEventListener("click",register)
document.getElementById("inicia_sesion").addEventListener("click",sesion)

let formulario_login = document.querySelector(".formulario_login");
let formulario_register= document.querySelector(".formulario_register");
let caja_login = document.querySelector(".caja_login");
let caja_register= document.querySelector(".caja_register");
let caja_form_login_register = document.querySelector('.caja_form_login_register')



function register(){

    
        formulario_register.style.display="block";
        caja_form_login_register.style.left="410px";
        formulario_login.style.display="none";
        caja_register.style.opacity="0";
        caja_login.style.opacity ="1";
 

}


function sesion(){

   
        formulario_register.style.display="none";
        caja_form_login_register.style.left="10px";
        formulario_login.style.display="block";
        caja_register.style.opacity="1";
        caja_login.style.opacity ="0";
    

}