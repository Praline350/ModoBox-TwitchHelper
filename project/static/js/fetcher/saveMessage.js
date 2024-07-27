async function saveMessage(csrfToken, author, message){
    console.log(author)
    console.log(message)
    try {
        let response = await fetch('/api/chat/messages/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Important pour inclure les cookies dans la requête
            body: JSON.stringify({
                username: author,
                message: message
            })
            
        });
        console.log(message)

        if (!response.ok) {
            throw new Error(`Erreur HTTP! statut: ${response.status}`);
        }

        let data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur lors de la requête POST:', error);
        return null;
    }
}

export { saveMessage }