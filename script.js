// Global state object to store user selections
const appState = {
    uploadedImages: [], // Array to store multiple images
    selectedType: null,
    selectedColor: null
};

// DOM Elements
const imageUpload = document.getElementById('imageUpload');
const uploadZone = document.getElementById('uploadZone');
const imageGallery = document.getElementById('imageGallery');
const galleryGrid = document.getElementById('galleryGrid');
const imageCount = document.getElementById('imageCount');
const clearAllBtn = document.getElementById('clearAllBtn');
const step2Button = document.getElementById('step2Button');
const step3Button = document.getElementById('step3Button');
const polaroidTypes = document.querySelectorAll('input[name="polaroidType"]');
const lightThemeBtn = document.getElementById('lightTheme');
const darkThemeBtn = document.getElementById('darkTheme');
const confirmationSection = document.getElementById('confirmationSection');
const finalImagePreview = document.getElementById('finalImagePreview');
const previewCount = document.getElementById('previewCount');
const totalImages = document.getElementById('totalImages');
const selectedTypeSpan = document.getElementById('selectedType');
const selectedColorSpan = document.getElementById('selectedColor');
const submitBtn = document.getElementById('submitBtn');
const resultsSection = document.getElementById('resultsSection');
const resultsContainer = document.getElementById('resultsContainer');

// Bootstrap collapse instances
const collapseOne = new bootstrap.Collapse(document.getElementById('collapseOne'), { toggle: false });
const collapseTwo = new bootstrap.Collapse(document.getElementById('collapseTwo'), { toggle: false });
const collapseThree = new bootstrap.Collapse(document.getElementById('collapseThree'), { toggle: false });

// Image Upload Handler
imageUpload.addEventListener('change', handleImageUpload);

// Drag and drop functionality
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = '#d4af37';
    uploadZone.style.transform = 'scale(1.02)';
});

uploadZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = '#d4a59a';
    uploadZone.style.transform = 'scale(1)';
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = '#d4a59a';
    uploadZone.style.transform = 'scale(1)';

    const files = e.dataTransfer.files;
    handleMultipleFiles(files);
});

function handleImageUpload(e) {
    const files = e.target.files;
    handleMultipleFiles(files);
}

function handleMultipleFiles(files) {
    appState.uploadedImages= [];
    galleryGrid.innerHTML = '';
    const validFiles = Array.from(files).filter(file => file.type.startsWith('image/'));

    if (validFiles.length === 0) {
        alert('Please select valid image files');
        return;
    }

    validFiles.forEach(file => {
        const reader = new FileReader();

        reader.onload = function(event) {
            const imageData = {
                id: Date.now() + Math.random(), // Unique ID
                src: event.target.result,
                name: file.name
            };

            appState.uploadedImages.push(imageData);
            addImageToGallery(imageData);
            updateImageCount();

            // Enable Step 2 if images exist
            if (appState.uploadedImages.length > 0) {
                step2Button.removeAttribute('disabled');
            }
        };

        reader.readAsDataURL(file);

    });

    // Show gallery
    imageGallery.classList.remove('d-none');
}

function addImageToGallery(imageData) {
    const galleryItem = document.createElement('div');
    galleryItem.className = 'gallery-item';
    galleryItem.dataset.id = imageData.id;

    galleryItem.innerHTML = `
        <img src="${imageData.src}" alt="${imageData.name}">
    `;

    galleryGrid.appendChild(galleryItem);

    // Animate entrance
    setTimeout(() => {
        galleryItem.style.animation = 'fadeIn 0.5s ease-out';
    }, 10);
}

function updateImageCount() {
    const count = appState.uploadedImages.length;
    imageCount.textContent = `${count} image${count !== 1 ? 's' : ''}`;
}

// Clear all images
clearAllBtn.addEventListener('click', function() {
    if (confirm(`Are you sure you want to remove all ${appState.uploadedImages.length} images?`)) {
        appState.uploadedImages = [];
        galleryGrid.innerHTML = '';
        imageGallery.classList.add('d-none');
        updateImageCount();
        step2Button.setAttribute('disabled', 'true');
        confirmationSection.classList.add('d-none');
    }
});

