const grid = document.getElementById("grid");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

menu.addEventListener("click",()=>{
    barraLateral.classList.toggle("max-barra-lateral");
    if(barraLateral.classList.contains("max-barra-lateral")){
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
    }
    else{
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";
    }
    if(window.innerWidth<=320){
        barraLateral.classList.add("mini-barra-lateral");
        main.classList.add("min-main");
        spans.forEach((span)=>{
            span.classList.add("oculto");
        })
    }
});

grid.addEventListener("click",()=>{
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach((span)=>{
        span.classList.toggle("oculto");
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const eliminarForm = document.getElementById('eliminarForm');
    const btnEliminar = document.querySelector('.btnEliminar');

    eliminarForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenimos el envío del formulario por defecto

        swal({
            title: "¿Estás seguro?",
            text: "Una vez eliminado, no podrás recuperar este elemento.",
            icon: "warning",
            buttons: ["Cancelar", "Eliminar"],
            dangerMode: true,
        })
        .then((willDelete) => {
            if (willDelete) {
                // Si el usuario confirma la eliminación, enviamos el formulario
                eliminarForm.submit();
            } else {
                // Si el usuario cancela la eliminación, no hacemos nada
                return false;
            }
        });
    });
});