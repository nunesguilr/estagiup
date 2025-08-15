document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput');
    const vagasContainer = document.getElementById('vagas-list');
    const vagaCards = vagasContainer.getElementsByClassName('vaga-card');
    const btnListView = document.getElementById('btn-list-view');
    const btnGridView = document.getElementById('btn-grid-view');

    // Função para alternar entre visualização de lista e grade
    if (btnListView && btnGridView && vagasContainer) {
        btnListView.addEventListener('click', function() {
            vagasContainer.classList.remove('grid-view');
            vagasContainer.classList.add('list-view');
            btnGridView.classList.remove('active');
            btnListView.classList.add('active');
        });

        btnGridView.addEventListener('click', function() {
            vagasContainer.classList.remove('list-view');
            vagasContainer.classList.add('grid-view');
            btnListView.classList.remove('active');
            btnGridView.classList.add('active');
        });
    }

    // Filtro de pesquisa
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = searchInput.value.toLowerCase();

            for (let i = 0; i < vagaCards.length; i++) {
                const card = vagaCards[i];
                const title = card.getAttribute('data-title');

                if (title.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    }
});