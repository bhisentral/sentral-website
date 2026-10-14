#!/usr/bin/env python3
"""
Booking-funnel generator — Phase 2 (6-page booking plan, 2026-09-25).

Generates: book-search.html (P0), book-checkout.html,
book-confirm.html, city-stay.html. Chrome (nav/hamburger/footer markup) is
extracted from property-template.html AT BUILD TIME so the funnel always
matches the site. Shared styles: booking-chrome.css (lifted chrome CSS) +
booking.css (funnel components). ALL rates/availability/taxes are SAMPLE
data from assets/booking-demo.js — production pulls live from StayNTouch
via SentralOS (pages 2 + 6; page 4 Room Detail folded into the search
'Suite details' pop-up 10-13), Shift4 embed unchanged (page 5).

Run from repo root:  python3 scripts/build-booking.py
"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pt=open(os.path.join(ROOT,'property-template.html')).read()
def block(start,end):
    i=pt.index(start); j=pt.index(end,i)+len(end)
    return pt[i:j]
NAV=block('<nav class="site-nav"','\n</nav>')
NAV=NAV.replace('href="#book-stay"','href="/book/search"')  # funnel pages have no on-page booking band  # '\n</nav>' at line start = the outer nav (ham-nav closes indented)
FOOT=block('<footer class="site-footer"','</footer>')
HAM_JS="""<script>
(function(){
  var btn=document.getElementById('hamburgerBtn'),panel=document.getElementById('mobileMenu');
  if(!btn||!panel)return;
  btn.addEventListener('click',function(){
    var open=panel.classList.toggle('open');
    btn.setAttribute('aria-expanded',open);
    panel.setAttribute('aria-hidden',!open);
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&panel.classList.contains('open')){
      panel.classList.remove('open');
      btn.setAttribute('aria-expanded','false');
      panel.setAttribute('aria-hidden','true');
    }
  });
})();
</script>"""
def _newtab(html):
    # ADA: announce links that open a new window (visually hidden)
    return re.sub(r'(<a [^>]*target="_blank".*?)(</a>)',
                  lambda m: m.group(1)+('' if 'sr-only' in m.group(1) else '<span class="sr-only"> (opens in a new tab)</span>')+m.group(2),
                  html, flags=re.S)

def page(title,body):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
      '<meta name="robots" content="noindex">\n'
      '<title>'+title+'</title>\n'
      '<link rel="stylesheet" href="/booking-chrome.css?v=3">\n'
      '<link rel="stylesheet" href="/overrides.css?v=4dark31">\n'
      '<link rel="stylesheet" href="/booking.css?v=18">\n'
      '<script src="/assets/booking-demo.js?v=7" defer></script>\n'
      '</head>\n<body>\n<a class="skip-to-content" href="#main">Skip to content</a>\n<header>\n'
      +NAV+'\n</header>\n<main id="main">\n'+body+'\n</main>\n\n'+FOOT+'\n'+HAM_JS+'\n</body>\n</html>\n')

RIBBON='<div class="bk-demo">Design prototype &mdash; sample rates &amp; availability &middot; live data comes from StayNTouch via SentralOS at build</div>'

def steps(on):
    names=['1 &middot; Suites &amp; Availability','2 &middot; Checkout','3 &middot; Confirmation']
    out=[]
    for i,n in enumerate(names):
        cls='on' if i==on else ('done' if i<on else '')
        out.append('<span class="bkh-step '+cls+'">'+n+'</span>')
    return '<div class="bkh-steps" aria-label="Booking progress">'+''.join(out)+'</div>'

def header(eyebrow,h1,sub_id,step_on=None):
    return ('<section class="bkh dark">\n  <div class="bkh-inner">\n'
      '    <span class="bkh-eyebrow">'+eyebrow+'</span>\n'
      '    <h1>'+h1+'</h1>\n'
      '    <p class="bkh-sub" id="'+sub_id+'"></p>\n'
      +(steps(step_on) if step_on is not None else '')+'\n  </div>\n</section>')

PAGES={}
# ═══ 2. SEARCH AVAILABILITY — Synxis-style cards (Laurie 10-2): rate plans
# inline (no extra click to see offers), strike-through best-rate pricing,
# nightly avg vs stay total, thumbnails, rooms-left. Cards + options are baked
# static from these constants (keep in sync with assets/booking-demo.js).
# Suite photos: (image, TAG). The tag is the only label a guest ever sees —
# caption + alt text — never the file name. PRODUCTION: CMS/StayNTouch media
# per suite with an editable tag field (Living room, Bedroom 1, Kitchen…).
# Images here are placeholders; tags are sample [FIELD]s.
_P=lambda f:'/assets/'+f+'.jpg'
SPHOTOS={
 'studio':[(_P('bk-room-studio'),'Living area'),(_P('bk-city-3'),'Sleeping area'),(_P('bk-city-2'),'Lounge'),
           (_P('bk-room-1br'),'Bedroom'),(_P('bk-city-1'),'Living room'),(_P('bk-room-2br'),'Bedroom detail')],
 'one-bedroom':[(_P('bk-room-1br'),'Living room'),(_P('bk-city-3'),'Bedroom 1'),(_P('bk-room-studio'),'Dining area'),
           (_P('bk-city-2'),'Lounge'),(_P('bk-city-1'),'Living area'),(_P('bk-room-2br'),'Bedroom detail')],
 'two-bedroom':[(_P('bk-room-2br'),'Bedroom 1'),(_P('bk-city-1'),'Living room'),(_P('bk-city-3'),'Bedroom 2'),
           (_P('bk-room-studio'),'Dining area'),(_P('bk-city-2'),'Lounge'),(_P('bk-room-1br'),'Living area')]}
SROOMS=[
 ('studio','Studio','Sleeps 2 · 1 Queen Bed · 1 Bath · 517 Sq Ft',189,4),
 ('one-bedroom','One Bedroom','Sleeps 2 · 1 Queen Bed · 1 Bath · 673 Sq Ft',229,7),
 ('two-bedroom','Two Bedroom','Sleeps 4 · 2 Queen Beds · 2 Baths · 1,053 Sq Ft',319,2)]
SPLANS=[
 ('fall','Limited Time Fall Sale | Stay 2+ Nights &amp; Save up to 20%','Flexible rate. Blackout dates and terms apply.',0.80),
 ('campus','Campus Bound','For campus tours, games &amp; parents&rsquo; weekends. Terms apply.',0.86),
 ('direct','Sentral.com Book Direct Rate | Save up to 10% off Best Rates','Book direct and save.',0.90)]
SOPTS=[('sol-modern','Phoenix — Sol Modern'),('sentral-old-town','Scottsdale — Sentral Old Town'),
 ('sentral-dtla-755','Los Angeles — Sentral DTLA 755 (31+ nights)'),('sentral-dtla-732','Los Angeles — Sentral DTLA 732 (31+ nights)'),
 ('figueroa-eight','Los Angeles — Figueroa Eight (31+ nights)'),('sentral-union-station','Denver — Sentral Union Station'),
 ('alea','Miami — Alea'),('sentral-wynwood','Miami — Sentral Wynwood'),('star-metals','Atlanta — Star Metals West Midtown'),
 ('sentral-michigan-avenue','Chicago — Sentral Michigan Avenue'),('otonomus','Las Vegas — Otonomus'),
 ('inkwell','Charlotte — Inkwell'),('joinery-north','Charlotte — Joinery North'),('joinery-west','Charlotte — Joinery West'),
 ('the-battery','Philadelphia — The Battery (30+ nights)'),('sentral-sobro','Nashville — Sentral SoBro'),
 ('sentral-east-austin-1630','Austin — Sentral East Austin 1630 (30+ nights)'),('sentral-east-austin-1614','Austin — Sentral East Austin 1614'),
 ('forme','Houston — Forme'),('sentral-first-hill','Seattle — Sentral First Hill (30+ nights)')]
def _money(n): return '$'+format(round(n),',')
def _specspans(spec): return ' &middot; '.join('<span>'+x+'</span>' for x in spec.split(' · '))
_SOPTS_HTML=''.join('<option value="'+a+'">'+b+'</option>' for a,b in SOPTS)
def _card(slug,name,spec,base,left):
    ph=SPHOTOS[slug]
    # Laurie 10-8: no rail — each card carries its own avg/night, stay total
    # (excl. taxes, incl. select fees) and BOOK, so one radio + one click books.
    # Rate notes collapse behind "Rate details"; avg rate pushed to the right edge.
    plans=''
    for i,(ps,pn,pnote,mult) in enumerate(SPLANS):
        price=round(base*mult)
        nid='rn-'+slug+'-'+ps
        plans+=('<div class="bk-plan2">'
          '<label class="bk-plan2-pick"><input type="radio" name="pl-'+slug+'" value="'+ps+'"'+(' checked' if i==0 else '')+'>'
          '<span class="bk-plan2-name">'+pn+'</span></label>'
          '<span class="bk-plan2-price"><s>'+_money(base)+'</s> <b>'+_money(price)+'</b><small>sample &middot; avg / night</small></span>'
          '<button type="button" class="bk-plan2-more" aria-expanded="false" aria-controls="'+nid+'">Rate details</button>'
          '<span class="bk-plan2-note" id="'+nid+'" hidden>'+pnote+'</span></div>')
    first=round(base*SPLANS[0][3])
    return ('<div class="bk-card" data-room="'+slug+'" data-base="'+str(base)+'"><div class="bk-room2">'
      '<div class="bk-room2-media bk-gal" data-name="'+name+'">'
      '<div class="bk-gal-stage">'
      '<button type="button" class="bk-gal-open" aria-label="View '+name+' photos full screen">'
      '<img class="bk-room2-img" src="'+ph[0][0]+'" alt="'+name+' &mdash; '+ph[0][1]+'"></button>'
      '<button type="button" class="bk-gal-nav prev" data-gal="-1" aria-label="Previous photo"><span aria-hidden="true">&lsaquo;</span></button>'
      '<button type="button" class="bk-gal-nav next" data-gal="1" aria-label="Next photo"><span aria-hidden="true">&rsaquo;</span></button>'
      '<span class="bk-gal-tag" aria-live="polite">'+ph[0][1]+' &middot; 1 / '+str(len(ph))+'</span></div>'
      '<div class="bk-thumbs" role="list">'+''.join(
        '<button type="button" role="listitem" class="bk-thumb'+(' on' if n==0 else '')+'" data-i="'+str(n)+'" data-src="'+src+'" data-tag="'+tag+'" aria-label="Show '+tag+'">'
        '<img src="'+src+'" alt="" loading="lazy"></button>' for n,(src,tag) in enumerate(ph))+'</div></div>'
      '<div class="bk-room2-mid"><div class="bk-room-name">'+name+'</div>'
      '<div class="bk-specs">'+_specspans(spec)+'</div>'
      '<div class="bk-room-links"><button type="button" class="bk-suite-link" data-suite="'+slug+'" aria-haspopup="dialog">Suite details</button></div>'
      '<div class="bk-plans2">'+plans+'</div></div>'
      '<div class="bk-room2-side"><span class="bk-left">'+str(left)+' rooms left!</span>'
      '<div class="bk-price-n" data-avg>'+_money(first)+'</div><div class="bk-price-l">Sample &middot; avg per night</div>'
      '<div class="bk-total-sm"><span data-tot><b>'+_money(first)+'</b> total &middot; 1 night</span>'
      '<small>Excludes taxes</small>'
      '<small>Includes <button type="button" class="bk-fees-link" data-fees>Select Fees</button></small></div>'
      '<div class="bk-step-ctl"><span class="lbl">Rooms</span>'
      '<button type="button" data-dec="'+slug+'" aria-label="One fewer '+name+'"><span aria-hidden="true">&minus;</span></button>'
      '<span class="n" id="n-'+slug+'" aria-live="polite">1</span>'
      '<button type="button" data-inc="'+slug+'" aria-label="One more '+name+'"><span aria-hidden="true">+</span></button></div>'
      '<a class="bk-btn bk-book-one" data-book="'+slug+'" href="/book/checkout?property=sol-modern&rooms='+slug+':1:'+SPLANS[0][0]+'">Book &nbsp;&rarr;</a>'
      '</div></div></div>')
SEARCH_CARDS=''.join(_card(*r) for r in SROOMS)

CHECK_SVG_INLINE='<svg class="rd-check" viewBox="0 0 24 24" width="34" height="34" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
# Transparent-pricing disclosure (Amy, live engine) — verbatim wording; shared by
# search + checkout. PRODUCTION: per-property fee list comes from property data.
FEES_DIALOG='''<dialog class="bk-fees" id="bkFees" aria-labelledby="bkFeesH">
  <button type="button" class="bk-fees-x" data-fees-close aria-label="Close">&times;</button>
  <h2 id="bkFeesH">Included Fees</h2>
  <p>Your rate may include one or more of the following:</p>
  <ul><li>Resort &amp; Destination Fee(s)</li><li>Cleaning Fee(s)</li><li>Residence Fee(s)</li></ul>
  <h3>Disclaimer</h3>
  <p>The fees listed above are subject to change based on the length of stay. Additional fees may also be assessed during your stay.</p>
</dialog>
<script>
document.addEventListener('click',function(e){
  var d=document.getElementById('bkFees'); if(!d) return;
  if(e.target.closest&&e.target.closest('[data-fees]')){ e.preventDefault(); d.showModal(); }
  else if(e.target.closest&&e.target.closest('[data-fees-close]')||e.target===d){ d.close(); }
});
</script>'''

PAGES['book-search.html']=('Search Availability — Book a Stay — Sentral',
header('Sentral &mdash; Book a Stay','Choose your <em>suite.</em>','bkhContext',0)+'\n'+RIBBON+'''
<div class="bk-wrap">
  <!-- PRODUCTION (P0): live availability + pricing from StayNTouch via
       SentralOS (method TBC w/ Nathan). Multi-room: per-card qty stepper for
       several of one suite; "Add another suite" from checkout returns here
       with the stay carried in ?rooms= and the strip below. -->
  <form class="bk-editbar" id="bkEdit">
    <div class="bk-f bk-f-grow"><label for="bkProp">Property</label>
      <select id="bkProp">'''+_SOPTS_HTML+'''</select></div>
    <div class="bk-f"><label for="bkIn">Check-in</label><input id="bkIn" type="date"></div>
    <div class="bk-f"><label for="bkOut">Check-out</label><input id="bkOut" type="date"></div>
    <div class="bk-f"><label for="bkAd">Adults</label>
      <select id="bkAd"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></div>
    <div class="bk-f"><label for="bkCh">Children</label>
      <select id="bkCh"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option></select></div>
    <div class="bk-f"><label for="bkPromo">Discount code</label><input id="bkPromo" type="text" placeholder="e.g. FALL20"></div>
    <button class="bk-btn slate" type="submit">Update Search &nbsp;&rarr;</button>
  </form>
  <div id="bkCityAlert"></div>
  <div class="bk-staystrip" id="bkStay" hidden></div>
  <div class="bk-results-head">
    <span id="bkCount">3 room types available for your search</span>
    <select id="bkSort" aria-label="Sort results">
      <option value="asc">Sort: Price low &rarr; high</option>
      <option value="desc">Sort: Price high &rarr; low</option>
    </select>
  </div>
  <div id="bkResults">'''+SEARCH_CARDS+'''</div>
</div>
'''+FEES_DIALOG+'''
<!-- Suite details (Laurie 10-13: replaces the Room Detail page). PRODUCTION:
     description text pulls from StayNTouch (room type description) via SentralOS. -->
<dialog class="bk-fees" id="bkSuite" aria-labelledby="bkSuiteH">
  <button type="button" class="bk-fees-x" data-suite-close aria-label="Close">&times;</button>
  <h2 id="bkSuiteH">Suite</h2>
  <div class="bk-specs" id="bkSuiteSpecs"></div>
  <p id="bkSuiteDesc"></p>
  <p class="bk-suite-src">Sample text &mdash; pulls from StayNTouch at build</p>
</dialog>
<!-- 7c MODIFY (reservations portal): search runs in modify mode when ?modify=CONF.
     BOOK opens New Booking review (existing vs new, difference) → payment
     verification → success; written back to StayNTouch, which sends the
     modification email + SMS. Static review links: ?show=review|verifying|modified -->
<dialog class="bk-fees rd-dlg" id="bkMod" aria-labelledby="bkModH">
  <button type="button" class="bk-fees-x" data-mod-close aria-label="Close">&times;</button>
  <div id="bkModBody"></div>
</dialog>
<!-- Full-screen suite gallery (Laurie 10-13): click a photo to open, arrows /
     keys / swipe to step through. Caption = the photo's editable TAG only
     (Living room, Bedroom 1, Kitchen…) — never a file name. -->
<dialog class="bk-light" id="bkLight" aria-labelledby="bkLightTitle">
  <h2 class="sr-only" id="bkLightTitle">Suite photos</h2>
  <button type="button" class="bk-light-x" data-light-close aria-label="Close photos">&times;</button>
  <button type="button" class="bk-light-nav prev" data-light="-1" aria-label="Previous photo"><span aria-hidden="true">&lsaquo;</span></button>
  <figure class="bk-light-fig"><img id="bkLightImg" src="" alt="">
    <figcaption><span class="bk-light-suite" id="bkLightSuite"></span><span id="bkLightTag"></span><span class="bk-light-n" id="bkLightN"></span></figcaption></figure>
  <button type="button" class="bk-light-nav next" data-light="1" aria-label="Next photo"><span aria-hidden="true">&rsaquo;</span></button>
</dialog>
<script>
(function(){
  var lb=document.getElementById('bkLight'), cur=null, idx=0;
  function thumbs(g){ return [].slice.call(g.querySelectorAll('.bk-thumb')); }
  function show(g,i){
    var t=thumbs(g), n=t.length; i=(i+n)%n; g.setAttribute('data-cur',i);
    var th=t[i], img=g.querySelector('.bk-room2-img');
    img.src=th.getAttribute('data-src'); img.alt=g.getAttribute('data-name')+' — '+th.getAttribute('data-tag');
    g.querySelector('.bk-gal-tag').textContent=th.getAttribute('data-tag')+' · '+(i+1)+' / '+n;
    t.forEach(function(x,k){ x.classList.toggle('on',k===i); x.setAttribute('aria-current',k===i?'true':'false'); });
    var strip=th.parentNode; strip.scrollLeft=th.offsetLeft-strip.clientWidth/2+th.clientWidth/2;
    return i;
  }
  function paint(){
    var t=thumbs(cur), th=t[idx];
    var im=document.getElementById('bkLightImg');
    im.src=th.getAttribute('data-src'); im.alt=cur.getAttribute('data-name')+' — '+th.getAttribute('data-tag');
    document.getElementById('bkLightSuite').textContent=cur.getAttribute('data-name');
    document.getElementById('bkLightTag').textContent=th.getAttribute('data-tag');
    document.getElementById('bkLightN').textContent=(idx+1)+' / '+t.length;
  }
  function step(d){ idx=show(cur,idx+d); paint(); }
  document.addEventListener('click',function(e){
    var t=e.target.closest?e.target:null; if(!t) return;
    var g=t.closest('.bk-gal');
    if(g){
      var nav=t.closest('.bk-gal-nav'), th=t.closest('.bk-thumb');
      if(nav){ show(g,(+g.getAttribute('data-cur')||0)+(+nav.getAttribute('data-gal'))); return; }
      if(th){ show(g,+th.getAttribute('data-i')); return; }
      if(t.closest('.bk-gal-open')){ cur=g; idx=+g.getAttribute('data-cur')||0; paint(); lb.showModal(); return; }
    }
    if(t.closest('[data-light]')) step(+t.closest('[data-light]').getAttribute('data-light'));
    else if(t.closest('[data-light-close]')||t===lb) lb.close();
  });
  lb.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'){ e.preventDefault(); step(1); }
    if(e.key==='ArrowLeft'){ e.preventDefault(); step(-1); }
  });
  var x0=null;
  lb.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; },{passive:true});
  lb.addEventListener('touchend',function(e){
    if(x0===null) return; var dx=e.changedTouches[0].clientX-x0; x0=null;
    if(Math.abs(dx)>40) step(dx<0?1:-1);
  });
})();
</script>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), stay=BOOK.parseRooms(q.rooms);   // suites already in the stay (multi-room)
  var props=BOOK.PROPERTIES, propSel=document.getElementById('bkProp'); // options baked static
  var cur=BOOK.prop(q.property)||null;
  var alertBox=document.getElementById('bkCityAlert');
  if(!cur && q.city && BOOK.CITIES[q.city]){
    var c=BOOK.CITIES[q.city];
    alertBox.innerHTML='<div class="bk-alert">'+c.name+' has '+c.props.length+
      ' Sentral properties. <a href="/stay/'+q.city+'?'+BOOK.qs({})+'">Choose your '+c.name+' property &rarr;</a></div>';
    cur=BOOK.prop(c.props[0]);
  }
  if(!cur){
    var cityMatch=q.city && props.filter(function(p){return p.city.toLowerCase().replace(/ /g,'-')===q.city})[0];
    cur=cityMatch||props[0];
  }
  propSel.value=cur.slug;
  if(q['in']) document.getElementById('bkIn').value=q['in'];
  if(q.out) document.getElementById('bkOut').value=q.out;
  if(q.adults) document.getElementById('bkAd').value=q.adults;
  if(q.children) document.getElementById('bkCh').value=q.children;
  if(q.promo) document.getElementById('bkPromo').value=q.promo;
  document.getElementById('bkEdit').addEventListener('submit',function(e){
    e.preventDefault();
    var p=propSel.value;
    location.search='?'+BOOK.qs({property:p,city:null,
      'in':document.getElementById('bkIn').value,out:document.getElementById('bkOut').value,
      adults:document.getElementById('bkAd').value,children:document.getElementById('bkCh').value,
      promo:document.getElementById('bkPromo').value.trim()||null,
      rooms:p===cur.slug?(BOOK.roomsParam(stay)||null):null});
  });
  var nights=BOOK.nights(q['in'],q.out);
  var short=cur.minStay>1&&nights&&nights<cur.minStay;
  document.getElementById('bkhContext').textContent=
    cur.name+', '+cur.city+(nights? ' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night') : ' — choose dates to see availability')
    +(q.promo?' · code '+q.promo.toUpperCase()+' applies at checkout':'');
  if(cur.minStay>1) alertBox.innerHTML+='<div class="bk-alert">'+cur.name+' hosts extended stays only — '+cur.minStay+' nights or more.'+(short?' Adjust your dates above to book.':'')+'</div>';

  var res=document.getElementById('bkResults'), pick={};
  function room(slug){ return cur.rooms.filter(function(r){return r.slug===slug})[0]; }
  function state(slug){
    if(!pick[slug]) pick[slug]={n:(stay[slug]&&stay[slug].n)||1, plan:(stay[slug]&&stay[slug].plan)||'fall'};
    return pick[slug];
  }
  function card(slug){ return res.querySelector('.bk-card[data-room="'+slug+'"]'); }
  function paintCard(slug){
    var r=room(slug), st=state(slug), pl=BOOK.plan(st.plan), c=card(slug);
    if(!r||!c) return;
    var avg=BOOK.planPrice(r,pl), n=nights||1;
    c.querySelector('[data-avg]').textContent=BOOK.money(avg);
    c.querySelector('[data-tot]').innerHTML='<b>'+BOOK.money(avg*n*st.n)+'</b> total · '+n+(n>1?' nights':' night')+(st.n>1?' · '+st.n+' rooms':'');
    c.querySelector('#n-'+slug).textContent=st.n;
    var bk=c.querySelector('.bk-book-one');
    bk.classList.toggle('off',!!short);
    if(short) bk.setAttribute('aria-disabled','true'); else bk.removeAttribute('aria-disabled');
  }
  cur.rooms.forEach(function(r){
    var st=state(r.slug);
    var radio=res.querySelector('input[name="pl-'+r.slug+'"][value="'+st.plan+'"]');
    if(radio) radio.checked=true;
    paintCard(r.slug);
  });
  res.addEventListener('change',function(e){
    if(e.target.type!=='radio') return;
    var slug=e.target.name.replace('pl-','');
    state(slug).plan=e.target.value;
    paintCard(slug);
  });
  res.addEventListener('click',function(e){
    var t=e.target.closest?e.target:null; if(!t) return;
    var sd=t.closest('.bk-suite-link');
    if(sd){
      var rr=room(sd.getAttribute('data-suite')), dlg=document.getElementById('bkSuite');
      document.getElementById('bkSuiteH').textContent=rr.name;
      document.getElementById('bkSuiteSpecs').textContent=rr.specs;
      document.getElementById('bkSuiteDesc').textContent=rr.desc;
      dlg.showModal(); return;
    }
    var more=t.closest('.bk-plan2-more');
    if(more){
      var note=document.getElementById(more.getAttribute('aria-controls')), open=note.hidden;
      note.hidden=!open; more.setAttribute('aria-expanded',open);
      more.textContent=open?'Hide details':'Rate details'; return;
    }
    var incB=t.closest('[data-inc]'), decB=t.closest('[data-dec]'),
        inc=incB&&incB.getAttribute('data-inc'), dec=decB&&decB.getAttribute('data-dec'), k=inc||dec;
    if(k){
      var st=state(k); st.n=Math.max(1,Math.min(9,st.n+(inc?1:-1)));
      paintCard(k); return;
    }
    var bk=t.closest('.bk-book-one');
    if(bk){
      e.preventDefault();
      if(short) return;
      if(q.modify){ modReview(bk.getAttribute('data-book')); return; }
      var slug=bk.getAttribute('data-book'), all={};
      for(var s in stay) all[s]=stay[s];
      all[slug]=state(slug);                          // add / replace this suite in the stay
      location.href='/book/checkout?'+BOOK.qs({property:cur.slug,city:null,rooms:BOOK.roomsParam(all)});
    }
  });
  var sdlg=document.getElementById('bkSuite');
  sdlg.addEventListener('click',function(e){ if(e.target===sdlg||e.target.closest('[data-suite-close]')) sdlg.close(); });
  document.getElementById('bkSort').addEventListener('change',function(){
    var dir=this.value==='desc'?-1:1;
    [].slice.call(res.children)
      .sort(function(a,b){ return dir*((+a.getAttribute('data-base'))-(+b.getAttribute('data-base'))); })
      .forEach(function(c){ res.appendChild(c); });
  });
  // ── 7c Modify mode ──
  var modDlg=document.getElementById('bkMod'), modBody=document.getElementById('bkModBody');
  function backHref(extra){ var o={}; for(var k in extra) o[k]=extra[k];
    o.conf=q.modify; o.modify=null; o.oin=null; o.oout=null; o.orooms=null; o.show=null; return '/reservations/details?'+BOOK.qs(o); }
  function modReview(slug){
    var st=state(slug), r=room(slug), newRooms=slug+':'+st.n+':'+st.plan;
    var base={property:cur.slug,adults:q.adults,children:q.children,promo:q.promo};
    var oldS=BOOK.summary(Object.assign({},base,{'in':q.oin||q['in'],out:q.oout||q.out,rooms:q.orooms||newRooms}));
    var newS=BOOK.summary(Object.assign({},base,{'in':q['in'],out:q.out,rooms:newRooms}));
    var diff=newS.total-oldS.total, ad=+q.adults||1, ch=+q.children||0;
    modBody.innerHTML='<h2 class="rd-dlg-h" id="bkModH">New booking</h2><p class="rd-copy">Please review the booking changes</p>'+
      '<div class="rd-nb"><b>'+cur.name+'</b><span>'+(st.n>1?st.n+' × ':'')+r.name+' · '+BOOK.plan(st.plan).short+'</span>'+
      '<small>'+ad+(ad>1?' adults':' adult')+(ch?', '+ch+(ch>1?' children':' child'):'')+'</small></div>'+
      '<dl class="bk-facts"><div><dt>Check-in</dt><dd>'+BOOK.fmtDate(q['in'])+'<small>4:00 PM</small></dd></div>'+
      '<div><dt>Check-out</dt><dd>'+BOOK.fmtDate(q.out)+'<small>11:00 AM</small></dd></div><div><dt>Nights</dt><dd>'+newS.nights+'</dd></div></dl>'+
      '<h3 class="bk-rail-h" style="margin-top:14px">Price details</h3>'+
      '<div class="bk-line"><span>Existing booking</span><span>'+BOOK.cents(oldS.total)+'</span></div>'+
      '<div class="bk-line"><span>New booking</span><span>'+BOOK.cents(newS.total)+'</span></div>'+
      '<div class="bk-total"><span>Difference</span><span>'+(diff<0?'−':'')+BOOK.cents(Math.abs(diff))+'</span></div>'+
      '<p class="rd-src">You may receive a refund or need to make an additional payment based on the difference in pricing.</p>'+
      '<div class="rd-dlg-btns"><button class="bk-btn" type="button" id="bkModGo">Book</button><button class="bk-btn-g" type="button" data-mod-close>Cancel</button></div>';
    document.getElementById('bkModGo').addEventListener('click',function(){ modVerify(newRooms); });
    if(!modDlg.open) modDlg.showModal();
  }
  function modVerify(newRooms){
    modBody.innerHTML='<div class="rd-spin" aria-hidden="true"></div><p class="rd-msg" id="bkModH" role="status">Verifying your payment details, please wait…</p>';
    if(!modDlg.open) modDlg.showModal();
    if(newRooms!==null) setTimeout(function(){ modDone(newRooms); },1800);
  }
  function modDone(newRooms){
    modBody.innerHTML='''+repr(CHECK_SVG_INLINE)+'''+'<p class="rd-msg" id="bkModH" role="status">Your booking modified successfully!</p>'+
      '<div class="rd-dlg-btns" style="justify-content:center"><a class="bk-btn slate" href="'+backHref({rooms:newRooms||q.orooms})+'">Back to booking details</a></div>';
    if(!modDlg.open) modDlg.showModal();
  }
  modDlg.addEventListener('click',function(e){ if(e.target===modDlg||e.target.closest('[data-mod-close]')) modDlg.close(); });
  if(q.modify){
    var wrap=document.querySelector('.bk-wrap');
    var bar=document.createElement('div'); bar.className='rd-modbar';
    bar.innerHTML='<a class="rd-link" href="'+backHref({rooms:q.orooms,'in':q.oin||q['in'],out:q.oout||q.out})+'">‹ Back to booking details</a>'+
      '<span>Modifying reservation <b>'+q.modify+'</b> — choose new dates or a different suite. You’ll review any price difference before anything changes.'+(q.promo?' <b>Code applied: '+q.promo.toUpperCase()+'</b>':'')+'</span>';
    wrap.insertBefore(bar,wrap.firstChild);
    document.querySelector('.bkh h1').innerHTML='Modify your <em>stay.</em>';
    document.querySelector('.bkh-eyebrow').textContent='Sentral — Manage Reservation';
    var stp=document.querySelector('.bkh-steps'); if(stp) stp.hidden=true;   // no checkout in modify
    document.getElementById('bkhContext').textContent='Reservation '+q.modify+' · '+cur.name+', '+cur.city+(nights?' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out):'');
    if(q.show==='review') modReview(cur.rooms[1].slug);
    if(q.show==='verifying') modVerify(null);
    if(q.show==='modified') modDone(q.orooms);
  }
  // Multi-room strip — only when returning from checkout via "Add another suite"
  var names=[];
  cur.rooms.forEach(function(r){ var s=stay[r.slug]; if(s&&s.n) names.push(s.n+' × '+r.name+' ('+(BOOK.plan(s.plan).short)+')'); });
  if(names.length){
    var strip=document.getElementById('bkStay');
    strip.hidden=false;
    strip.innerHTML='<span><b>In your stay:</b> '+names.join(', ')+'. Book another suite below to add it.</span>'+
      '<a class="bk-btn slate" href="/book/checkout?'+BOOK.qs({property:cur.slug,city:null})+'">Back to Checkout &nbsp;&rarr;</a>';
  }
});
</script>''')

US_STATES=['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
_STATE_OPTS='<option value="">Select</option>'+''.join('<option>'+s+'</option>' for s in US_STATES)
_COUNTRY_OPTS=''.join('<option'+(' selected' if c=='United States' else '')+'>'+c+'</option>' for c in
  ['United States','Canada','Mexico','United Kingdom','Australia','Brazil','China','France','Germany','India','Ireland','Israel','Italy','Japan','Netherlands','South Korea','Spain','Switzerland','Other'])

# ═══ 5. BOOKING DETAILS (CHECKOUT) — native guest form + Shift4 embed ═══
# Laurie 10-8: capture everything the live engine captures today (address,
# country, city, state, zip — Shift4's iframe takes card data ONLY), list the
# booked suite(s) in TEXT (no photo) with rate, dates + times, nights, guests;
# full price breakdown; Deposit + Cancellation policy links under the total.
PAGES['book-checkout.html']=('Checkout — Book a Stay — Sentral',
header('Sentral &mdash; Book a Stay','Almost <em>booked.</em>','ckContext',1)+'''
'''+RIBBON+'''
<div class="bk-wrap">
  <div class="bk-grid">
    <div>
      <div class="bk-card"><div class="bk-pad">
        <h2 class="bk-h2">Guest <em>details</em></h2>
        <!-- Native guest-info form (plan §5) — same fields the live engine
             captures; * = required, matching today. -->
        <form id="ckForm" class="bk-field-grid">
          <div class="bk-f"><label for="ck-fn">First name *</label><input id="ck-fn" autocomplete="given-name" required></div>
          <div class="bk-f"><label for="ck-ln">Last name *</label><input id="ck-ln" autocomplete="family-name" required></div>
          <div class="bk-f"><label for="ck-em">Email *</label><input id="ck-em" type="email" autocomplete="email" required></div>
          <div class="bk-f"><label for="ck-ph">Phone *</label>
            <div class="bk-phone"><select id="ck-cc" aria-label="Country code" autocomplete="tel-country-code"><option value="+1" selected>+1</option><option value="+44">+44</option><option value="+52">+52</option><option value="+61">+61</option><option value="+33">+33</option><option value="+49">+49</option><option value="+81">+81</option><option value="+91">+91</option></select>
            <input id="ck-ph" type="tel" autocomplete="tel-national" required></div></div>
          <div class="bk-f full"><label for="ck-a1">Address</label><input id="ck-a1" autocomplete="address-line1"></div>
          <div class="bk-f"><label for="ck-co">Country / territory *</label><select id="ck-co" autocomplete="country-name" required>'''+_COUNTRY_OPTS+'''</select></div>
          <div class="bk-f"><label for="ck-ci">City</label><input id="ck-ci" autocomplete="address-level2"></div>
          <div class="bk-f"><label for="ck-st">State *</label><select id="ck-st" autocomplete="address-level1" required>'''+_STATE_OPTS+'''</select>
            <input id="ck-st-x" autocomplete="address-level1" aria-label="State / province" hidden></div>
          <div class="bk-f"><label for="ck-zp">Zip code *</label><input id="ck-zp" autocomplete="postal-code" required></div>
          <div class="bk-f full"><label for="ck-rq">Special requests <span style="text-transform:none;letter-spacing:.02em">&mdash; optional</span></label><input id="ck-rq"></div>
        </form>
      </div></div>
      <div class="bk-card"><div class="bk-pad">
        <h2 class="bk-h2">Pay <em>with</em></h2>
        <!-- SHIFT4 — the existing payment capture embeds here UNCHANGED (plan §5).
             It collects card number, expiry, CVV, card zip and cardholder name
             only; guest address stays in the native form above. The prototype
             deliberately renders no card fields: never collect payment data
             outside the Shift4 iframe. -->
        <div class="bk-embed" style="margin-top:0"><strong>Shift4 payment capture</strong>
          <p>The current Shift4 embed drops in here unchanged: card number, expiry, CVV, card zip and cardholder name. Guest address is captured above. No card fields exist in this prototype by design.</p></div>
        <a class="bk-btn wide" id="ckGo" href="/book/confirmation">Book Now &nbsp;&rarr;</a>
        <div class="bk-note">By booking you agree to the <a href="/terms-of-use" target="_blank" rel="noopener" class="bk-inline">Terms &amp; Conditions</a> and <a href="/reservation-policies" target="_blank" rel="noopener" class="bk-inline">Reservation Policies</a>.</div>
      </div></div>
    </div>
    <aside class="bk-rail" aria-label="Booking details">
      <h2 class="bk-rail-h">Booking details</h2>
      <h3 id="railProp"></h3>
      <div class="bk-rail-sub" id="railAddr"></div>
      <div id="railRooms"></div>
      <dl class="bk-facts" id="railFacts"></dl>
      <hr>
      <h2 class="bk-rail-h">Total price details</h2>
      <div id="railLines"></div>
      <hr>
      <div class="bk-total"><span>Total for stay</span><span id="railTotal">&mdash;</span></div>
      <div class="bk-policy-links"><a href="/reservation-policies#payment" target="_blank" rel="noopener">Deposit</a> and <a href="/reservation-policies#cancellation" target="_blank" rel="noopener">Cancellation</a> policy</div>
      <div class="bk-note">Sample rates &amp; tax lines &mdash; property-specific fee and tax items are driven by property data at build</div>
    </aside>
  </div>
</div>
'''+FEES_DIALOG+'''
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), cur=BOOK.prop(q.property)||BOOK.PROPERTIES[0];
  document.getElementById('ckContext').textContent=cur.name+', '+cur.city+' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out);
  var back='/book/search?'+BOOK.qs({}), S=BOOK.summary(q,{modify:back}), sub=S.sub;
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railAddr').textContent=cur.address||(cur.city+', '+cur.state);
  document.getElementById('railRooms').innerHTML=(S.count?S.rooms:'<div class="bk-line"><small>No suites selected — start from Suites &amp; Availability.</small></div>')+
    '<a class="bk-addroom" href="'+back+'">+ Add another suite</a>';
  document.getElementById('railFacts').innerHTML=S.facts;
  document.getElementById('railLines').innerHTML=S.lines;
  document.getElementById('railTotal').textContent=sub?BOOK.cents(S.total):'—';
  // US → state dropdown; elsewhere → free-text region
  var co=document.getElementById('ck-co'), stS=document.getElementById('ck-st'), stX=document.getElementById('ck-st-x');
  co.addEventListener('change',function(){
    var us=co.value==='United States';
    stS.hidden=!us; stS.required=us; stX.hidden=us;
    stS.id=us?'ck-st':'ck-st-s'; stX.id=us?'ck-st-x':'ck-st';
  });
  var go=document.getElementById('ckGo');
  go.classList.toggle('off',!sub);
  go.addEventListener('click',function(e){
    var f=document.getElementById('ckForm');
    if(!f.reportValidity()){ e.preventDefault(); return; }
    var name=(document.getElementById('ck-fn').value+' '+document.getElementById('ck-ln').value).trim();
    go.href='/book/confirmation?'+BOOK.qs({guest:name});
  });
});
</script>''')

# ═══ 6. BOOKING CONFIRMATION — StayNTouch via SentralOS at build ═══
# Laurie 10-13: summary broken out like checkout (property, suites + rate,
# dates/times, guests, itemized price details, total) so the guest can see
# exactly what they booked and paid. Back to Sentral.com = slate button.
PAGES['book-confirm.html']=('Booking Confirmed — Sentral',
header('Sentral &mdash; Book a Stay','You&rsquo;re <em>booked.</em>','cfContext',2)+'''
'''+RIBBON+'''
<div class="bk-wrap">
  <!-- PRODUCTION: confirmation number + stay summary come from StayNTouch via
       SentralOS; completing the booking TRIGGERS the confirmation email and
       SMS from here (plan §6). Nothing is sent from the prototype. -->
  <div class="bk-grid">
    <div>
      <div class="bk-card"><div class="bk-pad">
        <span class="bk-eyebrow">Confirmation number</span>
        <div class="bk-confirm-n" id="cfNum">SENTRAL-DEMO</div>
        <div class="bk-specs" style="margin-bottom:14px">Sample number &mdash; issued by StayNTouch at build</div>
        <p style="font-size:.9375rem;color:#4a4643;max-width:60ch" id="cfMsg"></p>
        <p style="font-size:.8125rem;color:#6B6560;margin-top:10px">A confirmation email and text follow at build (triggered from this step). Need a hand? <strong id="cfPhone"></strong></p>
        <p class="bk-cf-ctas"><a class="bk-btn" href="/stay/sol-modern">See your property &nbsp;&rarr;</a>
        <a class="bk-btn slate bk-btn-flip" href="/">Back to Sentral.com</a></p>
      </div></div>
    </div>
    <aside class="bk-rail" aria-label="Your booking">
      <h2 class="bk-rail-h">Your booking</h2>
      <h3 id="railProp"></h3>
      <div class="bk-rail-sub" id="railAddr"></div>
      <div id="railRooms"></div>
      <dl class="bk-facts" id="railFacts"></dl>
      <hr>
      <h2 class="bk-rail-h">Total price details</h2>
      <div id="railLines"></div>
      <hr>
      <div class="bk-total"><span>Total for stay</span><span id="railTotal">&mdash;</span></div>
      <div class="bk-policy-links"><a href="/reservation-policies#payment" target="_blank" rel="noopener">Deposit</a> and <a href="/reservation-policies#cancellation" target="_blank" rel="noopener">Cancellation</a> policy</div>
      <div class="bk-note">Sample rates &amp; tax lines for design review</div>
    </aside>
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), S=BOOK.summary(q), cur=S.cur;
  document.getElementById('cfNum').textContent='SENT-'+(Date.now().toString(36).toUpperCase().slice(-6));
  document.getElementById('cfContext').textContent=cur.name+', '+cur.city+' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out);
  document.getElementById('cfMsg').textContent=(q.guest?q.guest+', your':'Your')+' suite at '+cur.name+' is set for '+BOOK.fmtDate(q['in'])+'. Check-in opens at 4:00 PM with keyless entry — your code arrives the morning of arrival.';
  document.getElementById('cfPhone').textContent=cur.phone||'(833) 370-4161';
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railAddr').textContent=cur.address||(cur.city+', '+cur.state);
  document.getElementById('railRooms').innerHTML=S.rooms||'<div class="bk-line"><small>Sample stay</small></div>';
  document.getElementById('railFacts').innerHTML=S.facts;
  document.getElementById('railLines').innerHTML=S.lines;
  document.getElementById('railTotal').textContent=S.sub?BOOK.cents(S.total):'—';
});
</script>''')

# ═══ 1a. CITY STAY SELECTOR — multi-property markets ═══
PAGES['city-stay.html']=('Choose Your Property — Book a Stay — Sentral',
header('Sentral &mdash; Book a Stay','<span id="cityH">Choose your <em>Sentral.</em></span>','ctContext')+'''
'''+RIBBON+'''
<div class="bk-wrap">
  <!-- 1a. Multi-property markets only (Austin, Charlotte, LA, Miami). Routes
       the guest to the right property's Search & Availability page, dates
       passed through untouched. -->
  <form class="bk-editbar" id="ctEdit">
    <div class="bk-f"><label for="ctIn">Check-in</label><input id="ctIn" type="date"></div>
    <div class="bk-f"><label for="ctOut">Check-out</label><input id="ctOut" type="date"></div>
    <div class="bk-f"><label for="ctAd">Adults</label>
      <select id="ctAd"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></div>
    <div class="bk-f"><label for="ctCh">Children</label>
      <select id="ctCh"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option></select></div>
    <div class="bk-f"><label for="ctPromo">Discount code <span style="text-transform:none;letter-spacing:.02em">&mdash; optional</span></label><input id="ctPromo" type="text" placeholder="e.g. FALL20" style="width:150px"></div>
    <button class="bk-btn" type="submit">Apply &nbsp;&rarr;</button>
  </form>
  <div class="bk-props" id="ctProps"></div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), c=BOOK.CITIES[q.city];
  if(!c){ location.replace('/book/search?'+BOOK.qs({})); return; }
  var nights=BOOK.nights(q['in'],q.out);
  if(q['in']) document.getElementById('ctIn').value=q['in'];
  if(q.out) document.getElementById('ctOut').value=q.out;
  if(q.promo) document.getElementById('ctPromo').value=q.promo;
  // Rate-line rule (owner 10-14): if a promo code applies but yields no rate
  // for a community, the card still shows the lowest available rate for the
  // requested dates — never a blank price. PRODUCTION: StayNTouch lowest
  // availability per community for q.in→q.out; promo pricing where eligible,
  // lowest-date rate as the fallback.
  if(nights){
    [].forEach.call(document.querySelectorAll('.bk-prop'),function(card){
      var note=card.querySelector('.bk-pb-note'), excl=card.querySelector('.bk-pb-excl');
      if(!note) return;
      var ok=card.getAttribute('data-promo-ok')!=='0';
      note.textContent='For your dates · before taxes';
      if(q.promo){ if(ok){ note.textContent+=' · promo-eligible'; } else if(excl){ excl.hidden=false; } }
    });
  }
  if(q.adults) document.getElementById('ctAd').value=q.adults;
  if(q.children) document.getElementById('ctCh').value=q.children;
  document.getElementById('ctEdit').addEventListener('submit',function(e){
    e.preventDefault();
    location.search='?'+BOOK.qs({city:q.city,
      'in':document.getElementById('ctIn').value, out:document.getElementById('ctOut').value,
      adults:document.getElementById('ctAd').value, children:document.getElementById('ctCh').value,
      promo:document.getElementById('ctPromo').value.trim()||null});
  });
  document.getElementById('cityH').innerHTML=c.name+'. <em>Choose your Sentral.</em>';
  document.getElementById('ctContext').textContent=c.props.length+' properties'+(nights?' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out):'')+(q.promo?' · code '+q.promo.toUpperCase()+' will apply at checkout':'');
  var IMGS=['/assets/bk-city-1.jpg','/assets/bk-city-2.jpg','/assets/bk-city-3.jpg'];
  document.getElementById('ctProps').innerHTML=c.props.map(function(slug,i){
    var p=BOOK.prop(slug);
    return '<a class="bk-prop" href="/book/search?'+BOOK.qs({property:slug,city:null})+'">'+
      '<img class="bk-prop-img" src="'+IMGS[i%3]+'" alt="'+p.name+'">'+
      '<div class="bk-prop-body"><div class="bk-prop-name">'+p.name+'</div>'+
      '<div class="bk-prop-meta">'+p.city+', '+p.state+(p.minStay>1?' · 30+ nights':'')+'</div>'+
      '<span class="bk-prop-cta">Check availability &nbsp;&rarr;</span></div></a>';
  }).join('');
});
</script>''')


# ═══ 7b–7d. RESERVATION PORTAL — Details + Manage (modify/cancel entry) ═══
# Replicates reservations.sentral.com (after Find Reservation) on the v4 brand:
# booking info, guest details (+ Edit Email/Phone), arrival info, Resend
# Confirmation, Modify / Cancel, Payment Summary w/ breakdown. Copy for every
# message is verbatim from the live portal. PRODUCTION: everything reads from
# and writes back to StayNTouch via SentralOS (resend / edit / cancel each
# trigger their own email + SMS). Static review links: ?show=resent | edit |
# updated | cancel | cancelled opens that state on load.
CANCEL_POLICY=('You may cancel your reservation for no charge before 11:59 PM local hotel time 2 day[s] before arrival. '
  'Please note that we will assess a fee of 1 night room and tax if you must cancel after this deadline. '
  'If you have made a prepayment, we will retain all or part of your prepayment. If not, we will charge your credit card.')
CHECK_SVG='<svg class="rd-check" viewBox="0 0 24 24" width="34" height="34" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PAGES['reservation-details.html']=('Reservation Details — Sentral',
header('Sentral &mdash; Manage Reservation','Reservation <em>details.</em>','rdContext')+'\n'+RIBBON+'''
<div class="bk-wrap">
  <div class="rd-top">
    <span class="rd-status" id="rdStatus" hidden>Cancelled</span>
    <p class="rd-help">Need help? 24/7 text assistance <a href="sms:+17373733736">737-373-3736</a></p>
  </div>
  <div class="bk-card"><div class="bk-pad">
    <div class="rd-grid">
      <section aria-labelledby="rdH1">
        <h2 class="bk-rail-h" id="rdH1">Booking information</h2>
        <div class="rd-body"><h3 class="rd-prop" id="rdProp">Sol Modern</h3>
        <div class="rd-addr" id="rdAddr">50 E. Fillmore Street, Phoenix, AZ 85004</div>
        <a class="rd-link" id="rdMap" href="#" target="_blank" rel="noopener">View on map</a>
        <dl class="bk-facts rd-facts">
          <div><dt>Offer code</dt><dd id="rdCode">&mdash;</dd></div>
          <div><dt>Confirmation number</dt><dd id="rdConf">SENT-SAMPLE</dd></div>
        </dl></div>
        <div class="rd-act"><button type="button" class="bk-btn slate rd-btn" data-open="resent">Resend Confirmation</button></div>
        <p class="rd-stay"><span id="rdNights">2 nights</span><b id="rdDates">Sample dates</b></p>
      </section>
      <section aria-labelledby="rdH2">
        <h2 class="bk-rail-h" id="rdH2">Guest details</h2>
        <div class="rd-body"><dl class="bk-facts rd-facts">
          <div><dt>First name</dt><dd id="rdFirst">Sample</dd></div>
          <div><dt>Last name</dt><dd id="rdLast">Guest</dd></div>
          <div class="full"><dt>Email</dt><dd id="rdEmail">guest@example.com</dd></div>
          <div class="full"><dt>Phone</dt><dd id="rdPhone">+1 555 010 0142</dd></div>
        </dl></div>
        <div class="rd-act"><button type="button" class="bk-btn slate rd-btn" data-open="edit">Edit Email/Phone</button></div>
      </section>
      <section aria-labelledby="rdH3">
        <h2 class="bk-rail-h" id="rdH3">Arrival / check-in</h2>
        <div class="rd-body"><p class="rd-copy">Important step-by-step instructions on how to access the building, check in, get connected to WiFi, and more!</p></div>
        <!-- [FIELD] per-property arrival guide URL -->
        <div class="rd-act"><a class="rd-link" href="#" id="rdArrival">View arrival information</a></div>
      </section>
    </div>
    <div class="rd-actions" id="rdActions">
      <a class="bk-btn slate" id="rdModify" href="/reservations/modify">Modify Booking</a>
      <button type="button" class="bk-btn-g" data-open="cancel">Cancel Booking</button>
    </div>
  </div></div>
  <div class="bk-card"><div class="bk-pad">
    <h2 class="bk-rail-h">Payment summary</h2>
    <div class="rd-pay">
      <span class="rd-cardmark" aria-hidden="true"></span><span class="rd-last4">&bull;&bull;&bull;&bull; 7744</span>
      <span class="rd-est"><small>Estimated total</small> <b id="rdTotal">&mdash;</b></span>
      <button type="button" class="rd-link rd-break" id="rdBreakBtn" aria-expanded="false" aria-controls="rdBreak">View breakdown</button>
    </div>
    <div class="rd-breakdown" id="rdBreak" hidden>
      <div class="bk-line strong"><span>Description</span><span>Charges</span></div>
      <div id="rdLines"></div>
      <div class="bk-line strong"><span>Estimated total</span><span id="rdTotal2"></span></div>
    </div>
    <p class="bk-note" style="text-align:left">Card shown as last four digits only &mdash; payment details stay with Shift4. Sample charges for design review.</p>
  </div></div>
</div>
<dialog class="bk-fees rd-dlg" id="rdDlg" aria-labelledby="rdDlgH">
  <button type="button" class="bk-fees-x" data-close aria-label="Close">&times;</button>
  <div id="rdDlgBody"></div>
</dialog>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q();
  // Sample reservation when opened without a lookup (static review links)
  var r={property:q.property||'sol-modern','in':q['in']||'2026-10-24',out:q.out||'2026-10-26',
    rooms:q.rooms||'one-bedroom:1:fall',adults:q.adults||'1',children:q.children||'0',promo:q.promo||''};
  var S=BOOK.summary(r), cur=S.cur, $=function(id){return document.getElementById(id)};
  var conf=(q.conf||'PHXA100000545').toUpperCase();
  $('rdContext').textContent=cur.name+', '+cur.city+' · Confirmation '+conf;
  $('rdProp').textContent=cur.name;
  $('rdAddr').textContent=cur.address||(cur.city+', '+cur.state);
  $('rdMap').href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((cur.address||cur.name+' '+cur.city));
  $('rdCode').textContent=r.promo?r.promo.toUpperCase():'—';
  $('rdConf').textContent=conf;
  $('rdNights').textContent=S.nights+(S.nights>1?' nights':' night');
  $('rdDates').textContent=BOOK.fmtDate(r['in'])+' → '+BOOK.fmtDate(r.out);
  if(q.first) $('rdFirst').textContent=q.first;
  if(q.last) $('rdLast').textContent=q.last;
  if(q.email) $('rdEmail').textContent=q.email;
  if(q.phone) $('rdPhone').textContent=q.phone;
  $('rdLines').innerHTML=S.lines;
  $('rdTotal').textContent=$('rdTotal2').textContent=BOOK.cents(S.total);
  $('rdModify').href='/reservations/modify?'+BOOK.qs({modify:conf,property:r.property,'in':r['in'],out:r.out,
    adults:r.adults,children:r.children,promo:r.promo||null,oin:r['in'],oout:r.out,orooms:r.rooms,rooms:null});
  $('rdBreakBtn').addEventListener('click',function(){
    var o=$('rdBreak').hidden; $('rdBreak').hidden=!o; this.setAttribute('aria-expanded',o);
    this.textContent=o?'Collapse breakdown':'View breakdown';
  });
  var dlg=$('rdDlg'), body=$('rdDlgBody');
  function msg(text,check){ return (check?'''+repr(CHECK_SVG)+''':'')+'<p class="rd-msg" id="rdDlgH">'+text+'</p>'; }
  function cancelled(){
    $('rdStatus').hidden=false; $('rdActions').classList.add('rd-off');
    [].forEach.call($('rdActions').querySelectorAll('a,button'),function(b){ b.setAttribute('aria-disabled','true'); b.tabIndex=-1; });
  }
  var VIEWS={
    resent:function(){ body.innerHTML=msg('Your confirmation has been resent to the email and phone number on file'); },
    updated:function(){ body.innerHTML=msg('Details updated successfully!'); },
    cancelled:function(){ body.innerHTML=msg('Your booking cancelled successfully!',true); cancelled(); },
    edit:function(){
      body.innerHTML='<h2 class="rd-dlg-h" id="rdDlgH">Edit email / phone</h2>'+
        '<form id="rdEdit" class="rd-form"><div class="bk-f"><label for="rdE">Email *</label><input id="rdE" type="email" autocomplete="email" required value="'+$('rdEmail').textContent+'"></div>'+
        '<div class="bk-f"><label for="rdP">Phone *</label><input id="rdP" type="tel" autocomplete="tel" required value="'+$('rdPhone').textContent+'"></div>'+
        '<div class="rd-dlg-btns"><button class="bk-btn slate" type="submit">Save</button><button class="bk-btn-g" type="button" data-close>Cancel</button></div></form>';
      $('rdEdit').addEventListener('submit',function(e){
        e.preventDefault(); if(!this.reportValidity()) return;
        $('rdEmail').textContent=$('rdE').value.trim(); $('rdPhone').textContent=$('rdP').value.trim();
        VIEWS.updated();
      });
    },
    cancel:function(){
      body.innerHTML='<h2 class="rd-dlg-h" id="rdDlgH">Cancel reservation</h2>'+
        '<p class="rd-copy">Are you sure you want to cancel this reservation? Review the cancellation policy and select Yes or No to continue</p>'+
        '<details class="rd-policy" open><summary>Cancellation policy</summary><p>'''+CANCEL_POLICY+'''</p>'+
        '<p class="rd-src">Policy text pulls from the booked rate in StayNTouch.</p></details>'+
        '<div class="rd-dlg-btns"><button class="bk-btn slate" type="button" id="rdYes">Yes</button><button class="bk-btn-g" type="button" data-close>No</button></div>';
      $('rdYes').addEventListener('click',VIEWS.cancelled);
    }
  };
  function open(v){ VIEWS[v](); if(!dlg.open) dlg.showModal(); }
  document.addEventListener('click',function(e){
    var t=e.target.closest&&e.target.closest('[data-open]');
    if(t&&!t.closest('.rd-off')){ open(t.getAttribute('data-open')); return; }
    if(e.target.closest&&e.target.closest('[data-close]')||e.target===dlg) dlg.close();
  });
  if(q.show&&VIEWS[q.show]) open(q.show);
  else if(/\/reservations\/cancel/.test(location.pathname)) open('cancel');  // 7d entry URL
  if(q.status==='cancelled') cancelled();
});
</script>''')

for fname,(title,body) in PAGES.items():
    open(os.path.join(ROOT,fname),'w').write(_newtab(page(title,body)))
    print('wrote',fname)

# ═══ 1a-static. PER-CITY STATIC PAGES ═══
# Owner 9-30: shareable static markup for the build team — property cards are
# baked into the HTML (no JS needed to see content); JS only carries dates +
# discount code into the card links. KEEP IN SYNC with assets/booking-demo.js
# CITIES/PROPERTIES (single source once the CMS drives both).
# (slug, name, city/state, stay-note, neighborhood, one-liner, amenities)
# Laurie 10-8: VIEW PROPERTY beside CHECK AVAILABILITY, location pin with the
# neighborhood, one line on suites + key amenities, amenities expand/collapse.
# Neighborhoods confirmed by Laurie: Inkwell = NoDa, Joinerys = Optimist Park.
# Everything marked [FIELD] is sample copy for ops/marketing to replace.
_AM=['Full kitchen','In-unit washer &amp; dryer','Fitness center','Keyless entry','Dedicated workspace','Pet friendly']
_LINE='[FIELD] Studios to two bedrooms &middot; full kitchens &middot; in-unit laundry &middot; fitness center'
CITY_DATA={
 'charlotte':   ('Charlotte',   [('inkwell','Inkwell','Charlotte, NC','','NoDa',_LINE,_AM,139,True),
                                 ('joinery-north','Joinery North','Charlotte, NC','','Optimist Park',_LINE,_AM,129,True),
                                 ('joinery-west','Joinery West','Charlotte, NC','','Optimist Park',_LINE,_AM,135,True)]),
 'austin':      ('Austin',      [('sentral-east-austin-1630','Sentral East Austin 1630','Austin, TX',' · 30+ nights','East Austin',_LINE,_AM,119,True),
                                 ('sentral-east-austin-1614','Sentral East Austin 1614','Austin, TX','','East Austin',_LINE,_AM,149,False)]),
 'los-angeles': ('Los Angeles', [('sentral-dtla-755','Sentral DTLA 755','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM,159,True),
                                 ('sentral-dtla-732','Sentral DTLA 732','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM,155,True),
                                 ('figueroa-eight','Figueroa Eight','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM,169,True)]),
 'miami':       ('Miami',       [('alea','Alea','Miami, FL','','[FIELD] Neighborhood',_LINE,_AM,189,True),
                                 ('sentral-wynwood','Sentral Wynwood','Miami, FL','','Wynwood',_LINE,_AM,179,True)]),
}
# Property pages: only the Sol Modern template is built so far, so every VIEW
# PROPERTY lands on it for review. PRODUCTION: /stay/{property-slug}.
PROP_PAGE={'sol-modern':'/stay/sol-modern'}
PIN='<svg class="bk-pin" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M12 22s7-6.4 7-12a7 7 0 0 0-14 0c0 5.6 7 12 7 12z" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
IMGS=['/assets/bk-city-1.jpg','/assets/bk-city-2.jpg','/assets/bk-city-3.jpg']
for cslug,(cname,props) in CITY_DATA.items():
    cards='\n'.join(
        '    <div class="bk-prop" data-prop="'+ps+'" data-promo-ok="'+('1' if promo_ok else '0')+'">\n'
        '      <div class="bk-prop-name bk-prop-name-top">'+pn+'</div>\n'
        '      <img class="bk-prop-img" src="'+IMGS[i%3]+'" alt="'+pn+'">\n'
        '      <div class="bk-prop-body">\n'
        '      <!-- PRODUCTION: lowest available rate per community for the requested dates\n'
        '           (StayNTouch via SentralOS). A promo with no eligible rate for this\n'
        '           community shows *Excluded from Promotion and the lowest date-rate —\n'
        '           the price never blanks because of a promo. -->\n'
        '      <div class="bk-prop-mid">\n'
        '        <div class="bk-prop-meta">'+meta+' &middot; '+hood+('<br>'+note.replace(' &middot; ','') if note else '')+'</div>\n'
        '        <div class="bk-pb"><span class="bk-pb-excl" hidden>*Excluded from Promotion</span>'
        '<span class="bk-pb-from">Rates From</span>'
        '<span class="bk-pb-amt">'+_money(low)+'</span> <span class="bk-pb-per">/ night</span>'
        '<small class="bk-pb-note">Before taxes</small></div>\n'
        '      </div>\n'
        '      <p class="bk-prop-line">'+line+'</p>\n'
        '      <details class="bk-prop-am"><summary>Amenities</summary><ul>'+''.join('<li>'+a+'</li>' for a in am)+'</ul></details>\n'
        '      <div class="bk-prop-btns">\n'
        '        <a class="bk-btn bk-prop-book" data-avail href="/book/search?property='+ps+'">Book Now &nbsp;&rarr;</a>\n'
        '        <a class="bk-btn slate" href="'+PROP_PAGE.get(ps,'/stay/sol-modern')+'">Property &nbsp;&rarr;</a>\n'
        '      </div></div>\n'
        '    </div>' for i,(ps,pn,meta,note,hood,line,am,low,promo_ok) in enumerate(props))
    body=(header('Sentral &mdash; Book a Stay',cname+'. <em>Choose your Sentral.</em>','ctContext')
      +'\n'+RIBBON+'''
<div class="bk-wrap">
  <form class="bk-editbar" id="ctEdit">
    <div class="bk-f"><label for="ctIn">Check-in</label><input id="ctIn" type="date"></div>
    <div class="bk-f"><label for="ctOut">Check-out</label><input id="ctOut" type="date"></div>
    <div class="bk-f"><label for="ctAd">Adults</label>
      <select id="ctAd"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></div>
    <div class="bk-f"><label for="ctCh">Children</label>
      <select id="ctCh"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option></select></div>
    <div class="bk-f"><label for="ctPromo">Discount code</label><input id="ctPromo" type="text" placeholder="e.g. FALL20"></div>
    <button class="bk-btn" type="submit">Apply &nbsp;&rarr;</button>
  </form>
  <div class="bk-props">
'''+cards+'''
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), nights=BOOK.nights(q['in'],q.out);
  document.getElementById('ctContext').textContent='''+repr(str(len(props)))+'''+' properties'+(nights?' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out):'')+(q.promo?' · code '+q.promo.toUpperCase()+' will apply at checkout':'');
  if(q['in']) document.getElementById('ctIn').value=q['in'];
  if(q.out) document.getElementById('ctOut').value=q.out;
  if(q.promo) document.getElementById('ctPromo').value=q.promo;
  // Rate-line rule (owner 10-14): if a promo code applies but yields no rate
  // for a community, the card still shows the lowest available rate for the
  // requested dates — never a blank price. PRODUCTION: StayNTouch lowest
  // availability per community for q.in→q.out; promo pricing where eligible,
  // lowest-date rate as the fallback.
  if(nights){
    [].forEach.call(document.querySelectorAll('.bk-prop'),function(card){
      var note=card.querySelector('.bk-pb-note'), excl=card.querySelector('.bk-pb-excl');
      if(!note) return;
      var ok=card.getAttribute('data-promo-ok')!=='0';
      note.textContent='For your dates · before taxes';
      if(q.promo){ if(ok){ note.textContent+=' · promo-eligible'; } else if(excl){ excl.hidden=false; } }
    });
  }
  if(q.adults) document.getElementById('ctAd').value=q.adults;
  if(q.children) document.getElementById('ctCh').value=q.children;
  [].forEach.call(document.querySelectorAll('.bk-prop'),function(c){
    c.querySelector('[data-avail]').href='/book/search?'+BOOK.qs({property:c.getAttribute('data-prop'),city:null});
  });
  document.getElementById('ctEdit').addEventListener('submit',function(e){
    e.preventDefault();
    location.search='?'+BOOK.qs({
      'in':document.getElementById('ctIn').value, out:document.getElementById('ctOut').value,
      adults:document.getElementById('ctAd').value, children:document.getElementById('ctCh').value,
      promo:document.getElementById('ctPromo').value.trim()||null});
  });
});
</script>''')

    fname='city-'+cslug+'.html'
    open(os.path.join(ROOT,fname),'w').write(_newtab(page(cname+' — Book a Stay — Sentral',body)))
    print('wrote',fname)

# ═══ STATIC BAKE (owner 9-30): funnel pages carry the Sol Modern demo content
# in their HTML — visible without JS, view-source-able for the build team.
# The page JS re-renders the same markup from the query string on load.
# KEEP IN SYNC with assets/booking-demo.js. ═══
ROOMS_PY=[('studio','Studio','Sleeps 2 · 1 Queen Bed · 1 Bath · 517 Sq Ft',189),
          ('one-bedroom','One Bedroom','Sleeps 2 · 1 Queen Bed · 1 Bath · 673 Sq Ft',229),
          ('two-bedroom','Two Bedroom','Sleeps 4 · 2 Queen Beds · 2 Baths · 1,053 Sq Ft',319)]
RIMG={'studio':'/assets/bk-room-studio.jpg','one-bedroom':'/assets/bk-room-1br.jpg','two-bedroom':'/assets/bk-room-2br.jpg'}
PLANS_PY=[('fall','Limited Time Fall Sale | Stay 2+ Nights &amp; Save up to 20%','Flexible rate. Blackout dates and terms apply.',0.80),
          ('campus','Campus Bound','For campus tours, games &amp; parents&rsquo; weekends. Terms apply.',0.86),
          ('direct','Sentral.com Book Direct Rate | Save up to 10% off Best Rates','Book direct and save.',0.90)]
PROPS_PY=[('sol-modern','Phoenix — Sol Modern'),('sentral-old-town','Scottsdale — Sentral Old Town'),
 ('sentral-dtla-755','Los Angeles — Sentral DTLA 755 (30+ nights)'),('sentral-dtla-732','Los Angeles — Sentral DTLA 732 (30+ nights)'),
 ('figueroa-eight','Los Angeles — Figueroa Eight (30+ nights)'),('sentral-union-station','Denver — Sentral Union Station'),
 ('alea','Miami — Alea'),('sentral-wynwood','Miami — Sentral Wynwood'),('star-metals','Atlanta — Star Metals West Midtown'),
 ('sentral-michigan-avenue','Chicago — Sentral Michigan Avenue'),('otonomus','Las Vegas — Otonomus'),
 ('inkwell','Charlotte — Inkwell'),('joinery-north','Charlotte — Joinery North'),('joinery-west','Charlotte — Joinery West'),
 ('the-battery','Philadelphia — The Battery (30+ nights)'),('sentral-sobro','Nashville — Sentral SoBro'),
 ('sentral-east-austin-1630','Austin — Sentral East Austin 1630'),('sentral-east-austin-1614','Austin — Sentral East Austin 1614'),
 ('forme','Houston — Forme'),('sentral-first-hill','Seattle — Sentral First Hill (30+ nights)')]
def money(n): return '$'+format(round(n),',')
def spec_spans(spec): return ' &middot; '.join('<span>'+x+'</span>' for x in spec.split(' · '))
def bake(fname, subs):
    fp=os.path.join(ROOT,fname); s=open(fp).read()
    for old,new in subs:
        assert s.count(old)==1, fname+' MISS '+old[:60]
        s=s.replace(old,new)
    open(fp,'w').write(s); print('baked',fname)

# — checkout: representative sample stay (1 × One Bedroom, Fall Sale, 3 nights, 2 adults) —
sub=183*3; rfee=15*3; taxes=[('City Tax',6),('Local Tax',1.5),('State Tax',5)]
def cents(n): return '$'+format(n,',.2f')
tl=[(l,round(sub*p)/100) for l,p in taxes]
lines=('<div class="bk-line"><span>Nightly total <small>3 nights</small></span><span>'+cents(sub-rfee)+'</span></div>'
  '<div class="bk-line"><span>Resort &amp; Destination Fee <small>(sample)</small></span><span>'+cents(rfee)+'</span></div>'
  +''.join('<div class="bk-line"><span>'+l+' <small>(sample '+format(p,'g')+'%)</small></span><span>'+cents(a)+'</span></div>' for (l,a),(_,p) in zip(tl,taxes)))
bake('book-checkout.html',[
 ('<h3 id="railProp"></h3>','<h3 id="railProp">Sol Modern, Phoenix</h3>'),
 ('<div class="bk-rail-sub" id="railAddr"></div>','<div class="bk-rail-sub" id="railAddr">50 E. Fillmore Street, Phoenix, AZ 85004</div>'),
 ('<div id="railRooms"></div>','<div id="railRooms"><div class="bk-suite"><div><b>One Bedroom</b><small>Limited Time Fall Sale | Stay 2+ Nights &amp; Save up to 20%</small></div><a href="/book/search">Modify</a></div><a class="bk-addroom" href="/book/search">+ Add another suite</a></div>'),
 ('<dl class="bk-facts" id="railFacts"></dl>','<dl class="bk-facts" id="railFacts"><div><dt>Check-in</dt><dd>Sample date<small>4:00 PM</small></dd></div><div><dt>Check-out</dt><dd>Sample date<small>11:00 AM</small></dd></div><div><dt>Nights</dt><dd>3</dd></div><div><dt>Guests</dt><dd>2 adults, 0 children</dd></div></dl>'),
 ('<div id="railLines"></div>','<div id="railLines">'+lines+'</div>'),
 ('<span id="railTotal">&mdash;</span>','<span id="railTotal">'+cents(sub+sum(a for _,a in tl))+'</span>'),
])

# — confirmation: sample number + same itemized summary as checkout —
bake('book-confirm.html',[
 ('<div class="bk-confirm-n" id="cfNum">SENTRAL-DEMO</div>','<div class="bk-confirm-n" id="cfNum">SENT-SAMPLE</div>'),
 ('<p style="font-size:.9375rem;color:#4a4643;max-width:60ch" id="cfMsg"></p>','<p style="font-size:.9375rem;color:#4a4643;max-width:60ch" id="cfMsg">Your suite at Sol Modern is set. Check-in opens at 4:00 PM with keyless entry &mdash; your code arrives the morning of arrival.</p>'),
 ('<strong id="cfPhone"></strong>','<strong id="cfPhone">(833) 370-4161</strong>'),
 ('<h3 id="railProp"></h3>','<h3 id="railProp">Sol Modern, Phoenix</h3>'),
 ('<div class="bk-rail-sub" id="railAddr"></div>','<div class="bk-rail-sub" id="railAddr">50 E. Fillmore Street, Phoenix, AZ 85004</div>'),
 ('<div id="railRooms"></div>','<div id="railRooms"><div class="bk-suite"><div><b>One Bedroom</b><small>Limited Time Fall Sale | Stay 2+ Nights &amp; Save up to 20%</small></div></div></div>'),
 ('<dl class="bk-facts" id="railFacts"></dl>','<dl class="bk-facts" id="railFacts"><div><dt>Check-in</dt><dd>Sample date<small>4:00 PM</small></dd></div><div><dt>Check-out</dt><dd>Sample date<small>11:00 AM</small></dd></div><div><dt>Nights</dt><dd>3</dd></div><div><dt>Guests</dt><dd>2 adults, 0 children</dd></div></dl>'),
 ('<div id="railLines"></div>','<div id="railLines">'+lines+'</div>'),
 ('<span id="railTotal">&mdash;</span>','<span id="railTotal">'+cents(sub+sum(a for _,a in tl))+'</span>'),
])
