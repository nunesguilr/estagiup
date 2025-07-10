// Espera todo o conteúdo do HTML ser carregado antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    const body = document.querySelector('body'),
          sidebar = document.querySelector('.sidebar'),
          toggle = document.querySelector(".toggle"),
          searchBtn = document.querySelector(".search-box"),
          modeSwitch = document.querySelector(".toggle-switch"),
          modeText = document.querySelector(".mode-text");

    // Verifica se o botão toggle existe antes de adicionar o evento
    if(toggle) {
        toggle.addEventListener("click" , () =>{
            sidebar.classList.toggle("close");
        });
    }

    // Verifica se o botão de busca existe
    if(searchBtn) {
        searchBtn.addEventListener("click" , () =>{
            sidebar.classList.remove("close");
        });
    }

    // Verifica se o switch de modo existe
    if(modeSwitch) {
        modeSwitch.addEventListener("click" , () =>{
            body.classList.toggle("dark");

            if(body.classList.contains("dark")){
                modeText.innerText = "Light mode";
            }else{
                modeText.innerText = "Dark mode";
            }
        });
    }

});