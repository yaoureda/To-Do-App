
document.getElementById("signup-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("floatingInput").value;
    const password = document.getElementById("floatingPassword").value;

    const response = await fetch("/api/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    if (response.status === 201) {
        window.location.href = "/login";
    } else if (response.status === 409) {
        alert("Username already exists");
    } else {
        alert("Signup failed");
    }
});