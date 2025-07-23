// scripts/main.js

function openCamera() {
  // This would ideally open camera input (for mobile support)
  // For web use, use getUserMedia or navigate to a dedicated camera page
  alert("Camera functionality will be implemented here.");
}

function handleFileUpload(file) {
  if (!file) return;
  if (!validateImage(file)) {
    alert("Invalid file type. Please upload a PNG or JPEG image.");
    return;
  }

  alert("Selected file: " + file.name);
  // TODO: Send this file to backend via fetch + FormData

  const formData = new FormData();
  formData.append("image", file);

  fetch("http://localhost:8000/convert", {
    method: "POST",
    body: formData,
  })
  .then(response => response.blob())
  .then(midiBlob => {
    const url = window.URL.createObjectURL(midiBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "output.mid";
    document.body.appendChild(a);
    a.click();
    a.remove();
  })
  .catch(err => {
    console.error("Conversion failed:", err);
    alert("Error uploading or converting file.");
  });
} 

// Include validator manually for now
typeof validateImage !== 'function' && (window.validateImage = (file) => {
  const validTypes = ['image/jpeg', 'image/png'];
  return file && validTypes.includes(file.type);
});