// Polaroid Type Selection
polaroidTypes.forEach(radio => {
    radio.addEventListener('change', function() {
        appState.selectedType = this.value;

        // Add visual feedback
        document.querySelectorAll('.polaroid-option').forEach(option => {
            option.style.transform = 'translateY(0)';
        });

        const selectedLabel = this.nextElementSibling;
        selectedLabel.style.transform = 'translateY(-8px)';

        // Enable and open Step 3
        step3Button.removeAttribute('disabled');

        setTimeout(() => {
            collapseThree.show();
        }, 500);
    });
});

// Color Theme Selection
lightThemeBtn.addEventListener('click', function() {
    selectColorTheme('Light', this);
});

darkThemeBtn.addEventListener('click', function() {
    selectColorTheme('Dark', this);
});

function selectColorTheme(theme, button) {
    appState.selectedColor = theme;

    // Remove active class from both buttons
    lightThemeBtn.classList.remove('active');
    darkThemeBtn.classList.remove('active');

    // Add active class to selected button
    button.classList.add('active');

    // Show confirmation section
    updateConfirmationSection();

    setTimeout(() => {
        confirmationSection.classList.remove('d-none');
        confirmationSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 300);
}

function updateConfirmationSection() {
    // Clear previous previews
    finalImagePreview.innerHTML = '';

    // Add all images to preview
    appState.uploadedImages.forEach(imageData => {
        const img = document.createElement('img');
        img.src = imageData.src;
        img.alt = imageData.name;
        img.className = 'preview-thumb';
        finalImagePreview.appendChild(img);
    });

    // Update counts and selections
    const count = appState.uploadedImages.length;
    previewCount.textContent = count;
    totalImages.textContent = count;
    const typeSpan = document.getElementById(appState.selectedType)
    selectedTypeSpan.textContent = capitalizeFirstLetter(typeSpan.textContent);
    selectedColorSpan.textContent = appState.selectedColor;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


// Add hover effects to accordion items
document.querySelectorAll('.accordion-item').forEach(item => {
    item.addEventListener('mouseenter', function() {
        if (!this.querySelector('.accordion-button').classList.contains('collapsed')) {
            this.style.transform = 'translateY(-5px)';
        }
    });

    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Smooth scroll for better UX
document.querySelectorAll('.accordion-button').forEach(button => {
    button.addEventListener('click', function() {
        setTimeout(() => {
            this.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 350);
    });
});

// Add sparkle effect on color theme buttons
function createSparkle(x, y) {
    const sparkle = document.createElement('div');
    sparkle.style.position = 'fixed';
    sparkle.style.left = x + 'px';
    sparkle.style.top = y + 'px';
    sparkle.style.width = '10px';
    sparkle.style.height = '10px';
    sparkle.style.background = 'radial-gradient(circle, #d4af37, transparent)';
    sparkle.style.borderRadius = '50%';
    sparkle.style.pointerEvents = 'none';
    sparkle.style.animation = 'sparkleAnimation 1s ease-out forwards';
    sparkle.style.zIndex = '9999';

    document.body.appendChild(sparkle);

    setTimeout(() => {
        sparkle.remove();
    }, 1000);
}

// Add sparkle animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkleAnimation {
        0% {
            transform: scale(0) translateY(0);
            opacity: 1;
        }
        100% {
            transform: scale(2) translateY(-50px);
            opacity: 0;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.8);
        }
    }
`;
document.head.appendChild(style);

// Add sparkle effect on button clicks
[lightThemeBtn, darkThemeBtn].forEach(btn => {
    btn.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;

        for (let i = 0; i < 8; i++) {
            setTimeout(() => {
                const offsetX = (Math.random() - 0.5) * 100;
                const offsetY = (Math.random() - 0.5) * 100;
                createSparkle(x + offsetX, y + offsetY);
            }, i * 50);
        }
    });
});

// Initialize tooltips if needed
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

console.log('Polaroid Creator initialized successfully!');