
///// TASKS SCRIPT

function loadTasks() {
  fetch('/api/tasks')
    .then(res => res.json())
    .then(tasks => {
      const tasksDiv = document.querySelector('.big-div');
      tasksDiv.innerHTML = '';

      tasks.forEach(task => {
        const div = document.createElement('div');
        div.className = "small-div d-grid gap-2 col-6 mx-auto"
        const date = new Date(task.created_at).toLocaleString('fr-FR');

        div.innerHTML = `
          <strong>${task.name}</strong>
          <span><u>Deadline</u>: ${task.deadline} </span>
          <span><u>Created:</u> ${date} </span>
          <button onclick="deleteTask(${task.id})">Delete</button>
        `;

        tasksDiv.appendChild(div);
      });
    });
}

document.addEventListener('DOMContentLoaded', loadTasks);

function addTask() {
  const name = prompt("Task name:");
  const deadline = prompt("Deadline (YYYY-MM-DD):");

  if (!name || !deadline) return;

  fetch('/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name,
      deadline: deadline
    })
  })
  .then(res => res.json())
  .then(() => loadTasks());
}

function deleteTask(id) {
  fetch(`/api/tasks/${id}`, {
    method: 'DELETE'
  })
  .then(() => loadTasks());
}

///// TIMER SCRIPT

const display = document.getElementById("display");
let timer = null;
let startTime = 0;
let elapsedTime = 0;
let totalTime = 25 * 60 * 1000;
let isRunning = false;

function set() {
    let input = window.prompt("For how many minutes do you want to work?:");
    let value = Number(input);

    if (Number.isInteger(value)) {
        totalTime = value * 60 * 1000;
        reset();
    } else {
        alert("Enter an integer");
    }
}

function start() {
    if (!isRunning) {
        startTime = Date.now() - elapsedTime;
        timer = setInterval(update,900);
        isRunning = true;
    }
}

function stop() {
    if (isRunning) {
        clearInterval(timer);
        elapsedTime = Date.now() - startTime;
        isRunning = false;

        const minutesWorked = Math.floor(elapsedTime / 60000);
        if (minutesWorked > 0) {
            logSession(minutesWorked);
        }
    }
}

function reset() {
    stop();
    startTime = 0;
    elapsedTime = 0;
    changeDisplay(totalTime);
}

function update() {
    const currentTime = Date.now();
    elapsedTime = currentTime - startTime;
    let remainingTime = totalTime - elapsedTime;

    if (remainingTime <= 0) {
        stop();
        display.textContent = "00:00:00";
        return;
    }

    changeDisplay(remainingTime);
}

function changeDisplay(remainingTime) {
    let hours = Math.floor(remainingTime / (1000*3600));
    let minutes = Math.floor((remainingTime / (1000*60))%60);
    let secondes = Math.floor((remainingTime / 1000)%60);

    hours = String(hours).padStart(2,"0");
    minutes = String(minutes).padStart(2,"0");
    secondes = String(secondes).padStart(2,"0");

    display.textContent = `${hours}:${minutes}:${secondes}`;
}

