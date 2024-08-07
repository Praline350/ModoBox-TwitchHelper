import  { scrollToBottom } from '../helper/chatHelper.js'
// import { saveMessage } from '../fetcher/saveMessage.js'
import { getCsrfToken } from '../helper/getCsrfToken.js';

function setupWebSocket(accessToken, username, display_name) {
    var ws = new WebSocket("wss://irc-ws.chat.twitch.tv:443");
    var chatBox = document.getElementById('chat-box');
    var csrfToken = getCsrfToken();

    ws.onopen = function(event) {
        ws.send(`PASS oauth:${accessToken}`);
        ws.send(`NICK ${display_name}`);
        ws.send(`JOIN #${username}`);
    };

    ws.onmessage = function(event) {
        var messageData = event.data;
        if (messageData.includes('PRIVMSG')) {
            var username = messageData.split('!')[0].substring(1);
            var message = messageData.split('PRIVMSG')[1].split(':').slice(1).join(':').trim();
            var messageDiv = document.createElement('div');
            var messageContent = document.createElement('p');
            var messageAuthor = document.createElement('strong');
            messageContent.classList.add('chat-message-content');
            messageDiv.classList.add('chat-message-container');
            messageAuthor.classList.add('chat-message-author');
            messageContent.innerHTML = `${message}`;
            messageAuthor.innerHTML = `${display_name}: `;
            chatBox.appendChild(messageDiv);
            messageDiv.appendChild(messageAuthor);
            messageDiv.appendChild(messageContent);
            // saveMessage(csrfToken, username, message)
            //     .then(postResponse => {
            //         if (postResponse) {
            //             console.log('Message posté avec succès:', postResponse);
            //         } else {
            //             console.error('Échec de la publication du message');
            //         }
            //     })
            //     .catch(error => {
            //         console.error('Erreur lors de la publication du message:', error);
            //     });
            scrollToBottom();
        }
    };

    ws.onerror = function(event) {
        console.error("Erreur WebSocket observée:", event);
    };

    ws.onclose = function(event) {
        console.log("WebSocket est maintenant fermé.");
    };

    return ws;
}

export { setupWebSocket } ;