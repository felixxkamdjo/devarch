import { login } from '../api/index.js';
import { saveToken, saveUser } from './auth.js';
import { initNavbar } from '../navbar/index.js';


//  DOM Elements
const emailInput    = document.getElementById('email');
const passwordInput = document.getElementById('password');

const loginBtn      = document.getElementById('loginBtn');
const loginBtnText  = document.getElementById('loginBtnText');
const loginSpinner  = document.getElementById('loginSpinner');

const authAlert     = document.getElementById('authAlert');
const togglePw      = document.getElementById('togglePw');


// Initialization
initApp();


function initApp() {
  initNavbar();

  redirectIfAuthenticated();

  bindEvents();
}


//  Event Bindings
function bindEvents() {

  togglePw.addEventListener('click', togglePasswordVisibility);

  loginBtn.addEventListener('click', handleLogin);

  [emailInput, passwordInput].forEach(input => {
    input.addEventListener('keydown', handleEnterKey);
  });
}


function handleEnterKey(event) {
  if (event.key === 'Enter') {
    handleLogin();
  }
}


//  Authentication
function redirectIfAuthenticated() {

  const user = localStorage.getItem('da_user');

  if (user) {
    location.href = '../../home/home.html';
  }
}


async function handleLogin() {

  console.log('Attempting login...');
  const credentials = getFormData();

  if (!isValidForm(credentials)) {
    showAlert('Please fill in all fields.', 'error');
    return;
  }

  setLoading(true);
  hideAlert();

  try {

    const response = await login(credentials);

    const token = extractToken(response);
    const user  = extractUser(response, credentials.email);

    if (!token) {
      throw new Error('No token received.');
    }

    saveToken(token);
    saveUser(user);

    redirectToHome();

  } catch (error) {

    showAlert(
      error.message || 'Invalid email or password.',
      'error'
    );

  } finally {

    setLoading(false);
  }
}


// Helpers

function getFormData() {

  return {
    email: emailInput.value.trim(),
    password: passwordInput.value
  };
}


function isValidForm({ email, password }) {
  return Boolean(email && password);
}


function extractToken(response) {

  return (
    response.data?.token ||
    response.token ||
    response.access_token
  );
}


function extractUser(response, fallbackEmail) {

  return (
    response.data?.user ||
    response.user ||
    { email: fallbackEmail }
  );
}


function redirectToHome() {
  location.href = '../../home/home.html';
}


function togglePasswordVisibility() {

  passwordInput.type =
    passwordInput.type === 'text'
      ? 'password'
      : 'text';
}


//  UI

export function setLoading(isLoading) {

  loginBtn.disabled = isLoading;

  loginBtnText.textContent =
    isLoading
      ? 'Signing in…'
      : 'Sign in';

  loginSpinner.style.display =
    isLoading
      ? 'block'
      : 'none';
}


export function showAlert(message, type) {

  authAlert.textContent   = message;
  authAlert.className     = `auth-alert ${type}`;
  authAlert.style.display = 'block';
}


export function hideAlert() {
  authAlert.style.display = 'none';
}