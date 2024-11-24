$(document).ready(function() {
    // Increase quantity
    $('.increase-qty').on('click', function() {
        var quantityInput = $('#quantity-input');
        var currentValue = parseInt(quantityInput.val());
        quantityInput.val(currentValue + 1);
    });

    // Decrease quantity
    $('.decrease-qty').on('click', function() {
        var quantityInput = $('#quantity-input');
        var currentValue = parseInt(quantityInput.val());
        if (currentValue > 1) {
            quantityInput.val(currentValue - 1);
        }
    });
});