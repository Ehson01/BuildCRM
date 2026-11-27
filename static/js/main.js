/**
 * BuildCRM 2026 Modern Interactive UI Engine
 * Vanilla JS micro-framework with zero dependencies
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initAlertAutoDismiss();
    initQuickTableSearch();
    initButtonMicroInteractions();
    initKeyboardShortcuts();
});

/**
 * Mobile Navigation Drawer Toggle
 */
function initMobileNav() {
    const toggleBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.main-nav');

    if (toggleBtn && nav) {
        toggleBtn.addEventListener('click', () => {
            const isOpen = nav.classList.toggle('show');
            toggleBtn.setAttribute('aria-expanded', isOpen);
            toggleBtn.innerHTML = isOpen 
                ? '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
                : '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>';
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && nav.classList.contains('show')) {
                nav.classList.remove('show');
                toggleBtn.setAttribute('aria-expanded', 'false');
                toggleBtn.innerHTML = '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>';
            }
        });
    }
}

/**
 * Modern Toast / Alert Notifications Auto-Dismiss
 */
function initAlertAutoDismiss() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.background = 'transparent';
        closeBtn.style.border = 'none';
        closeBtn.style.fontSize = '18px';
        closeBtn.style.lineHeight = '1';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.opacity = '0.6';
        closeBtn.style.padding = '0 0 0 12px';
        closeBtn.style.color = 'currentColor';
        closeBtn.title = 'Dismiss';
        closeBtn.addEventListener('click', () => dismissAlert(alert));
        alert.appendChild(closeBtn);

        // Auto dismiss after 6 seconds for non-error alerts
        if (!alert.classList.contains('alert-danger') && !alert.classList.contains('alert-error')) {
            setTimeout(() => {
                dismissAlert(alert);
            }, 6000);
        }
    });

    function dismissAlert(alertEl) {
        alertEl.style.transition = 'opacity 0.25s ease, transform 0.25s ease, max-height 0.3s ease, margin 0.3s ease';
        alertEl.style.opacity = '0';
        alertEl.style.transform = 'translateY(-6px)';
        setTimeout(() => {
            alertEl.style.maxHeight = '0';
            alertEl.style.margin = '0';
            alertEl.style.padding = '0';
            alertEl.style.overflow = 'hidden';
            setTimeout(() => alertEl.remove(), 300);
        }, 200);
    }
}

/**
 * Instant Client-Side Table Filter (progressive enhancement)
 */
function initQuickTableSearch() {
    const searchInputs = document.querySelectorAll('input[name="search"], input[type="search"]');
    searchInputs.forEach((input) => {
        const table = document.querySelector('.data-table');
        if (!table) return;

        input.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach((row) => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Button Micro-Interactions
 */
function initButtonMicroInteractions() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((btn) => {
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        btn.addEventListener('mouseup', function() {
            this.style.transform = '';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

/**
 * Power-user Keyboard Shortcuts
 * Press '/' to focus search input
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            const searchInput = document.querySelector('input[type="text"], input[name="search"]');
            if (searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        }
    });
}
