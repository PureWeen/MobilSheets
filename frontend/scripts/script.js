const backendURL = 'http://localhost:5000/convert-sync'; // Fixed endpoint

function uploadImage(file) {
  const formData = new FormData();
  formData.append("file", file); // Fixed parameter name

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
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to convert image. Please try again.');
  });
}

// Moved event listener outside the function
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("file-input").addEventListener("change", function () {
    const file = this.files[0];
    if (file) uploadImage(file);
  });
});
