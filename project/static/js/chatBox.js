// static/js/chatBox.js

document.addEventListener('DOMContentLoaded', (event) => {
    var chatBox = document.getElementById('chat-box');

    fetch('/api/get-token/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }

        var accessToken = data.access_token;
        var username = data.username;

        if (accessToken && username) {
            console.log("Username:", username);
            

            var ws = new WebSocket("wss://irc-ws.chat.twitch.tv:443");

            ws.onopen = function(event) {
                console.log("WebSocket ouvert, envoi des commandes IRC...");
                ws.send(`PASS oauth:${accessToken}`);
                ws.send(`NICK ${username}`);
                console.log(`NICK ${username}`);
                ws.send(`JOIN #${username}`);
                console.log(`JOIN #${username}`);
            };

            ws.onmessage = function(event) {
                console.log("Message reçu :", event.data);
                var messageData = event.data;
                if (messageData.includes('PRIVMSG')) {
                    var username = messageData.split('!')[0].substring(1);
                    var message = messageData.split('PRIVMSG')[1].split(':')[1];
                    var messageDiv = document.createElement('div');
                    messageDiv.innerHTML = `<strong>${username}:</strong> ${message}`;
                    chatBox.appendChild(messageDiv);
                }
            };

            ws.onerror = function(event) {
                console.error("Erreur WebSocket observée:", event);
            };

            ws.onclose = function(event) {
                console.log("WebSocket est maintenant fermé.");
            };
        } else {
            console.error("Informations utilisateur manquantes");
        }
    })
    .catch(error => console.error('Erreur:', error));
});
