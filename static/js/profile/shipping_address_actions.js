async function deleteAddress(addressId) {
    if (!confirm('Are you sure you want to delete this address?')) {
        return;
    }

    try {
        const response = await fetch(`/profile/delete-address/${addressId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            document.getElementById(`address-string-${addressId}`).remove();
            alert("Address deleted successfully.");
        } else {
            alert("Failed to delete the address. Please try again.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred while deleting the address.");
    }
}


function toggleEditForm(addressId) {
    const addressString = document.getElementById(`address-string-${addressId}`);
    const editForm = document.getElementById(`edit-form-${addressId}`);

    if (editForm.style.display === "none" || editForm.style.display === "") {
        addressString.style.display = "none";
        editForm.style.display = "block";
    } else {
        addressString.style.display = "block";
        editForm.style.display = "none";
    }
}

// Function to toggle the display of the add new address form
function toggleAddForm() {
    const addForm = document.getElementById("add-address-form");
    addForm.style.display = addForm.style.display === "none" ? "block" : "none";
}

