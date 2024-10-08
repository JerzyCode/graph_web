const logoutButton = document.getElementById('logout-button')

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

let isShowedNotification = false

if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
        try {
            await fetch(`/logout`, {})
            showSuccessMessage('Logout')
            setTimeout(() => {
                window.location.href = './home'
            }, 1500);
        } catch (error) {
            console.error('There was a problem with logout:', error);
            showFailMessage('Error occurred login out')
            throw error;
        }
    })
}

async function changeLocation() {
    window.location.href = './home'
}

function showNotification(message, color) {
    if (isShowedNotification) {
        return
    }
    setNotificationBarVisible(message, color)
    setTimeout(() => {
        setNotificationBarInvisible()
    }, 1500);
}

function setNotificationBarVisible(message, color) {
    isShowedNotification = true
    const notificationMessage = document.getElementById('notification-message');
    notificationMessage.textContent = message;
    progress.style.backgroundColor = color
    notificationBar.style.border = '1px solid ' + color
    notificationBar.classList.add('show')
    notificationBar.style.display = 'block'
    progress.classList.add('active')
}

function setNotificationBarInvisible() {
    notificationBar.classList.remove('show');
    progress.classList.remove('active')
    isShowedNotification = false
}

export function showSuccessMessage(message) {
    showNotification(message, '#4cda15')
}

export function showFailMessage(message) {
    showNotification(message, '#ff0000')
}
