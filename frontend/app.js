const USERS_API_URL = 'http://localhost:8000/users/';
const PRODUCTS_API_URL = 'http://localhost:8000/products/';
const CATALOGUES_API_URL = 'http://localhost:8000/catalogues/';


// Auth elements
const loginEmailInput = document.getElementById('login-email');
const loginPasswordInput = document.getElementById('login-password');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const authStatus = document.getElementById('auth-status');

let authToken = localStorage.getItem('token');

function updateAuthUI() {
    if (authToken) {
        loginEmailInput.style.display = 'none';
        loginPasswordInput.style.display = 'none';
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
        authStatus.style.display = 'block';
    } else {
        loginEmailInput.style.display = 'block';
        loginPasswordInput.style.display = 'block';
        loginBtn.style.display = 'block';
        logoutBtn.style.display = 'none';
        authStatus.style.display = 'none';
    }
}

async function apiFetch(url, options = {}) {
    if (!options.headers) options.headers = {};
    if (authToken) {
        options.headers['Authorization'] = `Bearer ${authToken}`;
    }
    const res = await fetch(url, options);
    if (res.status === 401) {
        logout();
        throw new Error('Не авторизован (401). Пожалуйста, войдите.');
    }
    return res;
}

async function login(email, password) {
    loginBtn.disabled = true;
    try {
        const res = await fetch(`${USERS_API_URL}login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!res.ok) throw new Error('Ошибка входа (неверный email или пароль)');
        const data = await res.json();
        authToken = data.access_token;
        localStorage.setItem('token', authToken);
        loginEmailInput.value = '';
        loginPasswordInput.value = '';
        updateAuthUI();
        showToast('Вы вошли в систему');
        fetchUsers();
        fetchProducts().then(() => fetchCatalogues());
    } catch (e) {
        showToast(e.message, 'error');
    } finally {
        loginBtn.disabled = false;
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('token');
    updateAuthUI();
    showToast('Вы вышли из системы');
}

// User elements
const userNameInput = document.getElementById('new-user-name');
const userEmailInput = document.getElementById('new-user-email');
const userPasswordInput = document.getElementById('new-user-password');
const addUserBtn = document.getElementById('add-user-btn');
const userList = document.getElementById('user-list');
const userCount = document.getElementById('user-count');

// Product elements
const productNameInput = document.getElementById('new-product-name');
const productPriceInput = document.getElementById('new-product-price');
const productAmountInput = document.getElementById('new-product-amount');
const addProductBtn = document.getElementById('add-product-btn');
const productList = document.getElementById('product-list');
const productCount = document.getElementById('product-count');

// Catalogue elements
const catalogueNameInput = document.getElementById('new-catalogue-name');
const addCatalogueBtn = document.getElementById('add-catalogue-btn');
const catalogueList = document.getElementById('catalogue-list');
const catalogueCount = document.getElementById('catalogue-count');

const toast = document.getElementById('toast');

let allProducts = []; // Cache to populate catalogue dropdowns

// ── Цвета аватарок ──
const COLORS = [
    'linear-gradient(135deg, #6c5ce7, #a29bfe)',
    'linear-gradient(135deg, #00b894, #55efc4)',
    'linear-gradient(135deg, #e17055, #fab1a0)',
    'linear-gradient(135deg, #0984e3, #74b9ff)',
    'linear-gradient(135deg, #fdcb6e, #f39c12)',
    'linear-gradient(135deg, #e84393, #fd79a8)',
    'linear-gradient(135deg, #00cec9, #81ecec)',
    'linear-gradient(135deg, #6c5ce7, #fd79a8)',
];

function getColor(id) {
    if (typeof id === 'string') {
        let hash = 0;
        for (let i = 0; i < id.length; i++) {
            hash = id.charCodeAt(i) + ((hash << 5) - hash);
        }
        return COLORS[Math.abs(hash) % COLORS.length];
    }
    return COLORS[id % COLORS.length];
}

function getInitials(name) {
    return name ? name.charAt(0).toUpperCase() : '?';
}

// ── Toast уведомления ──
let toastTimeout;
function showToast(message, type = 'success') {
    clearTimeout(toastTimeout);
    toast.textContent = message;
    toast.className = `toast ${type}`;
    requestAnimationFrame(() => toast.classList.add('show'));
    toastTimeout = setTimeout(() => toast.classList.remove('show'), 2500);
}

// ── Общие функции ──
function showLoading(container) {
    container.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка…</p>
        </div>`;
}

function showError(container, msg) {
    container.innerHTML = `
        <div class="error-state">
            <div class="icon">⚠️</div>
            <p>${msg}</p>
        </div>`;
}

function escapeHtml(text) {
    if (text === undefined || text === null) return '';
    const el = document.createElement('span');
    el.textContent = text;
    return el.innerHTML;
}

// ── Рендер Пользователей ──
function renderUsers(users) {
    userCount.textContent = users.length ? `${users.length} чел.` : '';

    if (users.length === 0) {
        userList.innerHTML = `
            <div class="empty-state">
                <div class="icon">👤</div>
                <p>Нет пользователей. Добавьте первого!</p>
            </div>`;
        return;
    }

    userList.innerHTML = '';
    
    const userSelect = document.getElementById('new-product-user');
    userSelect.innerHTML = '<option value="">Выберите пользователя...</option>';

    users.forEach((user, i) => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.style.animationDelay = `${i * 0.05}s`;
        card.innerHTML = `
            <div class="avatar" style="background: ${getColor(user.id)}">${getInitials(user.name)}</div>
            <div class="user-info">
                <div class="user-name">${escapeHtml(user.name)}</div>
                <div class="user-id">ID: ${user.id}</div>
            </div>
            <button class="btn-delete" title="Удалить" data-type="user" data-id="${user.id}">✕</button>
        `;
        userList.appendChild(card);

        const option = document.createElement('option');
        option.value = user.id;
        option.textContent = user.name;
        userSelect.appendChild(option);
    });
}

// ── Рендер Товаров ──
function renderProducts(products) {
    productCount.textContent = products.length ? `${products.length} шт.` : '';

    if (products.length === 0) {
        productList.innerHTML = `
            <div class="empty-state">
                <div class="icon">📦</div>
                <p>Нет товаров. Добавьте первый!</p>
            </div>`;
        return;
    }

    productList.innerHTML = '';
    products.forEach((product, i) => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.style.animationDelay = `${i * 0.05}s`;
        const pId = product.id || i;
        card.innerHTML = `
            <div class="avatar" style="background: ${getColor(pId)}">📦</div>
            <div class="user-info">
                <div class="user-name">${escapeHtml(product.name)}</div>
                <div class="user-id">Цена: ${escapeHtml(product.price)} | Кол-во: ${escapeHtml(product.amount)} | UserID: ${escapeHtml(product.user_id)}</div>
            </div>
            <button class="btn-delete" title="Удалить" data-type="product" data-id="${pId}">✕</button>
        `;
        productList.appendChild(card);
    });
}

