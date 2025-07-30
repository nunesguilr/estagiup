// Espera todo o conteúdo do HTML ser carregado antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    const body = document.querySelector('body'),
          sidebar = document.querySelector('.sidebar'),
          toggle = document.querySelector(".toggle"), // A variável que controla a seta
          searchBtn = document.querySelector(".search-box");

    // ESTE BLOCO FAZ A SETA FUNCIONAR
    // Verifica se o elemento da seta (toggle) existe antes de adicionar o evento
    if(toggle) {
        toggle.addEventListener("click" , () =>{
            sidebar.classList.toggle("close");
        });
    }

    // Este é o código da barra de pesquisa, pode manter para o futuro
    if(searchBtn) {
        searchBtn.addEventListener("click" , () =>{
            sidebar.classList.remove("close");
        });
    }
    
});