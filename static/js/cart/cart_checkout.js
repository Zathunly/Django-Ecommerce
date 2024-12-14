function showCheckoutConfirmationModal() {
    const modalTitle = document.getElementById('warningModalLabel');
    const modalBody = document.getElementById('warningModalBody');
    const confirmButton = document.getElementById('confirmButton');

    // Set modal content
    modalTitle.textContent = 'Checkout Confirmation';
    modalBody.textContent = 'Do you wish to checkout?';
    confirmButton.textContent = 'Proceed';
    confirmButton.classList.remove('btn-danger');
    confirmButton.classList.add('btn-primary');

    // Set the confirm button action
    confirmButton.onclick = function() {
        document.getElementById('checkoutForm').submit(); 
        bootstrap.Modal.getInstance(document.getElementById('warningModal')).hide();
    };

    // Show the modal
    const warningModal = new bootstrap.Modal(document.getElementById('warningModal'));
    warningModal.show();
}
