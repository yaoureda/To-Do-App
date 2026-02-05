function loadHabits() {
  fetch('/api/habits')
    .then(res => res.json())
    .then(habits => {
      const habitsDiv = document.querySelector('.big-div');
      habitsDiv.innerHTML = '';

      habits.forEach(habit => {
        const div = document.createElement('div');
        div.className = "small-div d-grid gap-2 col-6 mx-auto"
        const date = new Date(habit.created_at).toLocaleString('fr-FR');

        div.innerHTML = `
          <strong>${habit.name}</strong>
          <span><u>Streaks</u>: ${habit.streaks} </span>
          <span><u>Created:</u> ${date} </span>
          <button id="inc" onclick="incrementStreaks(${habit.id},${habit.streaks})">🔥 Increment Streaks</button>
          <button id="reset" onclick="resetStreaks(${habit.id})">🔄 Reset Streaks</button>
          <button onclick="deleteHabit(${habit.id})">Delete</button>
        `;

        habitsDiv.appendChild(div);
      });
    });
}

document.addEventListener('DOMContentLoaded', loadHabits);

function addHabit() {
  const name = prompt("Habit name:");

  if (!name) return;

  fetch('/api/habits', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name,
    })
  })
  .then(res => res.json())
  .then(() => loadHabits());
}

function deleteHabit(id) {
  fetch(`/api/habits/${id}`, {
    method: 'DELETE'
  })
  .then(() => loadHabits());
}

function resetStreaks(id) {
  fetch(`/api/streaks/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      streaks: 0
    })
  })
  .then(() => loadHabits());
}

function incrementStreaks(id, currentStreak) {
  fetch(`/api/streaks/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      streaks: currentStreak + 1
    })
  })
  .then(() => loadHabits());
}

