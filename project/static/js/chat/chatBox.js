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
})


const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const container = document.getElementById('messages-container');
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    container.appendChild(messageElement);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // Appuyer sur Entrée pour envoyer le message
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};


//     var csrfToken = getCsrfToken();
//     console.log("CSRF Token:", csrfToken); // Vérifier le token CSRF

//     fetch('/api/get-token/', {
//         method: 'GET',
//         headers: {
//             'X-CSRFToken': csrfToken,
//             'Content-Type': 'application/json'
//         },
//         credentials: 'include' // Important pour inclure les cookies dans la requête
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             console.error(data.error);
//             return;
//         }

//         var accessToken = data.access_token;
//         var username = data.username;
//         var display_name = data.display_name;

//         if (accessToken && username) {
//             console.log("Username:", username);
            
//             var ws = new WebSocket("wss://irc-ws.chat.twitch.tv:443");

//             ws.onopen = function(event) {
//                 console.log("WebSocket ouvert, envoi des commandes IRC...");
//                 ws.send(`PASS oauth:${accessToken}`);
//                 ws.send(`NICK ${display_name}`);
//                 console.log(`NICK ${display_name}`);
//                 ws.send(`JOIN #${username}`);
//                 console.log(`JOIN #${username}`);
//             };

//             ws.onmessage = function(event) {
//                 console.log("Message reçu :", event.data);
//                 var messageData = event.data;
//                 if (messageData.includes('PRIVMSG')) {
//                     var username = messageData.split('!')[0].substring(1);
//                     var message = messageData.split('PRIVMSG')[1].split(':')[1];
//                     var messageDiv = document.createElement('div');
//                     var messageContent = document.createElement('p');
//                     var messageAuthor = document.createElement('strong');
//                     messageContent.classList.add('chat-message-content')
//                     messageDiv.classList.add('chat-message-container')
//                     messageAuthor.classList.add('chat-message-author')
//                     messageContent.innerHTML = `${message}`
//                     messageAuthor.innerHTML = `${display_name}: `;
//                     chatBox.appendChild(messageDiv);
//                     messageDiv.appendChild(messageAuthor);
//                     messageDiv.appendChild(messageContent);
                    
//                     scrollToBottom();
//                 }
//             };

//             ws.onerror = function(event) {
//                 console.error("Erreur WebSocket observée:", event);
//             };

//             ws.onclose = function(event) {
//                 console.log("WebSocket est maintenant fermé.");
//             };
//         } else {
//             console.error("Informations utilisateur manquantes");
//         }
//     })
//     .catch(error => console.error('Erreur:', error));
// });
