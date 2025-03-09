document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Dashboard script loaded");

    // ✅ Extract user info from URL parameters
    const params = new URLSearchParams(window.location.search);
    let userId = params.get("user_id");
    let username = params.get("username");
    let firstName = params.get("first_name");

    // ✅ If missing from URL, try getting from sessionStorage
    if (!userId) {
        userId = sessionStorage.getItem("user_id");
        username = sessionStorage.getItem("username");
        firstName = sessionStorage.getItem("first_name");
    }

    // ✅ If still missing, redirect to login
    if (!userId) {
        console.warn("❌ No user found! Redirecting to login...");
        window.location.href = "/";
        return;
    }

    // ✅ Save user info in sessionStorage for navigation persistence
    sessionStorage.setItem("user_id", userId);
    sessionStorage.setItem("username", username);
    sessionStorage.setItem("first_name", firstName);

    document.getElementById("userIdLabel").textContent = userId;

    // ✅ Fetch Plans & Populate Plans Table
    fetch(`http://127.0.0.1:5002/plans?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            console.log("✅ Plans response:", data);

            const plansTableBody = document.querySelector("#plans-table tbody");
            if (!plansTableBody) {
                console.error("❌ Plans table not found in the HTML.");
                return;
            }

            if (data.plans.length === 0) {
                plansTableBody.innerHTML = "<tr><td colspan='2'>No Plans Created</td></tr>";
                return;
            }

            plansTableBody.innerHTML = ""; // Clear existing rows
            data.plans.forEach(plan => {
                console.log("🔹 Adding Plan:", plan);

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>
                        <a href="/plan/${plan.plan_id}?user_id=${userId}&username=${encodeURIComponent(username)}&first_name=${encodeURIComponent(firstName)}">
                            ${plan.name}
                        </a>
                    </td>
                    <td>${plan.description || "No description provided"}</td>
                `;
                plansTableBody.appendChild(row);
            });
        })
        .catch(error => console.error("❌ Error fetching plans:", error));

    // ✅ Fetch Goals & Populate Goals Table
// ✅ Fetch Goals & Populate Goals Table
fetch(`http://127.0.0.1:5002/goals?user_id=${userId}`)
.then(response => response.json())
.then(data => {
    console.log("✅ Goals response:", data);

    const goalsTableBody = document.querySelector("#goals-table tbody");
    if (!goalsTableBody) {
        console.error("❌ Goals table not found in the HTML.");
        return;
    }

    if (data.goals.length === 0) {
        goalsTableBody.innerHTML = "<tr><td colspan='3'>No Goals Created</td></tr>";
        return;
    }

    goalsTableBody.innerHTML = ""; // Clear existing rows
    data.goals.forEach(goal => {
        console.log("🔹 Adding Goal:", goal);

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>
                <a href="/goal/${goal.goal_id}?user_id=${userId}&username=${encodeURIComponent(username)}&first_name=${encodeURIComponent(firstName)}">
                    ${goal.name}
                </a>
            </td>
            <td>${goal.progress}%</td>
            <td>${goal.target_amount || "N/A"}</td>
        `;
        goalsTableBody.appendChild(row);
    });
})
.catch(error => console.error("❌ Error fetching goals:", error));

    // ✅ Update "Create New" links dynamically
    document.getElementById("createPlanLink").href = `/create-plan?user_id=${userId}&username=${encodeURIComponent(username)}&first_name=${encodeURIComponent(firstName)}`;
    document.getElementById("createGoalLink").href = `/create-goal?user_id=${userId}&username=${encodeURIComponent(username)}&first_name=${encodeURIComponent(firstName)}`;
});
