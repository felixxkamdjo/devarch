import { getUser, logout } from '../auth/index.js';


export function initNavbar() {

  const mount = document.getElementById('navbar-mount');

  if (!mount) {
    return;
  }

  // Resolve navbar path
  const depth  = location.pathname.split('/').filter(Boolean).length;

  const prefix =
    depth > 1
      ? '../'.repeat(depth - 1)
      : './';

  const navUrl =
    `${prefix}components/navbar/navbar.html`;

  fetch(navUrl)

    .then(response => {

      if (!response.ok) {
        throw new Error('not found');
      }

      return response.text();
    })

    .then(html => {

      mount.innerHTML = html;

      fixNavLinks(prefix);

      setupNavbar();
    })

    .catch(() => {

      mount.innerHTML = `
        <nav class="navbar">
          <div class="navbar__inner">
            <a href="${prefix}pages/home/home.html" class="navbar__logo">
              <span class="navbar__logo-mark">D</span>
              <span class="navbar__logo-text">DevArch</span>
            </a>
          </div>
        </nav>
      `;
    });
}


// Fix navbar links
function fixNavLinks(prefix) {

  document
    .querySelectorAll('.navbar a[href]')
    .forEach(link => {

      const href = link.getAttribute('href');

      if (href.startsWith('../pages/')) {

        link.setAttribute(
          'href',
          href.replace('../pages/', `${prefix}pages/`)
        );

      } else if (href.startsWith('../')) {

        link.setAttribute(
          'href',
          href.replace('../', prefix)
        );
      }
    });
}


// Configure navbar
function setupNavbar() {

  const user = getUser();

  highlightActiveLinks();

  if (user) {
    setupAuthenticatedNavbar(user);
  }

  setupSearch();
  setupMobileMenu();
}


// Highlight active route
function highlightActiveLinks() {

  document
    .querySelectorAll('.navbar__link')
    .forEach(link => {

      try {

        if (
          new URL(link.href).pathname === location.pathname
        ) {
          link.classList.add('active');
        }

      } catch (_) {}
    });
}


// Configure authenticated navbar
function setupAuthenticatedNavbar(user) {

  const navAuth   = document.getElementById('navAuth');
  const navUser   = document.getElementById('navUser');
  const navBell   = document.getElementById('navBell');
  const navEditor = document.getElementById('navEditor');

  if (navAuth) {
    navAuth.style.display = 'none';
  }

  if (navUser) {
    navUser.style.display = 'flex';
  }

  if (navBell) {
    navBell.style.display = 'grid';
  }

  if (navEditor) {
    navEditor.style.display = 'flex';
  }

  const firstname =
    user.user_firstname ||
    user.name ||
    user.email ||
    'U';

  const lastname =
    user.user_lastname || '';

  const avatarInitial =
    document.getElementById('navAvatarInitial');

  const avatarImg =
    document.getElementById('navAvatarImg');

  if (user.avatar_url && avatarImg) {

    avatarImg.src = user.avatar_url;

  } else if (avatarInitial) {

    avatarInitial.textContent =
      firstname[0].toUpperCase();
  }

  const dropName =
    document.getElementById('dropdownName');

  const dropEmail =
    document.getElementById('dropdownEmail');

  if (dropName) {
    dropName.textContent =
      `${firstname} ${lastname}`.trim();
  }

  if (dropEmail) {
    dropEmail.textContent =
      user.email || '';
  }

  setupDropdown();
  setupLogout();
}


// Configure dropdown
function setupDropdown() {

  const avatarBtn =
    document.getElementById('navAvatarBtn');

  const dropdown =
    document.getElementById('navDropdown');

  if (!avatarBtn || !dropdown) {
    return;
  }

  avatarBtn.addEventListener('click', event => {

    event.stopPropagation();

    dropdown.classList.toggle('open');
  });

  document.addEventListener('click', () => {
    dropdown.classList.remove('open');
  });
}


// Configure logout
function setupLogout() {

  const logoutBtn =
    document.getElementById('navLogout');

  if (!logoutBtn) {
    return;
  }

  logoutBtn.addEventListener('click', () => {
    logout();
  });
}


// Configure search
function setupSearch() {

  const searchInput =
    document.getElementById('navSearchInput');

  if (!searchInput) {
    return;
  }

  searchInput.addEventListener('keydown', event => {

    if (event.key !== 'Enter') {
      return;
    }

    const query =
      searchInput.value.trim();

    if (!query) {
      return;
    }

    const depth =
      location.pathname
        .split('/')
        .filter(Boolean)
        .length;

    const prefix =
      depth > 1
        ? '../'.repeat(depth - 1)
        : './';

    location.href =
      `${prefix}pages/home/home.html?q=${encodeURIComponent(query)}`;
  });
}


// Configure mobile menu
function setupMobileMenu() {

  const hamburger =
    document.getElementById('navHamburger');

  const navLinks =
    document.getElementById('navLinks');

  if (!hamburger || !navLinks) {
    return;
  }

  hamburger.addEventListener('click', () => {

    hamburger.classList.toggle('open');

    navLinks.classList.toggle('mobile-open');
  });
}