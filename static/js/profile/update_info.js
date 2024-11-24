function toggleEdit() {
    const inputs = document.querySelectorAll('.form-control');
    const editButton = document.getElementById('edit-btn');

    if (editButton.textContent === 'Edit') {
        // Enable all input fields for editing
        inputs.forEach(input => input.removeAttribute('readonly'));
        editButton.textContent = 'Save';
    } else {
        // Disable input fields and save the data
        inputs.forEach(input => input.setAttribute('readonly', true));
        editButton.textContent = 'Edit';

        // Call the function to save the data via AJAX
        update_info();
    }
}

function update_info() {
    const usernameElement = document.getElementById('username');
    const firstNameElement = document.getElementById('first_name');
    const lastNameElement = document.getElementById('last_name');
    const emailElement = document.getElementById('email');
    const phoneElement = document.getElementById('phone');
    const address1Element = document.getElementById('address1');
    const address2Element = document.getElementById('address2');
    const cityProvince = document.getElementById('city_province');
    const district = document.getElementById('district');

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    if (!usernameElement || !firstNameElement || !lastNameElement || !emailElement || !csrfToken) {
        console.error("One or more required elements could not be found.");
        return;
    }

    const editButton = document.getElementById('edit-btn');
    const url = editButton.getAttribute('data-url');

    $.ajax({    
        type: 'POST',
        url: url, 
        data: {
            action: 'update_info',
            username: usernameElement ? usernameElement.value : '',
            first_name: firstNameElement ? firstNameElement.value : '',
            last_name: lastNameElement ? lastNameElement.value : '',
            email: emailElement ? emailElement.value : '',
            phone: phoneElement ? phoneElement.value : '',
            district: district ? district.value : '',
            city_province: cityProvince ? cityProvince.value : '',
            address1: address1Element ? address1Element.value : '',
            address2: address2Element ? address2Element.value : '',

            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.success) {
                alert("User info updated successfully!");
                location.reload();  
            } else {
                alert("Error updating user info: " + response.error);
            }
        },
        error: function(xhr, errmsg, err) {
            console.error("AJAX error: " + errmsg);
            console.log("Error details:", xhr, err);
        }
    });
}
