document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput');
    const vagasContainer = document.getElementById('vagas-container'); 
    const vagaCards = vagasContainer.getElementsByClassName('vaga-card');

     // Se o container não existir na página, pare o script
    if (!vagasContainer) return; 

    const gridBtn = document.getElementById('grid-view-btn');
    const listBtn = document.getElementById('list-view-btn');

    // Função para ativar o botão correto
    function activateButton(activeBtn) {
        gridBtn.classList.remove('active');
        listBtn.classList.remove('active');
        activeBtn.classList.add('active');
    }

     // Evento para visualização em GRADE
    gridBtn.addEventListener('click', function() {
        vagasContainer.classList.remove('list-view');
        vagasContainer.classList.add('grid-view'); // Mantém a consistência
        gridBtn.classList.add('active');
        listBtn.classList.remove('active');
    });

    // Evento para visualização em LISTA
    listBtn.addEventListener('click', function() {
        vagasContainer.classList.remove('grid-view');
        vagasContainer.classList.add('list-view');
        listBtn.classList.add('active');
        gridBtn.classList.remove('active');
    });

    // A lógica de busca que você já tinha (verifique se o data-title foi adicionado no HTML)
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = searchInput.value.toLowerCase();
            const vagaItems = vagasContainer.getElementsByClassName('vaga-item');

            for (let i = 0; i < vagaItems.length; i++) {
                const item = vagaItems[i];
                const title = item.getAttribute('data-title');
                
                if (title && title.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            }
        });
    }

     // Inicia com a visualização em grade ativa por padrão
    activateButton(gridBtn);
});