// ── Рендер Каталогов ──
async function renderCatalogues(catalogues) {
    catalogueCount.textContent = catalogues.length ? `${catalogues.length} шт.` : '';

    if (catalogues.length === 0) {
        catalogueList.innerHTML = `
            <div class="empty-state">
                <div class="icon">📁</div>
                <p>Нет каталогов. Добавьте первый!</p>
            </div>`;
        return;
    }

    catalogueList.innerHTML = '';
    
    // Fetch products for each catalogue
    const catalogueProducts = {};
    await Promise.all(catalogues.map(async (cat) => {
        try {
            const res = await apiFetch(`${CATALOGUES_API_URL}${cat.id}/products`);
            if (res.ok) {
                catalogueProducts[cat.id] = await res.json();
            }
        } catch(e) {
            catalogueProducts[cat.id] = [];
        }
    }));

    catalogues.forEach((cat, i) => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.style.flexDirection = 'column';
        card.style.alignItems = 'stretch';
        card.style.animationDelay = `${i * 0.05}s`;
        
        const catProds = catalogueProducts[cat.id] || [];
        
        const prodListHtml = catProds.map(p => `
            <li style="margin-bottom: 4px; display:flex; align-items:center; gap: 8px;">
                <button class="btn-delete" style="width:20px; height:20px; font-size:10px; display:inline-flex;" data-type="del-cat-prod" data-cat="${cat.id}" data-prod="${p.id}">✕</button>
                <span>${escapeHtml(p.name)} (Цена: ${p.price})</span>
            </li>
        `).join('');

        const prodOptions = allProducts.map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('');

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="avatar" style="background: ${getColor(cat.id)}">📁</div>
                    <div class="user-info">
                        <div class="user-name">${escapeHtml(cat.name)}</div>
                        <div class="user-id">ID: ${cat.id}</div>
                    </div>
                </div>
                <button class="btn-delete" title="Удалить" data-type="catalogue" data-id="${cat.id}">✕</button>
            </div>
            
            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 13px; color: #999; margin-bottom: 5px;">Товары в каталоге:</div>
                <ul style="list-style: none; font-size: 14px; margin-bottom: 10px; color: #e0e0e0;">
                   ${prodListHtml || '<li style="color: #666; font-size: 13px;">Пусто</li>'}
                </ul>
                <div class="input-row" style="margin-top: 10px;">
                    <select id="select-cat-${cat.id}">
                        <option value="">Добавить товар...</option>
                        ${prodOptions}
                    </select>
                    <button class="btn-add" style="padding: 8px 16px; flex: 0 0 auto;" data-type="add-to-cat" data-id="${cat.id}">Добавить</button>
                </div>
            </div>
        `;
        catalogueList.appendChild(card);
    });
}

// ── API Пользователи ──
async function fetchUsers() {
    showLoading(userList);
    try {
        const res = await apiFetch(USERS_API_URL);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const users = await res.json();
        renderUsers(users);
    } catch (e) {
        showError(userList, `Не удалось загрузить: ${e.message}`);
    }
}

async function addUser(name, email, password) {
    addUserBtn.disabled = true;
    try {
        const res = await apiFetch(`${USERS_API_URL}register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        userNameInput.value = '';
        userEmailInput.value = '';
        userPasswordInput.value = '';
        showToast(`${name} успешно зарегистрирован!`);
        await fetchUsers();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    } finally {
        addUserBtn.disabled = false;
    }
}

