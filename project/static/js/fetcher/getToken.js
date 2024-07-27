async function getToken(csrfToken) {
    try {
        let response = await fetch('/api/get-token/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Important pour inclure les cookies dans la requête
        });
        let data = await response.json();
        if (data.error) {
            console.error(data.error);
            return null;
        }
        return {
            accessToken: data.access_token,
            username: data.username,
            displayName: data.display_name
        };
    } catch (error) {
        console.error('Erreur:', error);
        return null;
    }
}

export { getToken };