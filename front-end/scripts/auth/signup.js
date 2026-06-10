import { register } from '../api/index.js';
import { saveToken, saveUser } from './auth.js';
import { initNavbar } from '../navbar/index.js';

initNavbar();

if (localStorage.getItem('da_user')) location.href = '../../pages/home/home.html';

const firstnameInput = document.getElementById('firstname');
const lastnameInput  = document.getElementById('lastname');
const emailInput   = document.getElementById('email');
const passwordInput= document.getElementById('password');

const signupBtn    = document.getElementById('signupBtn');
const signupBtnText= document.getElementById('signupBtnText');
const signupSpinner= document.getElementById('signupSpinner');

const authAlert    = document.getElementById('authAlert');
const togglePw     = document.getElementById('togglePw');

const pwStrength   = document.getElementById('pwStrength');
const pwFill       = document.getElementById('pwFill');
const pwLabel      = document.getElementById('pwLabel');

togglePw.addEventListener('click', () => {
  passwordInput.type = passwordInput.type === 'text' ? 'password' : 'text';
});

passwordInput.addEventListener('input', () => {

  const pw = passwordInput.value;

  if (!pw) { pwStrength.style.display = 'none'; return; }

  pwStrength.style.display = 'flex';
  const score = getPasswordScore(pw);

  const levels = [
    { pct: '25%', color: '#EF4444', label: 'Weak' },
    { pct: '50%', color: '#F59E0B', label: 'Fair' },
    { pct: '75%', color: '#3B82F6', label: 'Good' },
    { pct: '100%',color: '#10B981', label: 'Strong' },
  ];

  const l = levels[Math.min(score, 3)];

  pwFill.style.width      = l.pct;
  pwFill.style.background = l.color;
  pwLabel.textContent     = l.label;
  pwLabel.style.color     = l.color;
});

export function getPasswordScore(pw) {

  let score = 0;

  if (pw.length >= 8)  score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;

  return Math.max(0, score - 1);
}

signupBtn.addEventListener('click', handleSignup);

async function handleSignup() {

  const firstname = firstnameInput.value.trim();
  const lastname  = lastnameInput.value.trim();
  const email     = emailInput.value.trim();
  const password  = passwordInput.value;

  if (!firstname || !lastname || !email || !password) {
    showAlert('All fields are required.', 'error');
    return;
  }

  if (password.length < 8) {
    showAlert('Password must be at least 8 characters.', 'error');
    return;
  }

  setLoading(true);
  hideAlert();

  try {

    const data = await register({
      user_firstname: firstname,
      user_lastname: lastname,
      email,
      password
    });

    console.log('REGISTER RESPONSE:', data);

    const token =
      data.data?.token ||
      data.token ||
      data.access_token;

    if (!token) {
      throw new Error('No token received.');
    }

    const user =
      data.data?.user ||
      data.user ||
      {
        user_firstname: firstname,
        user_lastname: lastname,
        email
      };

    saveToken(token);
    saveUser(user);

    location.href = '../../pages/home/home.html';

  } catch (err) {

    console.error(err);

    showAlert(
      err.message || 'Registration failed.',
      'error'
    );

  } finally {

    setLoading(false);

  }
}
export function setLoading(on) {
  signupBtn.disabled = on;
  signupBtnText.textContent = on ? 'Creating…' : 'Create account';
  signupSpinner.style.display = on ? 'block' : 'none';
}

export function showAlert(msg, type) {
  authAlert.textContent = msg; authAlert.className = `auth-alert ${type}`; authAlert.style.display = 'block';
}

export function hideAlert() { authAlert.style.display = 'none'; }