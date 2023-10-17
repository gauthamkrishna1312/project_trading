document.querySelector('#sidebar-toggle-btn-1').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent event propagation
    toggleSidebar();
});

document.querySelector('#sidebar-toggle-btn-2').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent event propagation
    toggleSidebar();
});

// Function to toggle the sidebar
function toggleSidebar() {
    var sidenav = document.querySelector('.sidenav');
    sidenav.classList.toggle('open');

    // Check if the sidebar is open
    if (sidenav.classList.contains('open')) {
        // Add a click event listener to the entire document to close the sidebar if clicking outside
        document.addEventListener('click', closeSidebarOnClickOutside);
    } else {
        // Remove the click event listener when the sidebar is closed
        document.removeEventListener('click', closeSidebarOnClickOutside);
    }
}

// Function to close the sidebar when clicking outside
function closeSidebarOnClickOutside(event) {
    var sidenav = document.querySelector('.sidenav');
    if (!sidenav.contains(event.target)) {
        sidenav.classList.remove('open');
        document.removeEventListener('click', closeSidebarOnClickOutside);
    }
}

