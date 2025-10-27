document.addEventListener("DOMContentLoaded", function () {
  const passwordInput = document.querySelector('input[name="password"]');
  const registerBtn = document.querySelector('button[type="submit"]');

  const lengthItem = document.getElementById('length');
  const uppercaseItem = document.getElementById('uppercase');
  const lowercaseItem = document.getElementById('lowercase');
  const numberItem = document.getElementById('number');
  const specialItem = document.getElementById('special');

  const checkValidity = () => {
    const value = passwordInput.value;
    const validLength = value.length >= 8;
    const hasUppercase = /[A-Z]/.test(value);
    const hasLowercase = /[a-z]/.test(value);
    const hasNumber = /\d/.test(value);
    const hasSpecial = /[\W_]/.test(value);

    lengthItem.className = validLength ? "text-success" : "text-danger";
    lengthItem.textContent = `${validLength ? "✅" : "❌"} At least 8 characters`;

    uppercaseItem.className = hasUppercase ? "text-success" : "text-danger";
    uppercaseItem.textContent = `${hasUppercase ? "✅" : "❌"} One uppercase letter`;

    lowercaseItem.className = hasLowercase ? "text-success" : "text-danger";
    lowercaseItem.textContent = `${hasLowercase ? "✅" : "❌"} One lowercase letter`;

    numberItem.className = hasNumber ? "text-success" : "text-danger";
    numberItem.textContent = `${hasNumber ? "✅" : "❌"} One number`;

    specialItem.className = hasSpecial ? "text-success" : "text-danger";
    specialItem.textContent = `${hasSpecial ? "✅" : "❌"} One special character`;

    registerBtn.disabled = !(validLength && hasUppercase && hasLowercase && hasNumber && hasSpecial);
  };

  if (passwordInput) {
    passwordInput.addEventListener("input", checkValidity);
    checkValidity(); // Initial state
  }
});
