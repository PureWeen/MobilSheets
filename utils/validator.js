// utils/validator.js

/**
 * Checks if a file is a valid image type (JPEG or PNG)
 * @param {File} file - the uploaded file
 * @returns {boolean} true if valid
 */
function validateImage(file) {
  const validTypes = ['image/jpeg', 'image/png'];
  return file && validTypes.includes(file.type);
}

// Export if using module bundlers (optional)
// export { validateImage };
