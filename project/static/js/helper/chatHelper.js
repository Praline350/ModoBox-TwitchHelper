import { getCsrfToken } from './getCsrfToken.js';

// Fonction pour charger les paramètres de chat
async function loadChatSettings() {
    const csrfToken = getCsrfToken();
    const response = await fetch('/api/chat/settings/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error('Failed to load chat settings');
    }
    return await response.json();
}

async function saveChatSettings(settings) {
    const csrfToken = getCsrfToken();
    const response = await fetch('/api/chat/settings/', {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(settings)
    });
    console.log(JSON.stringify(settings))

    if (!response.ok) {
        throw new Error('Failed to save chat settings');
    }

    return await response.json();
}

function applyChatSettings(settings) {
    const chatBox = document.getElementById('chat-box');
    const fontColorPicker = document.getElementById('chat-font-color-picker');
    const backgroundColorPicker = document.getElementById('chat-background-color-picker');
    console.log("Applying settings:", settings);

    if (settings.background_color) {
        chatBox.style.backgroundColor = settings.background_color;
        backgroundColorPicker.value = settings.background_color;
        console.log('Applied background color:', chatBox.style.backgroundColor);
    } else {
        console.log('No background color setting found');
    }

    if (settings.font_color) {
        fontColorPicker.value = settings.font_color;
        document.querySelectorAll('.chat-message-content').forEach((element) => {
            element.style.color = settings.font_color;
            console.log('Applied font color to element:', element.style.color);
        });
    } else {
        console.log('No font color setting found');
    }
}

function scrollToBottom() {
    var chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

export { loadChatSettings, saveChatSettings, applyChatSettings, scrollToBottom };