document.addEventListener("DOMContentLoaded", function() {
    // Switch between login and signup forms
    document.getElementById('show-signup').addEventListener('click', function() {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('signup-form').style.display = 'block';

        // Modify the label text and remove hyperlink
        const signupLabel = document.getElementById('signup-label');
        signupLabel.textContent = "Please complete the following below";
        signupLabel.style.cursor = "default"; // Remove pointer cursor
    });

    document.getElementById('show-login').addEventListener('click', function() {
        document.getElementById('signup-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';

        // Restore the original text for the sign-up link
        const signupLabel = document.getElementById('signup-label');
        signupLabel.innerHTML = `Don't have an account? <a href="#" id="show-signup">Create One</a>`;
        attachSignupEvent(); // Reattach event listener since we modified the innerHTML
    });

    function attachSignupEvent() {
        document.getElementById('show-signup').addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('signup-form').style.display = 'block';

            // Modify label text and remove hyperlink
            const signupLabel = document.getElementById('signup-label');
            signupLabel.textContent = "Please complete the following below";
            signupLabel.style.cursor = "default";
        });
    }

    attachSignupEvent(); // Call the function initially to attach event listener

    // Form validation on signup
    document.getElementById('signup-form-action').addEventListener('submit', function(e) {
        e.preventDefault();

        const username = document.getElementById('signup-username').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const dob = document.getElementById('signup-dob').value;

        // Email Validation (basic check)
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!email.match(emailPattern)) {
            alert("Please enter a valid email.");
            return;
        }

        // Password Strength Check (at least 6 characters, one uppercase, one number, one lowercase)
        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
        if (!password.match(passwordPattern)) {
            alert("Password must be at least 6 characters long, include an uppercase letter, a lowercase letter, and a number.");
            return;
        }

        // Check if password and confirm password match
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        // If all validation passes, submit the form
        alert('Account created successfully!');
    });
});
