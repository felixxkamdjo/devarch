import {
  getArticle,
  createArticle,
  updateArticle,
  uploadMedia,
  getCategories
} from '../api/index.js';

import { getUser } from '../auth/index.js';
import { initNavbar } from '../navbar/index.js';


//  Init

initNavbar();

if (!getUser()) {
  location.href = '../login/login.html';
}

const params    = new URLSearchParams(location.search);
const articleId = params.get('id');
const isEdit    = !!articleId;


//  Elements

const editorTitle      = document.getElementById('editorTitle');
const editorContent    = document.getElementById('editorContent');

const categorySelect   = document.getElementById('categorySelect');

const publishBtn       = document.getElementById('publishBtn');
const publishBtnText   = document.getElementById('publishBtnText');

const editorStatus     = document.getElementById('editorStatus');

const wordCount        = document.getElementById('wordCount');
const readTime         = document.getElementById('readTime');
const charCount        = document.getElementById('charCount');

const uploadZone       = document.getElementById('uploadZone');
const uploadInput      = document.getElementById('uploadInput');
const uploadPreview    = document.getElementById('uploadPreview');

const uploadPreviewImg = document.getElementById('uploadPreviewImg');
const uploadRemove     = document.getElementById('uploadRemove');
const uploadTrigger    = document.getElementById('uploadTrigger');

const uploadProgress   = document.getElementById('uploadProgress');
const uploadBar        = document.getElementById('uploadBar');

const toast            = document.getElementById('toast');


//  State

let uploadedImageUrl = null;
let autoSaveTimer    = null;



// Bootstrap
async function init() {
  await loadCategories();

  if (isEdit) {
    await loadArticle();
  }

  bindEvents();
}


//  Categories
async function loadCategories() {

  try {

    const res  = await getCategories();
    const cats = res.data || res.categories || [];

    cats.forEach(cat => {

      const option = document.createElement('option');

      option.value       = cat.id;
      option.textContent = cat.name;

      categorySelect.appendChild(option);
    });

  } catch (_) {
    // Optional
  }
}


//  Article
async function loadArticle() {

  try {

    const res     = await getArticle(articleId);
    const article = res.data || res.article || res;

    editorTitle.textContent = article.title || '';
    editorContent.innerHTML = article.content || '';

    categorySelect.value = article.category_id || '';

    const excerptInput = document.getElementById('excerptInput');

    if (excerptInput) {
      excerptInput.value = article.excerpt || '';
    }

    if (article.image_url) {

      uploadedImageUrl = article.image_url;

      uploadPreviewImg.src = article.image_url;

      document.getElementById('uploadZoneContent').style.display = 'none';

      uploadPreview.style.display = 'block';
    }

    publishBtnText.textContent = 'Update';

    document.title = `Editing: ${article.title} — DevArch`;

    updateStats();

  } catch (_) {

    showToast('Failed to load article.', 'error');
  }
}


//  Events
function bindEvents() {

  bindEditorEvents();
  bindFormatButtons();
  bindUploadEvents();

  publishBtn.addEventListener('click', publishArticle);
}


function bindEditorEvents() {

  editorContent.addEventListener('input', () => {
    updateStats();
    triggerAutoSave();
  });

  editorTitle.addEventListener('input', triggerAutoSave);
}


function bindFormatButtons() {

  document.querySelectorAll('.format-btn').forEach(btn => {

    btn.addEventListener('click', () => {

      const cmd = btn.dataset.cmd;

      editorContent.focus();

      if (cmd === 'h2' || cmd === 'h3') {

        document.execCommand('formatBlock', false, cmd);

      } else if (cmd === 'blockquote') {

        document.execCommand('formatBlock', false, 'blockquote');

      } else if (cmd === 'createLink') {

        const url = prompt('Enter URL:');

        if (url) {
          document.execCommand('createLink', false, url);
        }

      } else {

        document.execCommand(cmd, false, null);
      }
    });
  });
}


function bindUploadEvents() {

  uploadTrigger.addEventListener('click', () => {
    uploadInput.click();
  });

  uploadZone.addEventListener('click', e => {
    if (e.target === uploadZone) {
      uploadInput.click();
    }
  });

  uploadInput.addEventListener('change', () => {
    handleUpload(uploadInput.files[0]);
  });

  uploadZone.addEventListener('dragover', e => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
  });

  uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
  });

  uploadZone.addEventListener('drop', e => {

    e.preventDefault();

    uploadZone.classList.remove('dragover');

    handleUpload(e.dataTransfer.files[0]);
  });

  uploadRemove.addEventListener('click', resetUpload);
}



