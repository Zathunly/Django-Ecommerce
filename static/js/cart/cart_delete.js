$(document).on('click', '.delete-btn', function(e) {
    e.preventDefault();
    
    const url = $(this).data('url');
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    const selectedProductKeys = [];
    $('.product-checkbox:checked').each(function() {
        selectedProductKeys.push($(this).data('product-id'));
    });

    if (selectedProductKeys.length > 0) {
        showDeleteConfirmationModal(url, selectedProductKeys, csrfToken);
    } else {
        alert("Please select at least one product to delete.");
    }
});

function showDeleteConfirmationModal(url, productKeys, csrfToken) {
    const modalTitle = document.getElementById('warningModalLabel');
    const modalBody = document.getElementById('warningModalBody');
    const confirmButton = document.getElementById('confirmButton');

    modalTitle.textContent = 'Delete Confirmation';
    modalBody.textContent = 'Are you sure you want to delete the selected items?';
    confirmButton.textContent = 'Delete';
    confirmButton.classList.remove('btn-success');
    confirmButton.classList.add('btn-danger');

    confirmButton.onclick = function() {
        deleteCartItems(url, productKeys, csrfToken);
        bootstrap.Modal.getInstance(document.getElementById('warningModal')).hide();
    };
    const warningModal = new bootstrap.Modal(document.getElementById('warningModal'));
    warningModal.show();
}

function deleteCartItems(url, productKeys, csrfToken) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            product_keys: JSON.stringify(productKeys),  
            csrfmiddlewaretoken: csrfToken,
            action: 'delete',
        },
        success: function(response) {
            if (response.status === "success") {
                location.reload();
            } else {
                console.error("Error:", response.error);
            }
        },
        error: function(xhr, errmsg, err) {
            console.error("AJAX error:", errmsg);
        },
    });
}
