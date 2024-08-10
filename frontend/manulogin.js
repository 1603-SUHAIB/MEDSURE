document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    let isValid = true;

    // Validate Email
    const email = document.getElementById('email').value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === '') {
        showError('email-error', 'Email is required');
        isValid = false;
    } else if (!emailPattern.test(email)) {
        showError('email-error', 'Please enter a valid email');
        isValid = false;
    } else {
        clearError('email-error');
    }

    // Validate Password
    const password = document.getElementById('password').value.trim();
    if (password === '') {
        showError('password-error', 'Password is required');
        isValid = false;
    } else if (password.length < 6) {
        showError('password-error', 'Password must be at least 6 characters long');
        isValid = false;
    } else {
        clearError('password-error');
    }

    // If form is valid, navigate to the dashboard page
    if (isValid) {
        window.location.href = 'manudash.html';
    }
});

// Function to show error message
function showError(id, message) {
    const element = document.getElementById(id);
    element.textContent = message;
    element.style.display = 'block';
}

// Function to clear error message
function clearError(id) {
    const element = document.getElementById(id);
    element.textContent = '';
    element.style.display = 'none';
}
