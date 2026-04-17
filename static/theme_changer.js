document.addEventListener('DOMContentLoaded', () => {
    const themeDropdownItems = document.querySelectorAll('.theme-dropdown-item');
    
    // Apply the saved theme on page load
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Add click event listeners to dropdown items
    themeDropdownItems.forEach(item => {
        item.addEventListener('click', () => {
            const selectedTheme = item.getAttribute('data-theme');
            document.documentElement.setAttribute('data-theme', selectedTheme);
            localStorage.setItem('theme', selectedTheme);
        });
    });
});