document.addEventListener('DOMContentLoaded', () => {
    const readonlyDiv = document.querySelector('.readonly');

    function formatNumberWithDots(value) {
        let numericValue = value.replace(/[^\d.]/g, '');
        
        let [integerPart, decimalPart] = numericValue.split('.');
        
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

        return decimalPart && decimalPart !== '0' ? `${integerPart}.${decimalPart}` : integerPart;
    }

    if (readonlyDiv) {
        const rawValue = readonlyDiv.textContent.trim(); 
        readonlyDiv.textContent = formatNumberWithDots(rawValue); 
    }
});
