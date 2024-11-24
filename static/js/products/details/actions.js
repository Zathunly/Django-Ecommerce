let selectedSize = null;
let selectedColor = null;

function selectSize(button) {
    document.querySelectorAll('.size-option').forEach(btn => btn.classList.remove('active'));

    button.classList.add('active');
    selectedSize = button.getAttribute('data-size'); 
}

document.querySelectorAll('.size-option').forEach(button => {
    button.addEventListener('click', function () {
        selectSize(this);
    });
});

function selectColor(button) {
    const colorButtons = document.querySelectorAll('.color-option');
    colorButtons.forEach(btn => btn.classList.remove('active'));

    button.classList.add('active');

    selectedColor = button.getAttribute('data-color');

    const url = new URL(window.location.href);
    url.searchParams.set('color', selectedColor);

    const productImage = document.querySelector('#product-image');
    productImage.style.opacity = '0.5'; 

    fetch(url.href, { method: 'GET' })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newImage = doc.querySelector('#product-image');
            if (newImage) {
                const newImageSrc = newImage.getAttribute('src');
                productImage.setAttribute('src', newImageSrc);
            } else {
                console.warn('No image found for the selected color.');
            }
        })
        .catch(error => {
            console.error('Error fetching image:', error);
            alert('Failed to load the image for the selected color. Please try again.');
        })
        .finally(() => {
            productImage.style.opacity = '1';
        });
}

// Attach event listeners to all color buttons
document.querySelectorAll('.color-option').forEach(button => {
    button.addEventListener('click', function () {
        selectColor(this);
    });
});
