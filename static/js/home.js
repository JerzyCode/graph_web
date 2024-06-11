
const loginButton = document.getElementById('login-button')
const signUpButton = document.getElementById('signup-button')

const loginPopupContainer = document.getElementById('popup-container-login')
const signupPopupContainer = document.getElementById('popup-container-signup')

const closeLoginPopupButton = document.getElementById('close-login-popup')
const closeSignUpPopupButton = document.getElementById('close-signup-popup')



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

function closePopups() {
  closePopupContainer(loginPopupContainer)
  closePopupContainer(signupPopupContainer)
}

function showPopupContainer(popupContainer) {
  popupContainer.style.display = 'block';
}

function closePopupContainer(popupContainer) {
  popupContainer.style.display = 'none';

}


addListeners()