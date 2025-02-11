document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Script loaded");

    // 🔹 Handle Login Form Submission
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            console.log("🔹 Login form submitted");

            const username = document.getElementById("login-username").value;
            const password = document.getElementById("login-password").value;

            console.log("🔹 Sending login request...", { username, password });

            try {
                const response = await fetch("http://127.0.0.1:5001/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();
                console.log("✅ Login response:", result);

                if (response.ok) {
                    sessionStorage.setItem("user_id", result.user_id);
                    sessionStorage.setItem("username", username);
                    console.log("✅ Stored user:", { user_id: result.user_id, username });

                    window.location.href = "/dashboard";
                } else {
                    console.error("❌ Login failed:", result.error);
                    document.getElementById("login-status").innerText = result.error || "Login failed!";
                }
            } catch (error) {
                console.error("❌ Error connecting to the server:", error);
                document.getElementById("login-status").innerText = "Error connecting to the server.";
            }
        });
    }

    // 🔹 Show Signup Form When Clicking "Create One"
    const showSignupLink = document.getElementById("show-signup");
    const signupForm = document.getElementById("signup-form");
    if (showSignupLink && signupForm && loginForm) {
        showSignupLink.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("🔹 'Create One' clicked");
            loginForm.parentElement.style.display = "none"; 
            signupForm.style.display = "block";
            document.getElementById("signup-label").innerText = "Please complete the form below";
        });
    }

    // 🔹 Handle Signup Form Submission
    const signupFormAction = document.getElementById("signup-form-action");
    if (signupFormAction) {
        signupFormAction.addEventListener("submit", async function (event) {
            event.preventDefault();
            console.log("🔹 Signup form submitted");

            const firstName = document.getElementById("signup-firstname").value;
            const lastName = document.getElementById("signup-lastname").value;
            const username = document.getElementById("signup-username").value;
            const email = document.getElementById("signup-email").value;
            const password = document.getElementById("signup-password").value;
            const confirmPassword = document.getElementById("confirm-password").value;
            const dob = document.getElementById("signup-dob").value;

            if (password !== confirmPassword) {
                console.error("❌ Passwords do not match!");
                document.getElementById("signup-status").innerText = "Passwords do not match!";
                return;
            }

            const userData = { first_name: firstName, last_name: lastName, username, email, password, dob };
            console.log("🔹 Sending signup request...", userData);

            try {
                const response = await fetch("http://127.0.0.1:5001/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData)
                });

                const result = await response.json();
                console.log("✅ Signup response:", result);

                if (response.ok) {
                    document.getElementById("signup-status").innerText = "Account created successfully!";
                    signupFormAction.reset();
                } else {
                    document.getElementById("signup-status").innerText = result.error || "Signup failed!";
                }
            } catch (error) {
                console.error("❌ Error connecting to the server:", error);
                document.getElementById("signup-status").innerText = "Error connecting to the server.";
            }
        });
    }

    // 🔹 Fetch and Display Goals on Dashboard
    const dashboardGoalsContainer = document.getElementById("dashboard-goals");
    const userId = sessionStorage.getItem("user_id");
    
    if (dashboardGoalsContainer && userId) {
        console.log("🔹 Fetching goals for user:", userId);
        
        fetch(`http://127.0.0.1:5002/goals?user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                console.log("✅ Goals response:", data);

                if (!data.goals || data.goals.length === 0) {
                    dashboardGoalsContainer.innerHTML = "<p>No goals found.</p>";
                    return;
                }

                let goalListHTML = "<ul>";
                data.goals.forEach(goal => {
                    goalListHTML += `<li>${goal.name} - Progress: ${goal.progress}%</li>`;
                });
                goalListHTML += "</ul>";
                
                dashboardGoalsContainer.innerHTML = goalListHTML;
            })
            .catch(error => console.error("❌ Error fetching goals:", error));
    }
});
