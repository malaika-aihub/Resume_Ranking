const signupForm = document.getElementById('signupForm');
const signupStatus = document.getElementById('signupStatus');

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        signupStatus.style.color = "#FF6B6B"; // red
        signupStatus.textContent = "Please enter username and password ❌";
        return;
    }

    signupStatus.style.color = "#333";
    signupStatus.textContent = "Signing up... ⏳";

    try {
        const response = await fetch('http://127.0.0.1:8000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            signupStatus.style.color = "#4BB543"; // green
            signupStatus.textContent = data.message || "Signup successful ✅";

            // ⏳ Show message for 10 seconds, then redirect to index.html
            setTimeout(() => {
                signupStatus.textContent = "";
                window.location.href = "index.html"; // ensure path correct
            }, 10000); // 10000 ms = 10 seconds
        } else {
            signupStatus.style.color = "#FF6B6B"; // red
            signupStatus.textContent = data.detail || "Signup failed ❌";
        }

    } catch (err) {
        console.error(err);
        signupStatus.style.color = "#FF6B6B"; // red
        signupStatus.textContent = "Server error. Try again! ❌";
    }
});