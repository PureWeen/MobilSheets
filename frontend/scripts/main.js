let currentStream = null;
let useFrontCamera = true;

function isMobile() {
  return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

useFrontCamera = !isMobile();

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

  if (file.type === 'application/pdf') {
    // no extra animation needed, fold is already done above
  } else {
    // For images, the mail slot glow is handled in animation end callback
  }
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

  // Here you can handle canvas.toDataURL() for upload if needed
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
