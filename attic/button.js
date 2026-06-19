document.addEventListener('DOMContentLoaded', function () {
    const popupModal = document.getElementById('popupModal');
    const emojiButton = document.getElementById('emojiButton');
    const closeButton = document.querySelector('.close-button');

    emojiButton.addEventListener('click', () => {
        popupModal.style.display = 'flex';
        popupModal.setAttribute('aria-hidden', 'false');
    });

    closeButton.addEventListener('click', () => {
        popupModal.style.display = 'none';
        popupModal.setAttribute('aria-hidden', 'true');
    });

    window.addEventListener('click', (event) => {
        if (event.target === popupModal) {
            popupModal.style.display = 'none';
            popupModal.setAttribute('aria-hidden', 'true');
        }
    });

    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && popupModal.style.display === 'flex') {
            popupModal.style.display = 'none';
            popupModal.setAttribute('aria-hidden', 'true');
        }
    });
});
