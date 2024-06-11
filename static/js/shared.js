const logoutButton = document.getElementById('logout-button')

if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
        try {
            await fetch(`/logout`, {})
            console.log('test123')
            window.location.href = './home'

        } catch (error) {
            console.error('There was a problem with logout:', error);
            throw error;
        }
    })
}