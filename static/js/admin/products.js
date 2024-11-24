document.addEventListener('DOMContentLoaded', function() {
    // Price Input Formatting with Thousands Separators
    const priceInput = document.getElementById('id_price');
    const salePriceInput = document.getElementById('id_sale_price');
    const isSaleCheckbox = document.getElementById('id_is_sale');
    const salePriceField = salePriceInput ? salePriceInput.closest('.form-row') : null;

    function formatPriceInput(input) {
        let value = input.value.replace(/\D/g, ''); 
        input.value = new Intl.NumberFormat('de-DE').format(value);  
    }

    if (priceInput) {
        if (priceInput.value) {
            formatPriceInput(priceInput);
        }
        priceInput.addEventListener('input', function(event) {
            formatPriceInput(event.target);
        });
    }

    function toggleSalePriceField() {
        if (isSaleCheckbox.checked) {
            if (salePriceField) salePriceField.style.display = '';  
            if (salePriceInput) {
                salePriceInput.required = true;
                if (!salePriceInput.value) {
                    salePriceInput.value = '0';
                    salePriceInput.focus();
                }
                formatPriceInput(salePriceInput); 
            }
        } else {
            if (salePriceField) salePriceField.style.display = 'none';
            if (salePriceInput) {
                salePriceInput.required = false;
                salePriceInput.value = ''; 
            }
        }
    }

    if (salePriceField && salePriceInput) {
        toggleSalePriceField();
        if (salePriceInput.value) {
            formatPriceInput(salePriceInput);
        }
    }

    if (isSaleCheckbox) {
        isSaleCheckbox.addEventListener('change', toggleSalePriceField);
    }

    if (salePriceInput) {
        salePriceInput.addEventListener('input', function(event) {
            formatPriceInput(event.target);
        });
    }

    // Category and Subcategory Filtering
    const categorySelect = document.getElementById("id_category");
    const subcategorySelect = document.getElementById("id_subcategory");

    if (categorySelect && subcategorySelect) {
        categorySelect.addEventListener("change", function() {
            const categoryId = categorySelect.value;

            // Clear existing options in subcategory dropdown
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
