document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Session script loaded");

    // Retrieve user ID & username
    const userId = sessionStorage.getItem("user_id");
    const username = sessionStorage.getItem("username");

    console.log("🔹 Retrieved session:", { userId, username });

    if (!userId || !username) {
        console.warn("❌ No user found! Redirecting to login...");
        window.location.href = "/";
        return;
    }
});
