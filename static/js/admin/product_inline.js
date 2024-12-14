document.addEventListener('DOMContentLoaded', function () {
    const salePercentageInputs = document.querySelectorAll('input[name$="-sale_percentage"]');
    const isSaleCheckboxes = document.querySelectorAll('input[name$="-is_sale"]');
    const priceInputs = document.querySelectorAll('input[name$="-price"]');

    function formatWithThousandsSeparator(value) {
        const number = value.replace(/\D/g, ''); 
        return number.replace(/\B(?=(\d{3})+(?!\d))/g, '.'); 
    }

    function toggleSalePercentageState() {
        isSaleCheckboxes.forEach((checkbox, index) => {
            const salePercentageInput = salePercentageInputs[index];

            function setDisabledState(disable) {
                if (disable) {
                    salePercentageInput.disabled = true;
                    salePercentageInput.style.backgroundColor = '#e0e0e0';
                    salePercentageInput.value = '0'; 
                } else {
                    salePercentageInput.disabled = false;
                    salePercentageInput.style.backgroundColor = ''; 
                    if (!salePercentageInput.value) {
                        salePercentageInput.value = ''; 
                    }
                    salePercentageInput.focus();
                }
            }

            setDisabledState(!checkbox.checked);

            checkbox.addEventListener('change', function () {
                setDisabledState(!checkbox.checked);
            });
        });
    }

    // Format price inputs
    function formatPriceInputs() {
        priceInputs.forEach(input => {
            // Initial formatting on page load
            if (input.value) {
                input.value = formatWithThousandsSeparator(input.value);
            }

            // Add event listener for real-time formatting
            input.addEventListener('input', function (event) {
                const cursorPosition = input.selectionStart;
                const formattedValue = formatWithThousandsSeparator(event.target.value);
                input.value = formattedValue;

                // Preserve cursor position after formatting
                const diff = formattedValue.length - event.target.value.length;
                input.setSelectionRange(cursorPosition + diff, cursorPosition + diff);
            });
        });
    }

    // Initialize
    toggleSalePercentageState();
    formatPriceInputs();
});
