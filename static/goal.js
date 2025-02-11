document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Goal script loaded");

    const userId = sessionStorage.getItem("user_id");
    if (!userId) {
        console.warn("❌ No user found! Redirecting to login...");
        window.location.href = "/";
        return;
    }

    const goalForm = document.getElementById("create-goal-form");

    // 🔹 Handle Goal Form Submission
    goalForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        console.log("🔹 Goal form submitted");

        const goalName = document.getElementById("goal-name").value;
        const description = document.getElementById("goal-description").value;
        const targetAmount = document.getElementById("goal-target").value || null; // Optional

        console.log("🔹 Sending goal request...", { userId, goalName, description, targetAmount });

        try {
            const response = await fetch("http://127.0.0.1:5002/create-goal", {  // ✅ Uses updated route
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: userId,
                    name: goalName,
                    description: description,
                    target_amount: targetAmount
                })
            });

            const result = await response.json();
            console.log("✅ Goal response:", result);

            if (response.ok) {
                console.log("✅ Goal added successfully! Redirecting to dashboard...");
                window.location.href = "/dashboard";
            } else {
                document.getElementById("status-message").innerText = result.error || "Failed to add goal.";
            }
        } catch (error) {
            console.error("❌ Error connecting to the server:", error);
            document.getElementById("status-message").innerText = "Error connecting to the server.";
        }
    });
});
