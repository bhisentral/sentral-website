(function() {
  const btn = document.getElementById('hamburgerBtn');
  const panel = document.getElementById('mobileMenu');
  if (!btn || !panel) return;
  btn.addEventListener('click', function() {
    const open = panel.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    panel.setAttribute('aria-hidden', !open);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      panel.classList.remove('open');
      btn.setAttribute('aria-expanded','false');
      panel.setAttribute('aria-hidden','true');
      closeModal();
      closeLookup();
    }
  });
})();