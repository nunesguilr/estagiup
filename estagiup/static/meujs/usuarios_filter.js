document.addEventListener("DOMContentLoaded", function() {
    const cityInput = document.getElementById('cityInput');
    const groupFilter = document.getElementById('groupFilter');
    const userCards = document.querySelectorAll('.user-list-row-link'); // Seleciona o link <a>

    function filterUsers() {
        const cityTerm = cityInput.value.toLowerCase();
        const selectedGroup = groupFilter.value.toLowerCase();

        userCards.forEach(link => {
            const card = link.querySelector('.user-list-row'); // Pega o card dentro do link
            const cidade = card.getAttribute('data-cidade').toLowerCase();
            const grupo = card.getAttribute('data-grupo').toLowerCase();

            const matchesCity = cidade.includes(cityTerm);
            const matchesGroup = (selectedGroup === 'all') || (grupo === selectedGroup);

            // Mostra ou esconde o elemento <a> pai
            if (matchesCity && matchesGroup) {
                link.style.display = 'block';
            } else {
                link.style.display = 'none';
            }
        });
    }

    if (cityInput) {
        cityInput.addEventListener('input', filterUsers);
    }
    if (groupFilter) {
        groupFilter.addEventListener('change', filterUsers);
    }
});