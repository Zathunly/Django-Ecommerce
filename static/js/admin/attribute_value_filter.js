(function ($) {
    $(document).ready(function () {
        // Listen for changes on the ProductAttribute dropdown
        $(document).on("change", ".field-attribute select", function () {
            const attributeField = $(this);
            const selectedAttributeId = attributeField.val(); // Get selected attribute ID

            // Find the corresponding AttributeValue dropdown
            const valueField = attributeField.closest("tr").find(".field-value select");

            // Clear the current options
            valueField.html('<option value="">---------</option>');

            if (selectedAttributeId) {
                // Fetch the attribute values using AJAX
                const url = `/get_attribute_values/${selectedAttributeId}/`;

                $.getJSON(url, function (data) {
                    // Populate the AttributeValue dropdown with the results
                    $.each(data, function (index, item) {
                        valueField.append(
                            $('<option>', { value: item.id, text: item.value })
                        );
                    });
                });
            }
        });
    });
})(django.jQuery);
