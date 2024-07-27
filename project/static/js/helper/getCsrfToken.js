// Fonction helper pour obtenir le token CSRF à partir des balises meta
function getCsrfToken() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return csrfToken;
}

// Exporter la fonction pour qu'elle puisse être utilisée dans d'autres scripts
export { getCsrfToken };
