document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Session script loaded");

    // Retrieve user ID & username
    const userId = sessionStorage.getItem("user_id");
    const username = sessionStorage.getItem("username");

    console.log("🔹 Retrieved session:", { userId, username });

    // Get the current page URL
    const currentPath = window.location.pathname;

    // If no session is found and the user is trying to access a restricted page, redirect
    if (!userId || !username) {
        if (currentPath !== "/") {  // Allow the index page to load
            console.warn("❌ No user found! Redirecting to login...");
            window.location.href = "/";
        } else {
            console.warn("⚠️ No user session, but staying on the index page.");
        }
        return;
    }

    console.log("🔹 User session active:", { userId, username });
});
