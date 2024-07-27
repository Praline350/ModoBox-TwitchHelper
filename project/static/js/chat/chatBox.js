import { getCsrfToken } from '../helper/getCsrfToken.js';
import { loadChatSettings, saveChatSettings, applyChatSettings } from '../helper/chatHelper.js';

document.addEventListener('DOMContentLoaded', async (event) => {
    var chatBox = document.getElementById('chat-box');

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    try {
        const settings = await loadChatSettings();
        console.log('Loaded settings:', settings);
        setTimeout(() => {
            applyChatSettings(settings);
            console.log('Applied settings successfully');
        }, 0); // Délai de 0 millisecondes pour garantir que le DOM est prêt
    } catch (error) {
        console.error('Erreur de chargement des paramètres de chat:', error);
    }


    var csrfToken = getCsrfToken(); 

    fetch('/api/get-token/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'include' // Important pour inclure les cookies dans la requête
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }

        var accessToken = data.access_token;
        var username = data.username;
        var display_name = data.display_name;

        if (accessToken && username) {
            
            var ws = new WebSocket("wss://irc-ws.chat.twitch.tv:443");

            ws.onopen = function(event) {
                ws.send(`PASS oauth:${accessToken}`);
                ws.send(`NICK ${display_name}`);
                ws.send(`JOIN #${username}`);
            };

            ws.onmessage = function(event) {
                var messageData = event.data;
                if (messageData.includes('PRIVMSG')) {
                    var username = messageData.split('!')[0].substring(1);
                    var message = messageData.split('PRIVMSG')[1].split(':')[1];
                    var messageDiv = document.createElement('div');
                    var messageContent = document.createElement('p');
                    var messageAuthor = document.createElement('strong');
                    messageContent.classList.add('chat-message-content')
                    messageDiv.classList.add('chat-message-container')
                    messageAuthor.classList.add('chat-message-author')
                    messageContent.innerHTML = `${message}`
                    messageAuthor.innerHTML = `${display_name}: `;
                    chatBox.appendChild(messageDiv);
                    messageDiv.appendChild(messageAuthor);
                    messageDiv.appendChild(messageContent);
                    
                    scrollToBottom();
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
