const API_BASE = 'https://your-render-app.onrender.com';
const form = document.getElementById('botForm');
const statusContainer = document.getElementById('statusContainer');
const sessionCount = document.getElementById('sessionCount');
const botsCount = document.getElementById('botsCount');
const serverStatus = document.getElementById('serverStatus');

let totalBots = 0;
let activeSessions = {};

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const gamePin = document.getElementById('gamePin').value;
    const baseName = document.getElementById('baseName').value;
    const nbBots = parseInt(document.getElementById('nbBots').value);
    const autoReconnect = document.getElementById('autoReconnect').checked;

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading">⌛</span> Démarrage...';

    try {
        const formData = new FormData();
        formData.append('game_pin', gamePin);
        formData.append('base_name', baseName);
        formData.append('nb_bots', nbBots);
        formData.append('auto_reconnect', autoReconnect);

        const response = await fetch(`${API_BASE}/api/start`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showAlert(data.error, 'error');
        } else {
            showAlert(`✅ ${data.message}`, 'success');
            activeSessions[data.session_id] = {
                count: nbBots,
                gamePin: gamePin,
                baseName: baseName
            };
            totalBots += nbBots;
            updateStatus();
            form.reset();
        }
    } catch (error) {
        showAlert(`❌ Erreur: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

async function stopSession(sessionId) {
    if (!confirm('Arrêter cette session ?')) return;

    try {
        const response = await fetch(`${API_BASE}/api/stop/${sessionId}`, {
            method: 'GET'
        });

        const data = await response.json();

        if (data.status === 'stopped') {
            const bots = activeSessions[sessionId].count;
            totalBots -= bots;
            delete activeSessions[sessionId];
            updateStatus();
            showAlert(`✅ Session arrêtée`, 'success');
        }
    } catch (error) {
        showAlert(`❌ Erreur: ${error.message}`, 'error');
    }
}

function updateStatus() {
    const count = Object.keys(activeSessions).length;
    sessionCount.textContent = count;
    botsCount.textContent = totalBots;

    if (count === 0) {
        statusContainer.innerHTML = '<p class="empty-state">Aucune session active</p>';
    } else {
        statusContainer.innerHTML = Object.entries(activeSessions).map(([id, data]) => `
            <div class="session-item">
                <div class="session-info">
                    <div class="session-id">Session: ${id}</div>
                    <div class="session-details">
                        Code: ${data.gamePin} | Bots: ${data.count} | Nom: ${data.baseName}
                    </div>
                </div>
                <button class="btn btn-danger" onclick="stopSession('${id}')">Arrêter</button>
            </div>
        `).join('');
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.form-card');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 4000);
}

async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`, { method: 'GET' });
        if (response.ok) {
            serverStatus.textContent = '🟢 Connecté';
            serverStatus.style.color = 'var(--success)';
        } else {
            serverStatus.textContent = '🔴 Erreur';
            serverStatus.style.color = 'var(--danger)';
        }
    } catch (error) {
        serverStatus.textContent = '🔴 Hors ligne';
        serverStatus.style.color = 'var(--danger)';
    }
}

checkServerStatus();
setInterval(checkServerStatus, 30000);
