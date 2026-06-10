import { getArticle, deleteArticle } from '../api/index.js';
import { getUser } from '../auth/index.js';
import { initNavbar } from '../navbar/index.js';
import { formatDate, formatNumber } from '../utils/index.js';

initNavbar();

const params    = new URLSearchParams(location.search);
const articleId = params.get('id');
const base_url = 'http://localhost:8000/articles/'

//  Bootstrap 
async function init() {
  if (!articleId) { showError(); return; }

  try {
    const res     = await getArticle(articleId);
    // Backend retourne { success: true, data: { ...article } }
    const article = res.data || res.article || res;

    renderArticle(article);
    buildToc();
    handleAdminActions(article);
    await loadComments(articleId);

  } catch (_) {
    showError();
  }
}

//  Render article 
export function renderArticle(a) {
  document.title = `${a.title} — DevArch`;

  document.getElementById('articleSkeleton').style.display = 'none';
  document.getElementById('articleContent').style.display  = 'flex';

  const category = a.category_name || a.category?.name || 'General';
  document.getElementById('articleBreadCat').textContent = category;
  document.getElementById('articleBadge').textContent    = category;
  document.getElementById('articleTitle').textContent    = a.title;

  // Avatar auteur
  const av = document.getElementById('articleAuthorAvatar');
  av.textContent = (a.author_name || 'U')[0].toUpperCase();

  document.getElementById('articleAuthorName').textContent = a.author_name || 'Unknown';
  document.getElementById('articleDate').textContent       = formatDate(a.created_at);

  document.getElementById('articleStats').innerHTML = `
    <span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>
      ${formatNumber(a.views || 0)}
    </span>
  `;

  document.getElementById('articleActions').innerHTML = `
    <button class="btn btn--outline-accent btn--sm">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
      </svg>
      Save to pocket
    </button>
    <button class="btn btn--ghost btn--sm">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
      </svg>
      Share
    </button>
  `;

  // Cover image
  const coverImg = document.getElementById('articleCoverImg');
  if (a.image_url) {
    coverImg.src = a.image_url;
    coverImg.alt = a.title;
  } else {
    coverImg.closest('figure').style.display = 'none';
  }

  // Corps de l'article
  document.getElementById('articleBody').innerHTML = a.content || '';

  // Author card
  document.getElementById('authorCardName').textContent = a.author_name || 'Unknown';
  const acAv = document.getElementById('authorCardAvatar');
  acAv.textContent = (a.author_name || 'U')[0].toUpperCase();
}

//  Table of contents ─
export function buildToc() {
  const toc      = document.getElementById('articleToc');
  const headings = document.querySelectorAll('.prose h2, .prose h3');

  if (headings.length === 0) {
    const label = document.querySelector('.article-aside__label');
    if (label) label.style.display = 'none';
    return;
  }

  headings.forEach((h, i) => {
    h.id = h.id || `heading-${i}`;
    const a = document.createElement('a');
    a.href        = `#${h.id}`;
    a.textContent = h.textContent;
    a.className   = 'article-toc__link';
    if (h.tagName === 'H3') a.style.paddingLeft = '22px';
    toc.appendChild(a);
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const link = toc.querySelector(`a[href="#${e.target.id}"]`);
      if (link) link.classList.toggle('active', e.isIntersecting);
    });
  }, { rootMargin: '-10% 0px -80% 0px' });

  headings.forEach(h => observer.observe(h));
}

//  Comments ─
async function loadComments(id) {
  try {
    const res      = await fetch(`${id}/comments`);
    const json     = await res.json();
    const comments = json.data || [];
    renderComments(comments, id);
  } catch (err) {
    console.error('[article] loadComments error:', err);
  }
}

function renderComments(comments, articleId) {
  // Injecte la section commentaires après l'author card
  const authorCard = document.getElementById('authorCard');
  if (!authorCard) return;

  const section = document.createElement('section');
  section.className = 'comments-section';
  section.innerHTML = `
    <h2 class="comments-section__title">
      Comments <span class="comments-section__count">${comments.length}</span>
    </h2>
    <div class="comments-list" id="commentsList"></div>
    ${buildCommentForm(articleId)}
  `;

  authorCard.insertAdjacentElement('afterend', section);

  const list = section.querySelector('#commentsList');

  if (comments.length === 0) {
    list.innerHTML = '<p class="comments-empty">Be the first to comment.</p>';
  } else {
    comments.forEach(c => {
      const item = document.createElement('div');
      item.className = 'comment-item';
      item.innerHTML = `
        <div class="comment-item__avatar">${(c.author_name || 'U')[0].toUpperCase()}</div>
        <div class="comment-item__body">
          <div class="comment-item__header">
            <strong class="comment-item__author">${c.author_name || 'Unknown'}</strong>
            <span class="comment-item__date">${formatDate(c.created_at)}</span>
          </div>
          <p class="comment-item__text">${escapeHtml(c.text)}</p>
        </div>
      `;
      list.appendChild(item);
    });
  }

  // Soumettre un commentaire
  const user = getUser();
  const form = section.querySelector('#commentForm');
  if (!form) return;

  if (!user) {
    form.innerHTML = `<p class="comments-login">
      <a href="../login/login.html">Sign in</a> to leave a comment.
    </p>`;
    return;
  }

  form.querySelector('#submitComment').addEventListener('click', async () => {
    const textarea = form.querySelector('#commentText');
    const text     = textarea.value.trim();
    if (!text) return;

    try {
      const token = localStorage.getItem('da_token');
      const res   = await fetch(`${base_url}/${articleId}/comments`, {
        method:  'POST',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text })
      });

      if (!res.ok) throw new Error('Failed');

      // Recharge les commentaires
      textarea.value = '';
      const refreshed = await fetch(`${base_url}/${articleId}/comments`);
      const data      = await refreshed.json();
      section.remove();
      renderComments(data.data || [], articleId);

    } catch (err) {
      alert('Could not post comment. Please try again.');
    }
  });
}

function buildCommentForm(articleId) {
  return `
    <div class="comment-form" id="commentForm">
      <textarea
        id="commentText"
        class="comment-form__textarea"
        placeholder="Share your thoughts…"
        rows="3"
      ></textarea>
      <button class="btn btn--primary btn--sm" id="submitComment" type="button">
        Post comment
      </button>
    </div>
  `;
}

//  Admin actions ─
export function handleAdminActions(article) {
  const user = getUser();
  if (!user) return;

  const isOwner = String(user.id) === String(article.author_id);
  const isAdmin = user.role === 'admin';
  if (!isOwner && !isAdmin) return;

  const aside = document.getElementById('articleAsideAdmin');
  aside.style.display       = 'flex';
  aside.style.flexDirection = 'column';
  aside.style.gap           = '8px';

  document.getElementById('editArticleBtn').href = `../editor/editor.html?id=${article.id}`;

  document.getElementById('deleteArticleBtn').addEventListener('click', async () => {
    if (!confirm('Delete this article?')) return;
    try {
      await deleteArticle(article.id);
      location.href = '../home/home.html';
    } catch (_) {
      alert('Failed to delete article.');
    }
  });
}

//  Error state 
export function showError() {
  document.getElementById('articleSkeleton').style.display = 'none';
  document.getElementById('articleError').style.display    = 'flex';
}

//  Helpers 
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

init();