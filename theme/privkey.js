// Injects the PrivKey brand logo into the top of the mdBook sidebar and links
// it back to the docs portal root. The logo lives at the site root
// (/privkey-logo.png), shared across every project. Loaded as additional-js.
(function () {
  function addLogo() {
    var sidebar =
      document.querySelector('#mdbook-sidebar') ||
      document.querySelector('.sidebar');
    if (!sidebar || sidebar.querySelector('.pk-brand')) return;
    var a = document.createElement('a');
    a.className = 'pk-brand';
    a.href = '/';
    a.setAttribute('aria-label', 'PrivKey docs home');
    var img = document.createElement('img');
    // Relative to the page root so it works whether the site is served at a
    // domain root (docs.privkey.io) or a subpath (…github.io/docs/).
    img.src = (window.path_to_root || '') + 'brand-logo.png';
    img.alt = 'PrivKey';
    a.appendChild(img);
    var name = document.createElement('span');
    name.className = 'pk-name';
    name.textContent = 'PrivKey';
    a.appendChild(name);
    sidebar.insertBefore(a, sidebar.firstChild);
  }
  if (document.readyState !== 'loading') addLogo();
  else document.addEventListener('DOMContentLoaded', addLogo);
})();
