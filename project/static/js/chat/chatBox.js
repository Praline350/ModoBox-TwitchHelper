import { getCsrfToken } from '../helper/getCsrfToken.js';
import { loadChatSettings, saveChatSettings, applyChatSettings, scrollToBottom } from '../helper/chatHelper.js';
import { getToken } from '../fetcher/getToken.js';
import { setupWebSocket } from './websocket.js';

document.addEventListener('DOMContentLoaded', async (event) => {
    

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
    var tokenData = await getToken(csrfToken)

    if (tokenData) {
        setupWebSocket(tokenData.accessToken, tokenData.username, tokenData.displayName);
    } else {
        console.error("Informations utilisateur manquantes ou échec de la récupération du token");
    }
})
