// Admin interface JavaScript enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            const form = document.querySelector('.prompt-form');
            if (form) {
                e.preventDefault();
                form.submit();
            }
        }
        
        if (e.key === 'Escape') {
            const cancelBtn = document.querySelector('.btn[href="/admin"]');
            if (cancelBtn) {
                window.location.href = '/admin';
            }
        }
    });

    // Auto-focus login input
    const loginInput = document.querySelector('#password');
    if (loginInput) {
        loginInput.focus();
    }

    // Add copy functionality for prompt IDs
    const idCells = document.querySelectorAll('.id-cell code');
    idCells.forEach(cell => {
        cell.style.cursor = 'pointer';
        cell.title = 'Click to copy ID';
        cell.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const original = this.textContent;
                this.textContent = 'Copied!';
                this.style.background = '#d4edda';
                setTimeout(() => {
                    this.textContent = original;
                    this.style.background = '#f1f3f4';
                }, 1000);
            });
        });
    });
});

// Global helper functions
window.confirmDelete = function(description) {
    return confirm('Are you sure you want to delete "' + description + '"? This action cannot be undone.');
}; 