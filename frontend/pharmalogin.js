document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    let isValid = true;

    // Email validation
    if (!validateEmail(email)) {
        showError('email-error', 'Please enter a valid email address.');
        isValid = false;
    } else {
        clearError('email-error');
    }

    // Password validation
    if (password.length < 6) {
        showError('password-error', 'Password must be at least 6 characters.');
        isValid = false;
    } else {
        clearError('password-error');
    }

    // If valid, navigate to the dashboard
    if (isValid) {
        window.location.href = 'pharmadash.html';
    }
});

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

function showError(id, message) {
    document.getElementById(id).innerText = message;
    document.getElementById(id).style.display = 'block';
}

function clearError(id) {
    document.getElementById(id).innerText = '';
    document.getElementById(id).style.display = 'none';
}
