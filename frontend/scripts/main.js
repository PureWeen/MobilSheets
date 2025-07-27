let currentStream = null;
let useFrontCamera = true;

function isMobile() {
  return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

useFrontCamera = !isMobile();

const backendURL = 'http://localhost:5000/convert-sync';

function uploadImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  // Show loading state
  const mailSlot = document.getElementById('mail-slot');
  const originalText = mailSlot.textContent;
  mailSlot.textContent = 'Processing...';

  fetch(backendURL, {
    method: "POST",
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.blob();
  })
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "converted.mid";
    a.click();
    
    // Reset mail slot
    mailSlot.textContent = originalText;
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to convert image. Please try again.');
    
    // Reset mail slot
    mailSlot.textContent = originalText;
  });
}

async function openCamera() {
  try {
    if (currentStream) stopCamera();

    const constraints = {
      video: { facingMode: useFrontCamera ? 'user' : 'environment' },
      audio: false,
    };

    currentStream = await navigator.mediaDevices.getUserMedia(constraints);

    const video = document.getElementById('camera-preview');
    video.srcObject = currentStream;
    video.style.display = 'block';

    document.getElementById('close-camera').style.display = 'inline-block';
  } catch (err) {
    alert('Could not access camera: ' + err.message);
  }
}

function stopCamera() {
  if (!currentStream) return;

  currentStream.getTracks().forEach(track => track.stop());
  currentStream = null;

  const video = document.getElementById('camera-preview');
  video.style.display = 'none';

  document.getElementById('close-camera').style.display = 'none';
}

function playPaperSound() {
  const sound = document.getElementById('paper-sound');
  if (!sound) return;
  sound.pause();
  sound.currentTime = 0;
  sound.play().catch(() => {});
}

function animateFoldFromButton(buttonEl) {
  const container = document.querySelector('.container');
  const mailSlot = document.getElementById('mail-slot');
  const rect = buttonEl.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();

  const foldEl = document.createElement('div');
  foldEl.classList.add('fold-pdf');

  // Position relative to container for animation start
  foldEl.style.left = `${rect.left - containerRect.left + rect.width / 2 - 40}px`;
  foldEl.style.top = `${rect.top - containerRect.top}px`;

  container.appendChild(foldEl);

  foldEl.addEventListener('animationend', () => {
    foldEl.remove();
    mailSlot.classList.add('glow');
    setTimeout(() => mailSlot.classList.remove('glow'), 2200);
  });
}

function handleFileUpload(file) {
  if (!file) return;
  const validTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  if (!validTypes.includes(file.type)) {
    alert('Please upload a JPEG, PNG image, or a PDF file.');
    return;
  }

  playPaperSound();

  const uploadBtn = document.querySelector('.upload-button');
  animateFoldFromButton(uploadBtn);

  // Upload the file for conversion
  uploadImage(file);
}

function capturePhoto() {
  if (!currentStream) {
    alert('Camera is not active.');
    return;
  }

  const video = document.getElementById('camera-preview');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  stopCamera();

  playPaperSound();

  // Animate from camera button
  const cameraBtn = document.getElementById('camera-btn');
  animateFoldFromButton(cameraBtn);

  // Convert canvas to blob and upload
  canvas.toBlob((blob) => {
    if (blob) {
      // Create a file from the blob
      const file = new File([blob], 'camera-capture.png', { type: 'image/png' });
      uploadImage(file);
    }
  }, 'image/png');
}

document.addEventListener('DOMContentLoaded', () => {
  const cameraBtn = document.getElementById('camera-btn');
  const fileInput = document.getElementById('file-input');
  const closeCameraBtn = document.getElementById('close-camera');

  cameraBtn.addEventListener('click', openCamera);

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      handleFileUpload(fileInput.files[0]);
      fileInput.value = '';
    }
  });

  closeCameraBtn.addEventListener('click', capturePhoto);
});