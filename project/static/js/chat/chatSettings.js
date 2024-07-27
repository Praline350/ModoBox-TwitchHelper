import { saveChatSettings } from '../helper/chatHelper.js';

document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const backgroundColorPicker = document.getElementById('chat-background-color-picker');
    const fontColorPicker = document.getElementById('chat-font-color-picker');
    const saveCustomizationBtn = document.getElementById('save-customization-btn');

    // Fonction pour appliquer la couleur de la police
    function applyFontColor(color) {
        const messageContents = document.querySelectorAll('.chat-message-content');
        messageContents.forEach(function(messageContent) {
            messageContent.style.color = color;
        });
    }

    // Fonction pour sauvegarder les préférences sélectionnées
    async function savePreferences() {
        const selectedBackgroundColor = backgroundColorPicker.value;
        const selectedFontColor = fontColorPicker.value;

        const newSettings = {
            background_color: selectedBackgroundColor,
            font_color: selectedFontColor
        };

        chatBox.style.backgroundColor = selectedBackgroundColor;
        applyFontColor(selectedFontColor);

        try {
            await saveChatSettings(newSettings);
            console.log('Preferences saved successfully');
        } catch (error) {
            console.error('Error saving preferences:', error);
        }
    }

    // Attacher l'événement de sauvegarde au bouton de personnalisation
    saveCustomizationBtn.addEventListener('click', savePreferences);
});