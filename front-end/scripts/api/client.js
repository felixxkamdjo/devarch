// scripts/api/client.js

// API gateway base URL
const BASE = 'http://localhost:8000';


// Retrieve auth token
function getToken() {
  return localStorage.getItem('da_token');
}


// Send HTTP request
async function request(method, path, body = null, isFormData = false) {

  const headers = {};
  const token   = getToken();

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!isFormData && body) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,

    body: body
      ? (isFormData ? body : JSON.stringify(body))
      : undefined,
  });

  if (!response.ok) {

    let message = `HTTP ${response.status}`;

    try {

      const error = await response.json();

      message =
        error.message ||
        error.error ||
        message;

    } catch (_) {}

    throw new Error(message);
  }

  return response.json();
}


//  Auth API
export const login = body =>
  request('POST', '/auth/login', body);

export const register = body =>
  request('POST', '/auth/register', body);

export const validateToken = () =>
  request('GET', '/auth/validate');

export const getMe = () =>
  request('GET', '/auth/me');

export const updateMe = body =>
  request('PUT', '/auth/me', body);


//  Content API
export const getArticles = (params = {}) => {

  const queryString =
    new URLSearchParams(params).toString();

  return request(
    'GET',
    `/articles${queryString ? '?' + queryString : ''}`
  );
};


export const getArticle = id =>
  request('GET', `/articles/${id}`);

export const createArticle = body =>
  request('POST', '/articles', body);

export const updateArticle = (id, body) =>
  request('PUT', `/articles/${id}`, body);

export const deleteArticle = id =>
  request('DELETE', `/articles/${id}`);

export const getCategories = () =>
  request('GET', '/categories');

export const createCategory = body =>
  request('POST', '/categories', body);


//  Media API
export const uploadMedia = file => {

  const formData = new FormData();

  formData.append('file', file);

  return request(
    'POST',
    '/media/upload',
    formData,
    true
  );
};


export const getMedia = id =>
  request('GET', `/media/files/${id}`);

export const deleteMedia = id =>
  request('DELETE', `/media/files/${id}`);

export const listMedia = () =>
  request('GET', '/media/files');