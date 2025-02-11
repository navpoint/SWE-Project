document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Plan script loaded");

    const planForm = document.getElementById("plan-form");

    if (!planForm) {
        console.error("❌ Plan form not found!");
        return;
    }

    planForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        console.log("🔹 Plan form submitted");

        // Get user ID from sessionStorage
        const userId = sessionStorage.getItem("user_id");
        if (!userId) {
            console.warn("❌ No user found! Redirecting to login...");
            window.location.href = "/";
            return;
        }

        // Get input values
        const planName = document.getElementById("plan-name").value;
        const description = document.getElementById("plan-description").value;

        console.log("🔹 Sending plan request...", { userId, planName, description });

        try {
            const response = await fetch("http://127.0.0.1:5002/add-plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, name: planName, description })
            });

            const result = await response.json();
            console.log("✅ Plan response:", result);

            if (response.ok) {
                console.log("✅ Plan added successfully! Redirecting to dashboard...");
                window.location.href = "/dashboard";  // ✅ Redirect back to dashboard
            } else {
                document.getElementById("plan-status").innerText = result.error || "Failed to add plan.";
            }
        } catch (error) {
            console.error("❌ Error connecting to the server:", error);
            document.getElementById("plan-status").innerText = "Error connecting to the server.";
        }
    });
});
