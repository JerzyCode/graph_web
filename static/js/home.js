const loginButton = document.getElementById('login-button')
const signUpButton = document.getElementById('signup-button')

const loginPopupContainer = document.getElementById('popup-container-login')
const signupPopupContainer = document.getElementById('popup-container-signup')

const closeLoginPopupButton = document.getElementById('close-login-popup')
const closeSignUpPopupButton = document.getElementById('close-signup-popup')

const failMessageCompLogin = document.getElementById('fail-message-comp-login')
const failMessageCompSignUp = document.getElementById('fail-message-comp-signup')


document.addEventListener('DOMContentLoaded', (event) => {
    const flashMessage = failMessageCompLogin.getAttribute('data-flash-message')

    if (flashMessage && flashMessage.length > 2) {
        handleFlashMessage(flashMessage)
        //
    }
    addListeners()
})

function addListeners() {
    if (loginButton) {
        loginButton.addEventListener('click', () => showPopupContainer(loginPopupContainer))
    }

    if (signUpButton) {
        signUpButton.addEventListener('click', () => showPopupContainer(signupPopupContainer))
    }

    if (closeLoginPopupButton) {
        closeLoginPopupButton.addEventListener('click', () => closePopupContainer(loginPopupContainer))
    }

    if (closeSignUpPopupButton) {
        closeSignUpPopupButton.addEventListener('click', () => closePopupContainer(signupPopupContainer))
    }

    window.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closePopups()
        }
    })
    window.onclick = function (event) {
        if (event.target === loginPopupContainer
            || event.target === signupPopupContainer) {
            closePopups()
        }
    }
}

function handleFlashMessage(flashMessage) {
    console.log(flashMessage)
    if (flashMessage.includes('signup')) {
        if (flashMessage.includes('email')) {
            failMessageCompSignUp.textContent = 'Email is already taken.'
        } else {
            failMessageCompSignUp.textContent = 'Passwords do not match.'
        }
        showPopupContainer(signupPopupContainer)
        showFailMessageComp(failMessageCompSignUp)
    } else if (flashMessage.includes('login')) {
        showPopupContainer(loginPopupContainer)
        showFailMessageComp(failMessageCompLogin)
    }

}

function showFailMessageComp(failMessageComp) {
    failMessageComp.style.display = 'block'
}

function hideFailMessageComp(failMessageComp) {
    failMessageComp.style.display = 'none'
}


function closePopups() {
    closePopupContainer(loginPopupContainer)
    closePopupContainer(signupPopupContainer)
    hideFailMessageComp(failMessageCompLogin)
    hideFailMessageComp(failMessageCompSignUp)
}

export function showPopupContainer(popupContainer) {
    popupContainer.style.display = 'block';
}

function closePopupContainer(popupContainer) {
    hideFailMessageComp(failMessageCompLogin)
    hideFailMessageComp(failMessageCompSignUp)
    popupContainer.style.display = 'none';
}
