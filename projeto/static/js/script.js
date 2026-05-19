const cinco = document.getElementById("general-btn");
const dez = document.getElementById("especific-btn");

cinco.addEventListener("click", function() {
    window.location.href = "/cincoArquivos/";
});

dez.addEventListener("click", function(){
  window.location.href = "dezArquivos";
});