//  Stats
function updateStats() {

  const text  = editorContent.innerText || '';

  const words = text
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .length;

  const chars = text.length;

  if (wordCount) {
    wordCount.textContent = words.toLocaleString();
  }

  if (charCount) {
    charCount.textContent = chars.toLocaleString();
  }

  if (readTime) {
    readTime.textContent = Math.max(
      1,
      Math.ceil(words / 200)
    );
  }
}


//  Auto Save
function triggerAutoSave() {

  setStatus('Unsaved', '');

  clearTimeout(autoSaveTimer);

  autoSaveTimer = setTimeout(autoSave, 3000);
}


async function autoSave() {

  const title = editorTitle.innerText.trim();

  if (!title || !isEdit) {
    return;
  }

  try {

    setStatus('Saving…', 'saving');

    await updateArticle(articleId, buildPayload());

    setStatus('Saved', 'saved');

  } catch (_) {

    setStatus('Error', 'error');
  }
}


function setStatus(text, modifier = '') {

  editorStatus.textContent = text;

  editorStatus.className =
    `editor-toolbar__status${modifier ? ` ${modifier}` : ''}`;
}


//  Publish
async function publishArticle() {

  const title   = editorTitle.innerText.trim();
  const content = editorContent.innerHTML.trim();

  if (!title) {
    showToast('Please add a title.', 'error');
    return;
  }

  if (!content) {
    showToast('Content cannot be empty.', 'error');
    return;
  }

  publishBtn.disabled = true;

  publishBtnText.textContent =
    isEdit ? 'Updating…' : 'Publishing…';

  try {

    if (isEdit) {

      await updateArticle(articleId, buildPayload());

      showToast('Article updated!', 'success');

      setTimeout(() => {
        location.href = `../article/article.html?id=${articleId}`;
      }, 1200);

    } else {

      const res = await createArticle(buildPayload());

      const id =
        res.id ||
        res.data?.id ||
        res.article?.id;

      showToast('Article published!', 'success');

      setTimeout(() => {

        location.href = id
          ? `../article/article.html?id=${id}`
          : `../home/home.html`;

      }, 1200);
    }

  } catch (err) {

    showToast(
      err.message || 'Failed to publish.',
      'error'
    );

    publishBtn.disabled = false;

    publishBtnText.textContent =
      isEdit ? 'Update' : 'Publish';
  }
}


//  Payload
function buildPayload() {

  const excerptInput =
    document.getElementById('excerptInput');

  return {
    title: editorTitle.innerText.trim(),

    content: editorContent.innerHTML,

    status: 'published',

    category_id: categorySelect.value
      ? parseInt(categorySelect.value)
      : null,

    excerpt: excerptInput
      ? excerptInput.value.trim()
      : '',

    image_url: uploadedImageUrl
  };
}


// Upload
async function handleUpload(file) {

  if (!file) {
    return;
  }

  const MAX = 5 * 1024 * 1024;

  if (file.size > MAX) {

    showToast('File must be under 5 MB.', 'error');

    return;
  }

  uploadProgress.style.display = 'flex';
  uploadBar.style.width        = '20%';

  try {

    previewImage(file);

    uploadBar.style.width = '60%';

    const res = await uploadMedia(file);

    uploadedImageUrl =
      res.url ||
      res.data?.url ||
      res.file?.url ||
      null;

    uploadBar.style.width = '100%';

    setTimeout(() => {

      uploadProgress.style.display = 'none';

      document.getElementById('uploadZoneContent').style.display = 'none';

      uploadPreview.style.display = 'block';

    }, 400);

    showToast('Image uploaded!', 'success');

  } catch (_) {

    showToast('Upload failed.', 'error');

    uploadProgress.style.display = 'none';

    uploadBar.style.width = '0%';
  }
}


function previewImage(file) {

  const reader = new FileReader();

  reader.onload = e => {
    uploadPreviewImg.src = e.target.result;
  };

  reader.readAsDataURL(file);
}


function resetUpload() {

  uploadedImageUrl = null;

  uploadPreview.style.display = 'none';

  document.getElementById('uploadZoneContent').style.display = 'flex';

  uploadInput.value = '';
}


//  Toast
function showToast(message, type = '') {

  toast.textContent = message;

  toast.className = `toast ${type} show`;

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}


init();