async function deleteUser(id) {
    try {
        const res = await apiFetch(`${USERS_API_URL}${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showToast('Пользователь удалён');
        await fetchUsers();
        await fetchProducts();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    }
}

// ── API Товары ──
async function fetchProducts() {
    showLoading(productList);
    try {
        const res = await apiFetch(PRODUCTS_API_URL);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        allProducts = await res.json();
        renderProducts(allProducts);
        // Also re-render catalogues to update their dropdowns
        await fetchCatalogues(false);
    } catch (e) {
        showError(productList, `Не удалось загрузить: ${e.message}`);
    }
}

async function addProduct(name, price, amount, userId) {
    addProductBtn.disabled = true;
    try {
        const res = await apiFetch(PRODUCTS_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, price: parseInt(price, 10), amount: parseInt(amount, 10), user_id: userId }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        productNameInput.value = '';
        productPriceInput.value = '';
        productAmountInput.value = '';
        document.getElementById('new-product-user').value = '';
        showToast(`${name} добавлен`);
        await fetchProducts();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    } finally {
        addProductBtn.disabled = false;
    }
}

async function deleteProduct(id) {
    try {
        const res = await apiFetch(`${PRODUCTS_API_URL}${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showToast('Товар удалён');
        await fetchProducts();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    }
}

// ── API Каталоги ──
async function fetchCatalogues(showSpinner = true) {
    if (showSpinner) showLoading(catalogueList);
    try {
        const res = await apiFetch(CATALOGUES_API_URL);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const catalogues = await res.json();
        await renderCatalogues(catalogues);
    } catch (e) {
        showError(catalogueList, `Не удалось загрузить: ${e.message}`);
    }
}

async function addCatalogue(name) {
    addCatalogueBtn.disabled = true;
    try {
        const res = await apiFetch(CATALOGUES_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        catalogueNameInput.value = '';
        showToast(`Каталог ${name} добавлен`);
        await fetchCatalogues();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    } finally {
        addCatalogueBtn.disabled = false;
    }
}

async function deleteCatalogue(id) {
    try {
        const res = await apiFetch(`${CATALOGUES_API_URL}${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showToast('Каталог удалён');
        await fetchCatalogues();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    }
}

async function addProductToCatalogue(catId, prodId) {
    try {
        const res = await apiFetch(`${CATALOGUES_API_URL}${catId}/products/${prodId}`, { method: 'POST' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showToast('Товар добавлен в каталог');
        await fetchCatalogues();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    }
}

async function deleteProductFromCatalogue(catId, prodId) {
    try {
        const res = await apiFetch(`${CATALOGUES_API_URL}${catId}/products/${prodId}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showToast('Товар убран из каталога');
        await fetchCatalogues();
    } catch (e) {
        showToast(`Ошибка: ${e.message}`, 'error');
    }
}


// ── Обработчики Авторизации ──
loginBtn.addEventListener('click', () => {
    login(loginEmailInput.value.trim(), loginPasswordInput.value.trim());
});
logoutBtn.addEventListener('click', logout);

[loginEmailInput, loginPasswordInput].forEach(input => {
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') loginBtn.click();
    });
});
updateAuthUI();

// ── Обработчики Пользователи ──
addUserBtn.addEventListener('click', () => {
    const name = userNameInput.value.trim();
    const email = userEmailInput.value.trim();
    const password = userPasswordInput.value.trim();
    if (!name || !email || !password) return showToast('Заполните все поля (имя, email, пароль)', 'error');
    addUser(name, email, password);
});

[userNameInput, userEmailInput, userPasswordInput].forEach(input => {
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') addUserBtn.click();
    });
});

