// Function to toggle select or deselect all checkboxes
function toggleSelectAll(action) {
    const checkboxes = document.querySelectorAll('.product-checkbox');
    
    if (action === 'select') {
        checkboxes.forEach(checkbox => checkbox.checked = true);
    } else if (action === 'deselect') {
        checkboxes.forEach(checkbox => checkbox.checked = false);
    }

    // If using a dropdown, reset the dropdown selection after toggling
    const selectToggle = document.getElementById('select-toggle');
    if (selectToggle) {
        selectToggle.value = "";  
    }
}

// Function to show the confirmation modal
function showWarningModal(action, confirmCallback) {
    const modalTitle = document.getElementById('warningModalLabel');
    const modalBody = document.getElementById('warningModalBody');
    const confirmButton = document.getElementById('confirmButton');

    if (action === 'edit') {
        modalTitle.textContent = 'Edit Confirmation';
        modalBody.textContent = 'Do you want to enable editing mode for your cart?';
        confirmButton.textContent = 'Edit';
        confirmButton.classList.remove('btn-danger');
        confirmButton.classList.add('btn-primary');
    }

    confirmButton.onclick = function() {
        confirmCallback();
        bootstrap.Modal.getInstance(document.getElementById('warningModal')).hide();
    };

    const warningModal = new bootstrap.Modal(document.getElementById('warningModal'));
    warningModal.show();
}

function saveCartChanges() {
    const quantityInputs = document.querySelectorAll(".quantity-input");
    let updatedData = {};

    quantityInputs.forEach(input => {
        const productKey = input.getAttribute("data-product-id");  
        updatedData[productKey] = parseInt(input.value, 10) || 0;   
    });

    const url = document.getElementById("toggle-edit").dataset.url;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            updated_data: JSON.stringify(updatedData),  
            action: 'update',
            csrfmiddlewaretoken: csrfToken
        },
        success: function() {
            location.reload();
        },
        error: function(xhr, errmsg, err) {
            console.error('Error updating cart:', errmsg);
        },
    });
}


// Main document event listener for DOMContentLoaded
document.addEventListener("DOMContentLoaded", function() {
    const editButton = document.getElementById("toggle-edit");
    let isEditable = false;

    // Toggle Edit Mode
    if (editButton) {
        editButton.addEventListener("click", function() {
            if (!isEditable) {
                showWarningModal('edit', enableEditMode);
            } else {
                isEditable = false;
                editButton.textContent = "Edit";
                toggleEditElements(isEditable);
                saveCartChanges();  // Save changes on exit from edit mode
            }
        });
    }

    // Increase Quantity
    document.querySelectorAll(".increase-qty").forEach(button => {
        button.addEventListener("click", function() {
            const productKey = this.getAttribute("data-product-id");  // Get the unique product key (e.g., "2-M")
            const quantityInput = document.getElementById(`quantity-input-${productKey}`);  // Target specific quantity input

            console.log(`Trying to access quantity input with ID: quantity-input-${productKey}`);  // Debugging log

            if (quantityInput) {  // Check if the element exists
                const currentValue = parseInt(quantityInput.value, 10) || 0;
                quantityInput.value = currentValue + 1;
            } else {
                console.warn(`Quantity input with ID 'quantity-input-${productKey}' not found.`);
            }
        });
    });

    // Decrease Quantity
    document.querySelectorAll(".decrease-qty").forEach(button => {
        button.addEventListener("click", function() {
            const productKey = this.getAttribute("data-product-id");  // Get the unique product key (e.g., "2-M")
            const quantityInput = document.getElementById(`quantity-input-${productKey}`);  // Target specific quantity input

            // console.log(`Trying to access quantity input with ID: quantity-input-${productKey}`);  // Debugging log

            if (quantityInput) {  // Check if the element exists
                const currentValue = parseInt(quantityInput.value, 10) || 0;
                if (currentValue > 1) {
                    quantityInput.value = currentValue - 1;
                }
            } else {
                console.warn(`Quantity input with ID 'quantity-input-${productKey}' not found.`);
            }
        });
    });

    // Enable Edit Mode
    function enableEditMode() {
        isEditable = true;
        editButton.textContent = "Save";
        toggleEditElements(isEditable);
    }

    // Toggle Editable Elements State
    function toggleEditElements(isEditable) {
        const quantityInputs = document.querySelectorAll(".quantity-input");
        const decreaseButtons = document.querySelectorAll(".decrease-qty");
        const increaseButtons = document.querySelectorAll(".increase-qty");
        const deleteButtons = document.querySelectorAll(".delete-btn");
        const productCheckboxes = document.querySelectorAll(".product-checkbox");
        const checkboxContainers = document.querySelectorAll(".checkbox-container");

        const headerSelect = document.querySelector(".header-select");
        const headerText = headerSelect ? headerSelect.querySelector(".header-text") : null;
        const selectToggle = headerSelect ? headerSelect.querySelector("#select-toggle") : null;

        // Toggle display or disabled state
        quantityInputs.forEach(input => input.disabled = !isEditable);
        decreaseButtons.forEach(button => {
            button.disabled = !isEditable;
            button.style.display = isEditable ? "inline-block" : "none";
        });
        increaseButtons.forEach(button => {
            button.disabled = !isEditable;
            button.style.display = isEditable ? "inline-block" : "none";
        });
        deleteButtons.forEach(button => {
            button.style.display = isEditable ? "inline-block" : "none";
        });
        productCheckboxes.forEach(checkbox => {
            checkbox.style.display = isEditable ? "inline-block" : "none";
        });
        checkboxContainers.forEach(container => {
            container.style.display = isEditable ? "inline-block" : "none";
        });

        if (headerSelect) {
            headerSelect.style.display = isEditable ? "inline-block" : "none";
        }
        if (headerText) {
            headerText.style.display = isEditable ? "none" : "inline";
        }
        if (selectToggle) {
            selectToggle.style.display = isEditable ? "inline-block" : "none";
        }
    }
});
