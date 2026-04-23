// TALARIX APS X5 - Основной JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация
    initNavigation();
    checkSystemStatus();
    
    // Глобальное хранилище для текущего модуля
    window.currentModule = null;
});

// Инициализация навигации
function initNavigation() {
    // Обработчики для заголовков групп
    document.querySelectorAll('.nav-group-header').forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            toggleTree(targetId, this);
        });
    });
    
    // Обработчики для элементов меню
    document.querySelectorAll('.nav-tree-content li').forEach(item => {
        item.addEventListener('click', function() {
            const module = this.getAttribute('data-module');
            const moduleName = this.querySelector('.leaf').textContent;
            loadModule(module, moduleName);
            
            // Подсветка активного элемента
            document.querySelectorAll('.nav-tree-content li').forEach(li => li.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Переключение дерева
function toggleTree(treeId, headerElement) {
    const tree = document.getElementById(treeId);
    const allTrees = document.querySelectorAll('.nav-tree-content');
    const allHeaders = document.querySelectorAll('.nav-group-header');
    
    // Закрываем все остальные деревья
    allTrees.forEach(t => {
        if (t.id !== treeId) {
            t.classList.add('hidden');
        }
    });
    allHeaders.forEach(h => {
        if (h !== headerElement) {
            h.classList.remove('active');
        }
    });
    
    // Переключаем текущее
    tree.classList.toggle('hidden');
    headerElement.classList.toggle('active');
}

// Загрузка модуля
function loadModule(moduleId, moduleName) {
    window.currentModule = moduleId;
    document.getElementById('current-module').textContent = moduleName;
    document.getElementById('page-title').textContent = moduleName.replace(/[📦⚙️🏭📋🗺️🔄👥🕒🏗️🔀🔧📥📤🔒📊📅]\s*/, '');
    
    const workspace = document.getElementById('workspace');
    
    if (moduleId === 'materials') {
        loadMaterialsModule(workspace);
    } else {
        workspace.innerHTML = `
            <div class="welcome-message">
                <h2>Модуль "${moduleName}"</h2>
                <p>Функционал в разработке</p>
            </div>
        `;
    }
}

// Загрузка модуля материалов
function loadMaterialsModule(container) {
    container.innerHTML = `
        <div class="module-container">
            <div class="module-header">
                <h2>Материалы</h2>
                <button class="btn btn-primary" onclick="openMaterialForm()">+ Добавить материал</button>
            </div>
            <div id="materials-table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Название</th>
                            <th>Артикул</th>
                            <th>Контрагент</th>
                            <th>Модель учета</th>
                            <th>Срок хранения (дн.)</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody id="materials-table-body">
                        <tr>
                            <td colspan="6" style="text-align: center; color: #7f8c8d;">Загрузка данных...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    loadMaterialsData();
}

// Загрузка данных материалов
async function loadMaterialsData() {
    try {
        const response = await fetch('/api/materials');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const materials = await response.json();
        
        renderMaterialsTable(materials);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('materials-table-body').innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; color: #e74c3c;">Ошибка загрузки данных. Убедитесь, что сервер запущен.</td>
            </tr>
        `;
    }
}

// Отрисовка таблицы материалов
function renderMaterialsTable(materials) {
    const tbody = document.getElementById('materials-table-body');
    
    if (!materials || materials.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; color: #7f8c8d;">Нет данных</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = materials.map(material => `
        <tr data-id="${material.id || material.article}">
            <td>${material.name || '-'}</td>
            <td>${material.article || '-'}</td>
            <td>${material.counterparty || '-'}</td>
            <td>${material.accounting_model || '-'}</td>
            <td>${material.shelf_life || '-'}</td>
            <td class="actions">
                <button class="btn btn-warning" onclick="editMaterial('${material.id || material.article}')">✏️</button>
                <button class="btn btn-danger" onclick="deleteMaterial('${material.id || material.article}')">🗑️</button>
            </td>
        </tr>
    `).join('');
}

// Открытие формы добавления/редактирования
function openMaterialForm(data = null) {
    const isEdit = !!data;
    const modal = document.createElement('div');
    modal.className = 'form-modal';
    modal.innerHTML = `
        <div class="form-content">
            <h3>${isEdit ? 'Редактировать материал' : 'Новый материал'}</h3>
            <form id="material-form">
                <input type="hidden" id="material-id" value="${data?.id || ''}">
                <div class="form-group">
                    <label for="material-name">Название *</label>
                    <input type="text" id="material-name" required value="${data?.name || ''}">
                </div>
                <div class="form-group">
                    <label for="material-article">Артикул *</label>
                    <input type="text" id="material-article" required value="${data?.article || ''}">
                </div>
                <div class="form-group">
                    <label for="material-counterparty">Контрагент</label>
                    <input type="text" id="material-counterparty" value="${data?.counterparty || ''}">
                </div>
                <div class="form-group">
                    <label for="material-accounting-model">Модель учета</label>
                    <select id="material-accounting-model">
                        <option value="FIFO" ${data?.accounting_model === 'FIFO' ? 'selected' : ''}>FIFO</option>
                        <option value="LIFO" ${data?.accounting_model === 'LIFO' ? 'selected' : ''}>LIFO</option>
                        <option value="AVCO" ${data?.accounting_model === 'AVCO' ? 'selected' : ''}>AVCO</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="material-shelf-life">Срок хранения (дней)</label>
                    <input type="number" id="material-shelf-life" value="${data?.shelf_life || ''}">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeMaterialForm()">Отмена</button>
                    <button type="submit" class="btn btn-primary">${isEdit ? 'Сохранить' : 'Создать'}</button>
                </div>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Обработчик отправки формы
    document.getElementById('material-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveMaterial(isEdit);
    });
}

// Закрытие формы
function closeMaterialForm() {
    const modal = document.querySelector('.form-modal');
    if (modal) modal.remove();
}

// Сохранение материала
async function saveMaterial(isEdit) {
    const data = {
        name: document.getElementById('material-name').value,
        article: document.getElementById('material-article').value,
        counterparty: document.getElementById('material-counterparty').value,
        accounting_model: document.getElementById('material-accounting-model').value,
        shelf_life: parseInt(document.getElementById('material-shelf-life').value) || null
    };
    
    try {
        const url = isEdit ? `/api/materials/${data.article}` : '/api/materials';
        const method = isEdit ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Ошибка сохранения');
        
        closeMaterialForm();
        loadMaterialsData();
    } catch (error) {
        alert('Ошибка при сохранении: ' + error.message);
    }
}

// Редактирование материала
async function editMaterial(id) {
    try {
        const response = await fetch(`/api/materials/${id}`);
        if (!response.ok) throw new Error('Ошибка загрузки');
        const material = await response.json();
        openMaterialForm(material);
    } catch (error) {
        alert('Ошибка загрузки данных: ' + error.message);
    }
}

// Удаление материала
async function deleteMaterial(id) {
    if (!confirm('Вы уверены, что хотите удалить этот материал?')) return;
    
    try {
        const response = await fetch(`/api/materials/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Ошибка удаления');
        loadMaterialsData();
    } catch (error) {
        alert('Ошибка при удалении: ' + error.message);
    }
}

// Проверка статуса системы
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        document.getElementById('system-status').textContent = 'Работает';
        document.getElementById('system-status').classList.remove('error');
        document.getElementById('db-status').textContent = 'Подключена';
        document.getElementById('db-status').classList.remove('error');
    } catch (error) {
        document.getElementById('system-status').textContent = 'Ошибка';
        document.getElementById('system-status').classList.add('error');
        document.getElementById('db-status').textContent = 'Нет связи';
        document.getElementById('db-status').classList.add('error');
    }
}
