// Проверка статуса системы при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    checkHealth();
});

async function checkHealth() {
    const statusElement = document.getElementById('health-status');
    
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusElement.innerHTML = `
                <p class="status-healthy">✓ Система работает нормально</p>
                <p>Сервис: ${data.service}</p>
                <p>Время проверки: ${new Date().toLocaleTimeString('ru-RU')}</p>
            `;
        } else {
            statusElement.innerHTML = `
                <p class="status-error">⚠ Проблема с сервисом</p>
                <p>Статус: ${data.status}</p>
            `;
        }
    } catch (error) {
        statusElement.innerHTML = `
            <p class="status-error">✗ Ошибка подключения к API</p>
            <p>${error.message}</p>
        `;
    }
}
