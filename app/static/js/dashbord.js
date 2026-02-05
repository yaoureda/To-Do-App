
function getToday() {
    return new Date().toISOString().split("T")[0];
}

async function getStats() {
    const res = await fetch("/api/session");
    return await res.json();
}

async function logSession(minutesWorked) {
    const today = getToday();

    try {
        const res = await fetch("/api/session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                minutes: minutesWorked,
                date: today
            })
        });

        const data = await res.json();
        if (data.success) {
            updateDashboard(); // you may want to fetch stats from the backend
        } else {
            alert("Error logging session: " + (data.error || ""));
        }
    } catch (err) {
        console.error(err);
        alert("Failed to log session.");
    }
}


let workChart = null;

async function updateDashboard() {
    const stats = await getStats();

    const last7Days = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        last7Days.push(d.toISOString().split("T")[0]);
    }

    const minutes = last7Days.map(d => stats[d] || 0);

    const canvas = document.getElementById("workChart");
    if (!canvas) return;

    if (!workChart) {
        workChart = new Chart(canvas.getContext("2d"), {
            type: "bar",
            data: {
                labels: last7Days,
                datasets: [{
                    label: "Minutes worked",
                    data: minutes,
                    backgroundColor: "#4CAF50"
                }]
            },
            options: { responsive: true }
        });
    } else {
        workChart.data.labels = last7Days;
        workChart.data.datasets[0].data = minutes;
        workChart.update();
    }
}

async function clearAllStats() {
    if (!confirm("Are you sure? This will delete all your work history.")) return;

    try {
        const res = await fetch("/api/session", {
            method: "DELETE"
        });

        const data = await res.json();
        if (data.success) {
            updateDashboard();
        }
    } catch (err) {
        console.error(err);
        alert("Failed to clear stats.");
    }
}

document.addEventListener("DOMContentLoaded", updateDashboard);