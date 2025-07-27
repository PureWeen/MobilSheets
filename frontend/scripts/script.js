const backendURL = 'http://localhost:5000/upload'; // or your Render/Heroku link

function uploadImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  fetch(backendURL, {
    method: "POST",
    body: formData
  })
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "converted.mid";
    a.click();
  });
  document.getElementById("file-input").addEventListener("change", function () {
  const file = this.files[0];
  if (file) uploadImage(file);
});
}
