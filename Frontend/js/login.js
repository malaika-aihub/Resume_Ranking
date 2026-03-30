const loginForm = document.getElementById("loginForm");
const loginStatus = document.getElementById("loginStatus");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    loginStatus.textContent = "Logging in...";

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("token", data.token);
            loginStatus.textContent = "Login successful ✅";

            setTimeout(() => {
                window.location.href = "index.html";
            }, 1000);

        } else {
            loginStatus.textContent = data.detail || "Login failed ❌";
        }

    } catch (error) {
        console.error(error);
        loginStatus.textContent = "Server error ❌";
    }
});