userList.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-delete');
    if (btn && btn.dataset.type === 'user') deleteUser(btn.dataset.id);
});

// ── Обработчики Товары ──
addProductBtn.addEventListener('click', () => {
    const name = productNameInput.value.trim();
    const price = productPriceInput.value.trim();
    const amount = productAmountInput.value.trim();
    const userId = document.getElementById('new-product-user').value;

    if (!name || !price || !amount || !userId) {
        return showToast('Заполните все поля товара и выберите пользователя', 'error');
    }
    addProduct(name, price, amount, userId);
});

[productNameInput, productPriceInput, productAmountInput].forEach(input => {
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') addProductBtn.click();
    });
});

productList.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-delete');
    if (btn && btn.dataset.type === 'product') deleteProduct(btn.dataset.id);
});

// ── Обработчики Каталоги ──
addCatalogueBtn.addEventListener('click', () => {
    const name = catalogueNameInput.value.trim();
    if (!name) return showToast('Введите название каталога', 'error');
    addCatalogue(name);
});

catalogueNameInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addCatalogueBtn.click();
});

catalogueList.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-delete');
    const addBtn = e.target.closest('.btn-add');

    if (btn) {
        if (btn.dataset.type === 'catalogue') {
            deleteCatalogue(btn.dataset.id);
        } else if (btn.dataset.type === 'del-cat-prod') {
            deleteProductFromCatalogue(btn.dataset.cat, btn.dataset.prod);
        }
    } else if (addBtn && addBtn.dataset.type === 'add-to-cat') {
        const catId = addBtn.dataset.id;
        const prodId = document.getElementById(`select-cat-${catId}`).value;
        if (!prodId) return showToast('Выберите товар для добавления', 'error');
        addProductToCatalogue(catId, prodId);
    }
});

// ── Старт ──
fetchUsers();
fetchProducts().then(() => fetchCatalogues());