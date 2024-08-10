document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    let isValid = true;

    // Validate Name
    const name = document.getElementById('name').value.trim();
    if (name === '') {
        showError('name-error', 'Name is required');
        isValid = false;
    } else {
        clearError('name-error');
    }

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

    // Validate Confirm Password
    const confirmPassword = document.getElementById('confirm-password').value.trim();
    if (confirmPassword === '') {
        showError('confirm-password-error', 'Please confirm your password');
        isValid = false;
    } else if (confirmPassword !== password) {
        showError('confirm-password-error', 'Passwords do not match');
        isValid = false;
    } else {
        clearError('confirm-password-error');
    }

    // Validate Role
    const role = document.querySelector('input[name="role"]:checked');
    if (!role) {
        showError('role-error', 'Please select a role');
        isValid = false;
    } else {
        clearError('role-error');
    }

    // Validate File Upload
    const proof = document.getElementById('proof').value;
    if (proof === '') {
        showError('proof-error', 'Please upload a proof');
        isValid = false;
    } else {
        clearError('proof-error');
    }

    // Validate Terms & Conditions
    const terms = document.getElementById('terms').checked;
    if (!terms) {
        showError('terms-error', 'You must agree to the Terms & Conditions');
        isValid = false;
    } else {
        clearError('terms-error');
    }

    // If form is valid, submit the form or perform further actions
    if (isValid) {
        alert('Form submitted successfully!');
        // You can submit the form data via AJAX or similar method here
        // e.g., form.submit();
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
