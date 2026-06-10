import { getArticles } from '../api/index.js';
import { getUser } from '../auth/index.js';

import { initNavbar } from '../navbar/index.js';

import {
  formatDate,
  formatNumber
} from '../utils/index.js';


initNavbar();


//  DOM

const categoryList    = document.getElementById('categoryList');

const featuredSection = document.getElementById('featuredSection');

const skeletonGrid    = document.getElementById('skeletonGrid');

const articlesGrid    = document.getElementById('articlesGrid');

const emptyState      = document.getElementById('emptyState');

const relatedList     = document.getElementById('relatedList');

const articlesTitle   = document.getElementById('articlesTitle');

const loadMoreBtn     = document.getElementById('articlesLoadMore');



 //  State
let currentCategory = 'all';

let currentPage = 1;

const PAGE_SIZE = 20;


 //  Bootstrap

async function init() {

  await loadArticles(true);

  updateSidebarUser();

  bindEvents();
}


 //  Load articles
async function loadArticles(reset = false) {

  if (reset) {

    articlesGrid.innerHTML = '';

    currentPage = 1;
  }

  showSkeleton(reset);

  try {

    const params = {
      page: currentPage,
      limit: PAGE_SIZE
    };

    if (currentCategory !== 'all') {
      params.category = currentCategory;
    }

    const data = await getArticles(params);

    const articles =
      data.articles ||
      data.data ||
      (Array.isArray(data) ? data : []);

    hideSkeleton();

    if (reset && articles.length === 0) {

      emptyState.style.display = 'flex';

      featuredSection.style.display = 'none';

      loadMoreBtn.style.display = 'none';

      return;
    }

    emptyState.style.display = 'none';

    articlesGrid.style.display = 'grid';

    if (reset && articles.length > 0) {

      renderFeatured(articles[0]);

      articles
        .slice(1)
        .forEach(article => appendCard(article));

    } else {

      articles.forEach(article => appendCard(article));
    }

    loadMoreBtn.style.display =
      articles.length < PAGE_SIZE
        ? 'none'
        : '';

    currentPage++;

    if (reset) {
      renderRelated(articles.slice(0, 3));
    }

  } catch (error) {

    hideSkeleton();

    console.error(
      '[home] loadArticles error:',
      error
    );
  }
}


 //  Render featured article
function renderFeatured(article) {

  const {
    id,
    title,
    content,
    author_name,
    views = 0,
    created_at,
  } = article;

  document.getElementById('featuredCategory')
    .textContent = 'General';

  document.getElementById('featuredLink')
    .href = `../../pages/article/article.html?id=${id}`;

  document.getElementById('featuredTitleLink')
    .href = `../../pages/article/article.html?id=${id}`;

  document.getElementById('featuredTitle')
    .textContent = title;

  document.getElementById('featuredExcerpt')
    .textContent =
      stripHtml(content).slice(0, 250) + '…';

  document.getElementById('featuredMeta')
    .innerHTML = `
      <span>
        <svg width="12" height="12" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="2">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        ${formatNumber(views)}
      </span>

      <span>
        by <strong>${author_name || 'Unknown'}</strong>
      </span>

      <span>
        ${formatDate(created_at)}
      </span>
    `;

  const featuredImg =
    document.getElementById('featuredImg');

  if (featuredImg) {

    featuredImg.src = '/assets/placeholder.jpg';

    featuredImg.alt = title;
  }

  featuredSection.style.display = 'flex';
}


 //  Append article card
function appendCard(article) {

  const template =
    document.getElementById('blog-card-template');

  if (!template) {
    return;
  }

  const card = template.content.cloneNode(true);

  const element =
    card.querySelector('.blog-card');

  element.querySelector('.blog-card__img-wrap')
    .href = `../../pages/article/article.html?id=${article.id}`;

  element.querySelector('.blog-card__img')
    .src = '../../assets/placeholder.jpg';

  element.querySelector('.blog-card__img')
    .alt = article.title;

  element.querySelector('.blog-card__category')
    .textContent = 'General';

  element.querySelector('.blog-card__views-count')
    .textContent = formatNumber(article.views || 0);

  element.querySelector('.blog-card__title')
    .textContent = article.title;

  element.querySelector('.blog-card__author-name')
    .textContent =
      article.author_name || 'Unknown';

  element.querySelector('.blog-card__excerpt')
    .textContent =
      stripHtml(article.content || '')
        .slice(0, 100) + '…';

  articlesGrid.appendChild(card);
}


//  Render related articles
function renderRelated(articles) {

  relatedList.innerHTML = '';

  const template =
    document.getElementById('related-card-template');

  if (!template) {
    return;
  }

  articles.forEach(article => {

    const card = template.content.cloneNode(true);

    const element =
      card.querySelector('.related-card');

    element.querySelector('.related-card__img-wrap')
      .href = `/pages/article/article.html?id=${article.id}`;

    element.querySelector('.related-card__img')
      .src = '../../assets/placeholder.jpg';

    element.querySelector('.related-card__img')
      .alt = article.title;

    element.querySelector('.related-card__badge')
      .textContent = 'General';

    element.querySelector('.related-card__views-count')
      .textContent =
        formatNumber(article.views || 0);

    element.querySelector('.related-card__title')
      .textContent = article.title;

    relatedList.appendChild(card);
  });
}


//  Update sidebar user
function updateSidebarUser() {

  const user = getUser();

  if (!user) {
    return;
  }

  const sidebarUser =
    document.getElementById('sidebarUser');

  if (sidebarUser) {
    sidebarUser.style.display = 'flex';
  }

  const sidebarName =
    document.getElementById('sidebarName');

  if (sidebarName) {
    sidebarName.textContent =
      user.user_firstname || user.email;
  }

  const avatar =
    document.getElementById('sidebarAvatar');

  if (!avatar) {
    return;
  }

  if (user.avatar_url) {

    avatar.style.backgroundImage =
      `url(${user.avatar_url})`;

  } else {

    avatar.textContent =
      (
        user.user_firstname ||
        user.email ||
        'U'
      )[0].toUpperCase();
  }
}


//  Toggle skeleton
function showSkeleton(show) {

  if (skeletonGrid) {

    skeletonGrid.style.display =
      show ? 'grid' : 'none';
  }

  if (show && articlesGrid) {

    articlesGrid.style.display = 'none';
  }
}


function hideSkeleton() {

  if (skeletonGrid) {
    skeletonGrid.style.display = 'none';
  }
}


//  Strip HTML
function stripHtml(html) {

  const container =
    document.createElement('div');

  container.innerHTML = html;

  return container.textContent || '';
}


 
//  Bind events
function bindEvents() {

  if (!loadMoreBtn) {
    return;
  }

  loadMoreBtn.addEventListener('click', () => {
    loadArticles(false);
  });
}


init();