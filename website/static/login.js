const wrapper = document.querySelector('.wrapper')
const signUpLink = document.querySelector('.signUp-link')
const signInLink = document.querySelector('.signIn-link')

signUpLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signIn');
    wrapper.classList.remove('animate-signUp');  
});

signInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signUp');
    wrapper.classList.remove('animate-signIn');  
});

function showFlashMessage(message, category) {
    const flashMessagesDiv = document.getElementById('flash-messages');

    // Create the flash message div
    const flashMessage = document.createElement('div');
    flashMessage.className = `alert alert-${category} alert-dismissable fade show`;
    flashMessage.setAttribute('role', 'alert');
    flashMessage.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;

    // Append the flash message to the container
    flashMessagesDiv.appendChild(flashMessage);

    // Automatically remove the flash message after 5 seconds
    setTimeout(() => {
        flashMessage.remove();
    }, 5000);
}

document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    const firstName = document.getElementById('Firstname').value;
    const lastName = document.getElementById('Lastname').value;
    const email = document.getElementById('email').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    if (firstName.length < 2) {
        showFlashMessage('Firstname must be greater than 2 characters.', 'danger');
    } else if (lastName.length < 2) {
        showFlashMessage('Lastname must be greater than 2 characters.', 'danger');
    } else if (email.length < 4) {
        showFlashMessage('Email must be greater than 4 characters.', 'danger');
    } else if (password1 !== password2) {
        showFlashMessage("Hey your passwords don't match.", 'danger');
    } else if (password1.length < 7) {
        showFlashMessage('Password must be at least 7 characters.', 'danger');
    } else {
        showFlashMessage('Account created!', 'success');

        // Optionally, submit the form after successful validation
        // this.submit();
    }
});