document.addEventListener("DOMContentLoaded", function() {
    const categorySelect = document.getElementById("category");

    const categoryForm = document.getElementById("category-form");

    // Submit the form automatically when a category is selected
    categorySelect.addEventListener("change", function() {
        categoryForm.submit();
    });
    
    const subcategoryContainer = document.getElementById("subcategory-container");
    const filterForm = document.getElementById("filter-form");

    function handleCategoryChange() {
        if (categorySelect.value) {
            subcategoryContainer.style.display = "block";
        } else {
            subcategoryContainer.style.display = "none";
        }
    }

    handleCategoryChange();

    categorySelect.addEventListener("change", handleCategoryChange);

    function submitFilters() {
        filterForm.submit();
    }

    window.submitFilters = submitFilters;
});

