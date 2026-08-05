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
// Nav BOOK A STAY opens the booking strip instead of navigating (owner 8-4)
(function(){
  var btn=document.querySelector('.nav-ctas .btn-sn'), panel=document.getElementById('navBookPanel');
  if(!btn||!panel) return;
  btn.addEventListener('click',function(e){ e.preventDefault(); panel.hidden=!panel.hidden; });
  document.addEventListener('click',function(e){ if(!panel.hidden && !panel.contains(e.target) && !btn.contains(e.target)) panel.hidden=true; });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') panel.hidden=true; });
})();
