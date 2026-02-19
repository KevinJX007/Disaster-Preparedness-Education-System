const app = {
    user: { name: "", score: 0, progress: 0 },

    login: function() {
        const nameInput = document.getElementById('username').value;
        if(nameInput) {
            this.user.name = nameInput;
            document.getElementById('hero-name').innerText = nameInput;
            this.showScreen('dashboard-screen');
            this.talk("Great to see you, " + nameInput + "! Choose a mission.");
        }
    },

    showScreen: function(screenId) {
        document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
        document.getElementById(screenId).classList.remove('hidden');
    },

    talk: function(msg) {
        document.getElementById('bubble').innerText = msg;
    },

    startModule: function(type) {
        if(type === 'earthquake') {
            this.showScreen('game-screen');
            this.initEarthquakeGame();
        }
    },

    initEarthquakeGame: function() {
        const canvas = document.getElementById('game-canvas');
        canvas.innerHTML = `
            <div class="choice-container">
                <button class="game-btn" onclick="app.solveTask(true)">🛡️ Get under a Table</button>
                <button class="game-btn" onclick="app.solveTask(false)">🪟 Run to the Window</button>
            </div>
        `;
    },

    solveTask: function(isCorrect) {
        const feedback = document.getElementById('game-feedback');
        if(isCorrect) {
            feedback.innerHTML = "✨ 100 PTS! You're a natural!";
            this.user.score += 100;
            this.updateProgress(25);
            setTimeout(() => this.showScreen('dashboard-screen'), 2000);
        } else {
            feedback.innerHTML = "❌ Careful! Windows can break. Try again!";
        }
    },

    updateProgress: function(amount) {
        this.user.progress += amount;
        document.getElementById('progress-bar').style.width = this.user.progress + "%";
    }
};