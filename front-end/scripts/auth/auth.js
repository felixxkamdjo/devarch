// auth/auth.js

export function saveToken(token) { localStorage.setItem('da_token', token); }
export function getToken()  { return localStorage.getItem('da_token'); }
export function removeToken(){ localStorage.removeItem('da_token'); }

export function saveUser(user)  { localStorage.setItem('da_user', JSON.stringify(user)); }
export function getUser() {
  try { return JSON.parse(localStorage.getItem('da_user')); } catch { return null; }
}
export function removeUser(){ localStorage.removeItem('da_user'); }

export function logout() {
  removeToken(); removeUser();
  location.href = '../../pages/home/home.html';
}

export function isLoggedIn() { return !!getToken() && !!getUser(); }
