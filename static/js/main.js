/**
 * Image Similarity Comparison - Frontend Logic
 * Handles image uploads, preview, and result display
 */

// DOM Elements
const image1Input = document.getElementById('image1');
const image2Input = document.getElementById('image2');
const compareForm = document.getElementById('compareForm');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const compareBtn = document.getElementById('compareBtn');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    setupImageUpload(1);
    setupImageUpload(2);
    setupFormSubmission();
});

/**
 * Setup image upload handling for each input
 */
function setupImageUpload(imageNumber) {
    const input = document.getElementById(`image${imageNumber}`);
    const uploadBox = document.getElementById(`uploadBox${imageNumber}`);
    const preview = document.getElementById(`preview${imageNumber}`);
    const previewImg = document.getElementById(`previewImg${imageNumber}`);

    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageSelect(file, uploadBox, preview, previewImg);
        }
    });

    // Drag and drop functionality
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('active');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('active');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('active');

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            input.files = e.dataTransfer.files;
            handleImageSelect(file, uploadBox, preview, previewImg);
        } else {
            showAlert('Please drop a valid image file', 'warning');
        }
    });
}

/**
 * Handle image file selection and preview
 */
function handleImageSelect(file, uploadBox, preview, previewImg) {
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showAlert('File size must be less than 16MB', 'danger');
        return;
    }

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        showAlert('Only JPG, JPEG, and PNG files are allowed', 'danger');
        return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadBox.querySelector('.upload-label').style.display = 'none';
        preview.style.display = 'block';
        uploadBox.classList.add('active');
    };
    reader.readAsDataURL(file);
}

/**
 * Remove selected image
 */
function removeImage(imageNumber) {
    const input = document.getElementById(`image${imageNumber}`);
    const uploadBox = document.getElementById(`uploadBox${imageNumber}`);
    const preview = document.getElementById(`preview${imageNumber}`);
    const previewImg = document.getElementById(`previewImg${imageNumber}`);

    input.value = '';
    previewImg.src = '';
    uploadBox.querySelector('.upload-label').style.display = 'block';
    preview.style.display = 'none';
    uploadBox.classList.remove('active');
}

/**
 * Setup form submission handling
 */
function setupFormSubmission() {
    compareForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Validate both images are selected
        if (!image1Input.files[0] || !image2Input.files[0]) {
            showAlert('Please select both images', 'warning');
            return;
        }

        // Show loading state
        setLoadingState(true);
        hideResults();

        // Prepare form data
        const formData = new FormData();
        formData.append('image1', image1Input.files[0]);
        formData.append('image2', image2Input.files[0]);

        try {
            // Send request to backend
            const response = await fetch('/compare', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                displayResults(data);
            } else {
                showAlert(data.message || 'Error comparing images', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Failed to connect to server. Please try again.', 'danger');
        } finally {
            setLoadingState(false);
        }
    });
}

/**
 * Display comparison results
 */
function displayResults(data) {
    const score = data.similarity_score;
    const level = data.similarity_level;
    const rawScore = data.raw_score;

    // Update score display
    document.getElementById('similarityScore').textContent = score.toFixed(1);
    document.getElementById('rawScore').textContent = rawScore.toFixed(4);

    // Update similarity level badge
    const levelBadge = document.getElementById('similarityLevel');
    levelBadge.textContent = level + ' Similarity';
    levelBadge.className = 'badge fs-5 ' + getSimilarityBadgeClass(score);

    // Update progress bar
    const progressBar = document.getElementById('similarityBar');
    progressBar.style.width = score + '%';
    progressBar.setAttribute('aria-valuenow', score);
    progressBar.innerHTML = `<span class="fw-bold">${score.toFixed(1)}%</span>`;
    progressBar.className = 'progress-bar progress-bar-striped progress-bar-animated ' +
                            getProgressBarClass(score);

    // Update score circle color
    const scoreCircle = document.getElementById('scoreCircle');
    scoreCircle.style.background = getScoreGradient(score);

    // Update description
    document.getElementById('similarityDescription').textContent =
        getSimilarityDescription(score);

    // Show results with animation
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Get badge class based on similarity score
 */
function getSimilarityBadgeClass(score) {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-info';
    if (score >= 40) return 'bg-warning';
    return 'bg-danger';
}

/**
 * Get progress bar class based on similarity score
 */
function getProgressBarClass(score) {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-info';
    if (score >= 40) return 'bg-warning';
    return 'bg-danger';
}

/**
 * Get gradient color for score circle
 */
function getScoreGradient(score) {
    if (score >= 80) {
        return 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
    } else if (score >= 60) {
        return 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
    } else if (score >= 40) {
        return 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
    } else {
        return 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
    }
}

/**
 * Get similarity description text
 */
function getSimilarityDescription(score) {
    if (score >= 80) {
        return 'The images are very similar. They likely show the same object, scene, or concept with minimal differences.';
    } else if (score >= 60) {
        return 'The images show high similarity. They may be related in content, subject matter, or visual composition.';
    } else if (score >= 40) {
        return 'The images have moderate similarity. They share some common features or elements but differ significantly.';
    } else if (score >= 20) {
        return 'The images have low similarity. They are quite different with only minor commonalities.';
    } else {
        return 'The images are very different with minimal or no visual similarities.';
    }
}

/**
 * Set loading state
 */
function setLoadingState(loading) {
    if (loading) {
        compareBtn.disabled = true;
        compareBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        loadingSpinner.style.display = 'block';
    } else {
        compareBtn.disabled = false;
        compareBtn.innerHTML = '<i class="bi bi-arrows-angle-contract"></i> Compare Images';
        loadingSpinner.style.display = 'none';
    }
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.style.display = 'none';
    resultsSection.classList.remove('fade-in');
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    compareForm.insertAdjacentElement('afterend', alertDiv);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
