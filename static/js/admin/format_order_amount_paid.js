document.addEventListener('DOMContentLoaded', () => {
    const readonlyDiv = document.querySelector('.readonly');

    function formatNumberWithDots(value) {
        // Remove any non-digit characters except for the decimal point
        let numericValue = value.replace(/[^\d.]/g, '');
        
        // If there's a decimal point, split into integer and decimal parts
        let [integerPart, decimalPart] = numericValue.split('.');
        
        // Format the integer part with dots as thousands separators
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

        // Return the formatted integer part only, ignoring ".0"
        return decimalPart && decimalPart !== '0' ? `${integerPart}.${decimalPart}` : integerPart;
    }

    if (readonlyDiv) {
        const rawValue = readonlyDiv.textContent.trim(); // Get the raw text inside the div
        readonlyDiv.textContent = formatNumberWithDots(rawValue); // Format and update the div's content
    }
});
