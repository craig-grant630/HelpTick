// Select elements
const resolveButton = document.querySelector('[data-type="resolve-btn"]');
const resolveScreen = document.getElementById('resolve-screen-hidden');
const closeButton = document.getElementById('close');

// Show modal when the "Resolve" button is clicked
resolveButton.addEventListener('click', function() {
    resolveScreen.style.display = 'flex'; // Show modal
});

// Close the modal when the close button is clicked
closeButton.addEventListener('click', function() {
    resolveScreen.style.display = 'none'; // Hide modal
});