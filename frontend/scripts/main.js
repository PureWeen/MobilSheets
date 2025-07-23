let currentStream = null;
let useFrontCamera = true;

// Detect if device is mobile
function isMobile() {
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// Set default camera based on device type
function setDefaultCameraMode() {
  useFrontCamera = !isMobile(); // desktop: front, mobile: back
}

setDefaultCameraMode();

async function openCamera() {
  try {
    if (currentStream) {
      stopCamera();
    }

    const constraints = {
      video: {
        facingMode: useFrontCamera ? "user" : "environment"
      }
    };

    currentStream = await navigator.mediaDevices.getUserMedia(constraints);

    const video = document.getElementById("camera-preview");
    video.srcObject = currentStream;
    video.style.display = "block";

    // Show switch camera button only if multiple cameras are present
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoInputs = devices.filter(d => d.kind === "videoinput");
    document.getElementById("switch-camera").style.display = videoInputs.length > 1 ? "flex" : "none";

  } catch (error) {
    alert("Error accessing camera: " + error.message);
  }
}

function stopCamera() {
  if (!currentStream) return;

  currentStream.getTracks().forEach(track => track.stop());
  currentStream = null;

  const video = document.getElementById("camera-preview");
  video.style.display = "none";

  document.getElementById("switch-camera").style.display = "none";
}

function playPaperSound() {
  const paperSound = document.getElementById("paper-sound");
  if (!paperSound) return;

  paperSound.pause();
  paperSound.currentTime = 0;
  paperSound.play().catch(() => {});
}

function validateFile(file) {
  const validTypes = ["image/jpeg", "image/png", "application/pdf"];
  return file && validTypes.includes(file.type);
}

function handleFileUpload(file) {
  if (!validateFile(file)) {
    alert("Please upload a JPEG, PNG image, or a PDF file.");
    return;
  }

  alert(`File accepted: ${file.name}`);

  playPaperSound();

  if (file.type === "application/pdf") {
    animatePdfFold();
  } else {
    simulateMidiDelivery();
  }
}

function animatePdfFold() {
  const container = document.querySelector(".container");
  const mailSlot = document.getElementById("mail-slot");
  const uploadBtn = document.querySelector(".upload-button");
  const rect = uploadBtn.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();

  const foldEl = document.createElement("div");
  foldEl.classList.add("fold-pdf");

  foldEl.style.left = `${rect.left - containerRect.left + rect.width / 2 - 40}px`;
  foldEl.style.top = `${rect.top - containerRect.top}px`;

  container.appendChild(foldEl);

  foldEl.addEventListener("animationend", () => {
    foldEl.remove();
    mailSlot.classList.add("glow");
    setTimeout(() => mailSlot.classList.remove("glow"), 2200);
  });
}

function simulateMidiDelivery() {
  const mailSlot = document.getElementById("mail-slot");
  mailSlot.classList.add("glow");
  setTimeout(() => mailSlot.classList.remove("glow"), 2200);
}

document.addEventListener("DOMContentLoaded", () => {
  const camToggleBtn = document.getElementById("camera-toggle");
  const switchCamBtn = document.getElementById("switch-camera");

  camToggleBtn.addEventListener("click", () => {
    if (currentStream) {
      stopCamera();
    } else {
      openCamera();
    }
  });

  switchCamBtn.addEventListener("click", () => {
    useFrontCamera = !useFrontCamera;
    openCamera();
  });
});