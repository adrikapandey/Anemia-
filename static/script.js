document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileElem = document.getElementById('fileElem');
    
    // States
    const uploadState = dropArea;
    const loadingState = document.getElementById('loading-state');
    const resultState = document.getElementById('result-state');

    // Result Nodes
    const diagnosisText = document.getElementById('diagnosis-text');
    const confidenceFill = document.getElementById('confidence-fill');
    const probabilityText = document.getElementById('probability-text');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight-drag'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight-drag'), false);
    });

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);
    
    // Handle selected files from dialog
    fileElem.addEventListener('change', (e) => {
        if(e.target.files.length) {
            handleFiles(e.target.files);
        }
    });

    function preventDefaults (e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        const file = files[0];
        // Ensure it's an image
        if (!file.type.match('image.*')) {
            alert('Please upload an image file (PNG, JPG, JPEG).');
            return;
        }

        // Switch to Loading View
        uploadState.classList.add('hidden');
        loadingState.classList.remove('hidden');

        uploadImageForPrediction(file);
    }

    function uploadImageForPrediction(file) {
        const url = '/predict';
        const formData = new FormData();
        formData.append('file', file);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if(data.error) {
                alert("Error from Server: " + data.error);
                resetApp();
                return;
            }
            displayResult(data.prediction, data.probability, data.cached);
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Connection error! Make sure the Python server is running.");
            resetApp();
        });
    }

    function displayResult(prediction, probabilityRaw, isCached) {
        // Hide loading, show result
        loadingState.classList.add('hidden');
        resultState.classList.remove('hidden');

        // Reset previous color classes
        diagnosisText.classList.remove('text-anemic', 'text-non-anemic');

        let cacheBadge = isCached ? " ⚡️ (Cache Hit)" : "";

        if (prediction === 'Anemic') {
            diagnosisText.textContent = 'Anemic' + cacheBadge;
            diagnosisText.classList.add('text-anemic');
            confidenceFill.style.background = 'var(--accent-red)';
        } else {
            diagnosisText.textContent = 'Non-Anemic' + cacheBadge;
            diagnosisText.classList.add('text-non-anemic');
            confidenceFill.style.background = '#06d6a0'; // Success green
        }

        probabilityText.textContent = `${probabilityRaw}%`;

        // Animate the confidence bar smoothly
        setTimeout(() => {
            confidenceFill.style.width = `${probabilityRaw}%`;
        }, 100);
    }

    // Global function to reset the UI from backend/button
    window.resetApp = function() {
        resultState.classList.add('hidden');
        loadingState.classList.add('hidden');
        uploadState.classList.remove('hidden');
        
        // Reset inputs and styles
        fileElem.value = "";
        confidenceFill.style.width = '0%';
    }
});
