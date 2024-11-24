function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the clicked section
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }

    document.querySelectorAll('.sidebar ul li a').forEach(link => {
        link.classList.remove('active');
    });

    // Add 'active' class to the clicked link if it exists
    const activeLink = document.getElementById(sectionId + '-link');
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Automatically show the section based on the URL hash
document.addEventListener('DOMContentLoaded', function() {
    const hash = window.location.hash.substring(1); // Get the hash value without the '#'
    if (hash) {
        showSection(hash);
    } else {
        // Default section (if no hash in URL)
        showSection('account-info'); // Change to the default section ID you want
    }
});

// Example for password change success
document.querySelector('.change-pwd-btn').addEventListener('click', function() {
    const url = document.getElementById('change-pwd-btn').getAttribute('data-url');
    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    if (newPassword !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            action: 'update_password',
            new_password: newPassword,
            confirm_password: confirmPassword,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function(response) {
            if (response.success) {
                alert('Password changed successfully!');
                window.location.hash = '#change-password';
                location.reload();
            } else {
                alert('Error: ' + response.error);
            }
        },
        error: function(xhr, errmsg, err) {
            console.error('AJAX error: ' + errmsg);
            console.log('Error details:', xhr, err);
            alert('There was an error. Please try again.');
        }
    });
});
