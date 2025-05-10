// Hlavní JavaScript soubor pro FastAPI CMS

document.addEventListener('DOMContentLoaded', function() {
    console.log('FastAPI CMS - JavaScript načten');
    
    // Inicializace všech komponent
    initializeComponents();
    
    // Nastavení událostí pro formuláře
    setupFormValidation();
    
    // Nastavení interaktivních prvků
    setupInteractiveElements();
});

/**
 * Inicializace všech komponent na stránce
 */
function initializeComponents() {
    // Inicializace dropdown menu
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu.classList.contains('show')) {
                dropdownMenu.classList.remove('show');
            } else {
                // Zavřít všechny otevřené dropdown menu
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
                dropdownMenu.classList.add('show');
            }
        });
    });
    
    // Zavřít dropdown menu při kliknutí mimo
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.dropdown-toggle')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
    
    // Inicializace tooltipů
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'tooltip';
            tooltipElement.textContent = tooltipText;
            document.body.appendChild(tooltipElement);
            
            const rect = this.getBoundingClientRect();
            tooltipElement.style.top = rect.bottom + 10 + 'px';
            tooltipElement.style.left = rect.left + (rect.width / 2) - (tooltipElement.offsetWidth / 2) + 'px';
            tooltipElement.classList.add('show');
            
            this.addEventListener('mouseleave', function() {
                tooltipElement.remove();
            });
        });
    });
}

/**
 * Nastavení validace formulářů
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validace povinných polí
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Přidat zprávu o chybě, pokud ještě neexistuje
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        errorMessage.textContent = 'Toto pole je povinné';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                    
                    // Odstranit zprávu o chybě, pokud existuje
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                }
            });
            
            // Validace e-mailu
            const emailFields = form.querySelectorAll('[type="email"]');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            emailFields.forEach(field => {
                if (field.value.trim() && !emailRegex.test(field.value.trim())) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Přidat zprávu o chybě, pokud ještě neexistuje
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        errorMessage.textContent = 'Zadejte platnou e-mailovou adresu';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                }
            });
            
            // Validace shody hesel
            const passwordField = form.querySelector('[name="password"]');
            const confirmPasswordField = form.querySelector('[name="password_confirm"]');
            if (passwordField && confirmPasswordField) {
                if (passwordField.value !== confirmPasswordField.value) {
                    isValid = false;
                    confirmPasswordField.classList.add('is-invalid');
                    
                    // Přidat zprávu o chybě, pokud ještě neexistuje
                    let errorMessage = confirmPasswordField.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        errorMessage.textContent = 'Hesla se neshodují';
                        confirmPasswordField.parentNode.insertBefore(errorMessage, confirmPasswordField.nextSibling);
                    }
                }
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Nastavení interaktivních prvků
 */
function setupInteractiveElements() {
    // Tlačítka pro mazání
    const deleteButtons = document.querySelectorAll('[data-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('data-delete');
            const confirmMessage = this.getAttribute('data-confirm') || 'Opravdu chcete smazat tuto položku?';
            
            if (confirm(confirmMessage)) {
                // Pokud je to odkaz, přesměrovat
                if (this.tagName === 'A') {
                    window.location.href = this.getAttribute('href');
                } 
                // Pokud je to tlačítko v rámci formuláře, odeslat formulář
                else if (this.form) {
                    this.form.submit();
                }
            }
        });
    });
    
    // Tlačítko pro mobilní menu
    const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            const mobileMenu = document.querySelector('.mobile-menu');
            if (mobileMenu) {
                mobileMenu.classList.toggle('show');
            }
        });
    }
    
    // Přepínače záložek
    const tabButtons = document.querySelectorAll('[data-tab]');
    tabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Deaktivovat všechny záložky
            const tabContainer = this.closest('.tabs-container');
            if (tabContainer) {
                tabContainer.querySelectorAll('[data-tab]').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Skrýt všechny obsahy záložek
                tabContainer.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Aktivovat vybranou záložku
                this.classList.add('active');
                
                // Zobrazit obsah vybrané záložky
                const targetTabId = this.getAttribute('data-tab');
                const targetTabContent = tabContainer.querySelector(`#${targetTabId}`);
                if (targetTabContent) {
                    targetTabContent.classList.add('active');
                }
            }
        });
    });
    
    // Automatické zavření alertů
    const autoCloseAlerts = document.querySelectorAll('.alert[data-auto-close]');
    autoCloseAlerts.forEach(alert => {
        const timeout = parseInt(alert.getAttribute('data-auto-close')) || 5000;
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, timeout);
    });
}

/**
 * Zobrazí notifikaci uživateli
 * @param {string} message - Zpráva k zobrazení
 * @param {string} type - Typ notifikace (success, error, warning, info)
 * @param {number} duration - Doba zobrazení v ms
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Přidat notifikaci do dokumentu
    const notificationContainer = document.querySelector('.notification-container');
    if (notificationContainer) {
        notificationContainer.appendChild(notification);
    } else {
        const newNotificationContainer = document.createElement('div');
        newNotificationContainer.className = 'notification-container';
        newNotificationContainer.appendChild(notification);
        document.body.appendChild(newNotificationContainer);
    }
    
    // Zobrazit notifikaci s animací
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Automaticky skrýt notifikaci po určité době
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

/**
 * Odešle AJAX požadavek
 * @param {string} url - URL pro požadavek
 * @param {string} method - HTTP metoda (GET, POST, PUT, DELETE)
 * @param {Object} data - Data k odeslání
 * @param {Function} callback - Callback funkce po dokončení
 */
function sendAjaxRequest(url, method = 'GET', data = null, callback = null) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            if (callback) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    callback(null, response);
                } catch (e) {
                    callback(null, xhr.responseText);
                }
            }
        } else {
            if (callback) {
                callback(new Error(`Request failed with status ${xhr.status}`), null);
            }
        }
    };
    
    xhr.onerror = function() {
        if (callback) {
            callback(new Error('Network error occurred'), null);
        }
    };
    
    if (data) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
}
