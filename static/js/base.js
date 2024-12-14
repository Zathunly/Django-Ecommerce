$(document).ready(function() {
    $('#spinner-box').show();

    setTimeout(function() {
        $('#spinner-box').hide();
    }, 500); 
});

function showLogoutConfirmationModal(logoutUrl) {
    const modalTitle = document.getElementById('warningModalLabel');
    const modalBody = document.getElementById('warningModalBody');
    const confirmButton = document.getElementById('confirmButton');

    // Set modal content
    modalTitle.textContent = 'Logout Confirmation';
    modalBody.textContent = 'Are you sure you want to log out?';
    confirmButton.textContent = 'Logout';

    // Set the confirm button action
    confirmButton.onclick = function() {
        location.href = logoutUrl; // Redirect to the logout URL
        bootstrap.Modal.getInstance(document.getElementById('warningModal')).hide();
    };

    // Show the modal
    const warningModal = new bootstrap.Modal(document.getElementById('warningModal'));
    warningModal.show();
}

