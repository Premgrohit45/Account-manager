// Encryption utilities using Web Crypto API
class CryptoUtils {
    static async generateKey(password, salt) {
        const encoder = new TextEncoder();
        const passwordBuffer = encoder.encode(password);
        const saltBuffer = encoder.encode(salt);

        // Derive key using PBKDF2
        const keyMaterial = await window.crypto.subtle.importKey(
            'raw',
            passwordBuffer,
            { name: 'PBKDF2' },
            false,
            ['deriveBits', 'deriveKey']
        );

        return await window.crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: saltBuffer,
                iterations: 100000,
                hash: 'SHA-256'
            },
            keyMaterial,
            { name: 'AES-GCM', length: 256 },
            true,
            ['encrypt', 'decrypt']
        );
    }

    static async encrypt(text, key) {
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        
        const encrypted = await window.crypto.subtle.encrypt(
            { name: 'AES-GCM', iv: iv },
            key,
            data
        );

        return {
            encrypted: Array.from(new Uint8Array(encrypted)),
            iv: Array.from(iv)
        };
    }

    static async decrypt(encryptedData, iv, key) {
        const decrypted = await window.crypto.subtle.decrypt(
            { name: 'AES-GCM', iv: new Uint8Array(iv) },
            key,
            new Uint8Array(encryptedData)
        );

        return new TextDecoder().decode(decrypted);
    }
}

// Password strength checker using zxcvbn
function checkPasswordStrength(password) {
    const result = zxcvbn(password);
    const strengthMap = {
        0: { class: 'strength-weak', text: 'Weak' },
        1: { class: 'strength-weak', text: 'Weak' },
        2: { class: 'strength-fair', text: 'Fair' },
        3: { class: 'strength-good', text: 'Good' },
        4: { class: 'strength-strong', text: 'Strong' }
    };
    return strengthMap[result.score];
}

// Password generator
function generatePassword(length = 16, options = {
    uppercase: true,
    lowercase: true,
    numbers: true,
    symbols: true
}) {
    const chars = {
        uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        lowercase: 'abcdefghijklmnopqrstuvwxyz',
        numbers: '0123456789',
        symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
    };

    let allowedChars = '';
    for (const [key, value] of Object.entries(options)) {
        if (value) allowedChars += chars[key];
    }

    let password = '';
    const array = new Uint32Array(length);
    window.crypto.getRandomValues(array);
    
    for (let i = 0; i < length; i++) {
        password += allowedChars[array[i] % allowedChars.length];
    }

    return password;
}

// AJAX request wrapper
async function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

// Show/hide password toggle
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('password-toggle')) {
        const input = e.target.closest('.input-group').querySelector('input');
        const icon = e.target.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
});

// Password strength meter
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('password-input')) {
        const meter = e.target.closest('.form-group').querySelector('.password-strength-meter');
        const feedback = e.target.closest('.form-group').querySelector('.password-feedback');
        
        if (meter && feedback) {
            const strength = checkPasswordStrength(e.target.value);
            meter.className = 'password-strength-meter ' + strength.class;
            feedback.textContent = strength.text;
        }
    }
});

// Logout functionality
document.getElementById('logoutBtn')?.addEventListener('click', async function(e) {
    e.preventDefault();
    try {
        await makeRequest('/logout', 'POST');
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout failed:', error);
    }
});

// Search functionality
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(async () => {
            try {
                const results = await makeRequest(`/search?q=${encodeURIComponent(e.target.value)}`);
                // Update UI with search results
                updateSearchResults(results);
            } catch (error) {
                console.error('Search failed:', error);
            }
        }, 300);
    });
}

// Update search results in the UI
function updateSearchResults(results) {
    const container = document.querySelector('.search-results');
    if (!container) return;

    container.innerHTML = results.map(result => `
        <div class="card priority-${result.priority}">
            <div class="card-body">
                <h5 class="card-title">${result.name}</h5>
                <span class="badge badge-${result.type}">${result.type}</span>
                <p class="card-text">${result.username}</p>
                <button class="btn btn-primary btn-sm view-password" 
                        data-id="${result.id}">
                    View Password
                </button>
            </div>
        </div>
    `).join('');
}

// Loading spinner
function showSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-overlay';
    spinner.innerHTML = `
        <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideSpinner() {
    const spinner = document.querySelector('.spinner-overlay');
    if (spinner) {
        spinner.remove();
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    const tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltips.map(tooltip => new bootstrap.Tooltip(tooltip));

    const popovers = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popovers.map(popover => new bootstrap.Popover(popover));
}); 