// add_to_cart.js

$(document).on('click', '#add-to-cart', function(e) {
    e.preventDefault();

    // Validate Size selection
    if (!selectedSize) {
        alert("Please select a size before adding to cart.");
        return;
    }

    // Validate Color selection
    if (!selectedColor) {
        alert("Please select a color before adding to cart.");
        return;
    }

    var $this = $(this); 
    var url = $this.data('url');
    var productId = $this.val();
    var productQty = $('#quantity-input').val() || 1;
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    var priceText = $this.closest('.product-info').find('.product-price').text().trim();
    var numericPriceText = priceText.replace(' VND', '').replace(/\./g, '').replace(',', '.').replace(/[^0-9.]/g, '');
    var productPrice = parseFloat(numericPriceText);
    
    if (isNaN(productPrice)) {
        console.error("Product price could not be parsed.");
        return;
    }
    
    var attributes = {
        size: selectedSize,
        color: selectedColor // Include color in attributes
    };

    console.log("Data being sent in AJAX:", { 
        product_id: productId,
        product_qty: productQty,
        product_price: productPrice,
        attributes: attributes
    });

    $this.addClass('active');

    $.ajax({
        type: 'POST',
        url: url,
        data: { 
            product_id: productId,
            product_qty: productQty,
            product_price: productPrice,
            attributes: JSON.stringify(attributes),  
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
        },
        success: function(json) {
            document.getElementById('cart_quantity').textContent = json.qty;
            location.reload();
        },
        error: function(xhr, errmsg, err) {
            console.error("AJAX error: " + errmsg);
            console.log("Error details:", xhr, err);
        },
        complete: function() {
            $this.removeClass('active');
        }
    });
});
