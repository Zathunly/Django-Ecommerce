document.addEventListener('DOMContentLoaded', function () {
    const priceInput = document.getElementById('id_price');
    const salePercentageInput = document.getElementById('id_sale_percentage');
    const isSaleCheckbox = document.getElementById('id_is_sale');
    const salePriceDiv = document.querySelector('.readonly'); // Select the readonly sale price div
    const salePercentageField = salePercentageInput ? salePercentageInput.closest('.form-row') || salePercentageInput.parentElement : null;

    function formatPriceInput(input) {
        let value = input.value.replace(/\D/g, ''); // Remove all non-digit characters
        input.value = value ? new Intl.NumberFormat('de-DE').format(value) : ''; // Add thousands separator or clear
    }

    // Ensure sale_percentage is always included in the form submission
    function ensureSalePercentageSubmission() {
        if (!salePercentageInput) return;

        if (isSaleCheckbox.checked) {
            salePercentageInput.disabled = false;
            salePercentageInput.required = true;
        } else {
            salePercentageInput.disabled = false; // Ensure it is submitted
            salePercentageInput.required = false;
            salePercentageInput.value = '0'; // Set value to 0
        }
    }

    // Format price input on load and input events
    if (priceInput) {
        priceInput.value && formatPriceInput(priceInput);
        priceInput.addEventListener('input', event => formatPriceInput(event.target));
    }

    // Toggle sale price and sale percentage visibility
    function toggleSaleFields() {
        if (isSaleCheckbox.checked) {
            // Show and enable the sale percentage field and sale price div
            if (salePercentageField) salePercentageField.style.display = '';
            if (salePriceDiv) salePriceDiv.style.display = '';
            if (salePercentageInput) {
                salePercentageInput.disabled = false;
                salePercentageInput.required = true;
            }
        } else {
            // Hide the sale percentage field and sale price div
            if (salePercentageField) salePercentageField.style.display = 'none';
            if (salePriceDiv) salePriceDiv.style.display = 'none';
        }
        ensureSalePercentageSubmission(); // Always ensure a value for sale_percentage
    }

    // Initialize on page load
    if (isSaleCheckbox) {
        toggleSaleFields(); // Ensure fields are correctly initialized
        isSaleCheckbox.addEventListener('change', toggleSaleFields); // Add toggle listener
    }

    const categorySelect = document.getElementById("id_category");
    const subcategorySelect = document.getElementById("id_subcategory");

    if (categorySelect && subcategorySelect) {
        categorySelect.addEventListener("change", function () {
            const categoryId = categorySelect.value;
            subcategorySelect.innerHTML = '<option value="">Select subcategory</option>';

            if (categoryId) {
                fetch(`/get-subcategories/?category_id=${categoryId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.subcategories.forEach(subcategory => {
                            const option = new Option(subcategory.name, subcategory.id);
                            subcategorySelect.add(option);
                        });
                        subcategorySelect.disabled = false;
                    })
                    .catch(error => console.error('Error fetching subcategories:', error));
            } else {
                subcategorySelect.disabled = true;
            }
        });
    }
});
