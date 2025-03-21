// static/js/navbar.js

document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname; // Obtém o caminho atual
    const links = document.querySelectorAll('.nav-link'); // Seleciona todos os links

    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active'); // Adiciona a classe 'active' ao link correspondente
        }
    });
});