#!/usr/bin/env python3
"""
Booking-funnel generator — Phase 3 (6-page booking plan, 2026-09-25).

Generates: book-search.html (P0), book-room.html, book-checkout.html,
book-confirm.html, city-stay.html. Chrome (nav/hamburger/footer markup) is
extracted from property-template.html AT BUILD TIME so the funnel always
matches the site. Shared styles: booking-chrome.css (lifted chrome CSS) +
booking.css (funnel components). ALL rates/availability/taxes are SAMPLE
data from assets/booking-demo.js — production pulls live from StayNTouch
via SentralOS (pages 2/4/6), Shift4 embed unchanged (page 5).

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
def page(title,body):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
      '<meta name="robots" content="noindex">\n'
      '<title>'+title+'</title>\n'
      '<link rel="stylesheet" href="/booking-chrome.css">\n'
      '<link rel="stylesheet" href="/overrides.css?v=4dark31">\n'
      '<link rel="stylesheet" href="/booking.css">\n'
      '<script src="/assets/booking-demo.js" defer></script>\n'
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
PAGES['book-search.html']=('Search Availability — Book a Stay — Sentral','<section class="bkh dark">\n  <div class="bkh-inner">\n    <span class="bkh-eyebrow">Sentral &mdash; Book a Stay</span>\n    <h1>Choose your <em>suite.</em></h1>\n    <p class="bkh-sub" id="bkhContext">Select a property and dates to see availability.</p>\n    <div class="bkh-steps" aria-label="Booking progress">\n      <span class="bkh-step on">1 &middot; Suites &amp; Availability</span>\n      <span class="bkh-step">2 &middot; Checkout</span>\n      <span class="bkh-step">3 &middot; Confirmation</span>\n    </div>\n  </div>\n</section>\n<div class="bk-demo">Design prototype &mdash; sample rates &amp; availability &middot; live data comes from StayNTouch via SentralOS at build</div>\n<div class="bk-wrap">\n  <!-- 1. Home widget hands city/dates/guests here; no PMS call upstream.\n       PRODUCTION (P0): this page pulls live availability + pricing from\n       StayNTouch via SentralOS (data pull method TBC w/ Nathan) and hosts\n       the multi-room booking module below. -->\n  <form class="bk-editbar" id="bkEdit">\n    <div class="bk-f"><label for="bkProp">Property</label>\n      <select id="bkProp"></select></div>\n    <div class="bk-f"><label for="bkIn">Check-in</label><input id="bkIn" type="date"></div>\n    <div class="bk-f"><label for="bkOut">Check-out</label><input id="bkOut" type="date"></div>\n    <div class="bk-f"><label for="bkAd">Adults</label>\n      <select id="bkAd"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></div>\n    <div class="bk-f"><label for="bkCh">Children</label>\n      <select id="bkCh"><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option></select></div>\n    <button class="bk-btn" type="submit">Update Search &nbsp;&rarr;</button>\n  </form>\n  <div id="bkCityAlert"></div>\n  <div class="bk-grid">\n    <div id="bkResults"></div>\n    <aside class="bk-rail" aria-label="Your stay">\n      <h3 id="railProp">Your stay</h3>\n      <div class="bk-rail-sub" id="railDates"></div>\n      <div id="railLines"></div>\n      <hr>\n      <div class="bk-total"><span>Total</span><span id="railTotal">&mdash;</span></div>\n      <a class="bk-btn wide off" id="railGo" href="#">Continue to Checkout &nbsp;&rarr;</a>\n      <div class="bk-note">Sample rates for design review &mdash; taxes shown at checkout</div>\n    </aside>\n  </div>\n</div>\n<script>\ndocument.addEventListener(\'DOMContentLoaded\',function(){\n  var q=BOOK.q(), sel=BOOK.parseRooms(q.rooms);\n  var props=BOOK.PROPERTIES, propSel=document.getElementById(\'bkProp\');\n  props.forEach(function(p){\n    var o=document.createElement(\'option\'); o.value=p.slug;\n    o.textContent=p.city+\' — \'+p.name+(p.minStay>1?\' (30+ nights)\':\'\');\n    propSel.appendChild(o);\n  });\n  var cur=BOOK.prop(q.property) || null;\n  // 1a. City hand-off: multi-property market w/ no property chosen → selector\n  var alertBox=document.getElementById(\'bkCityAlert\');\n  if(!cur && q.city && BOOK.CITIES[q.city]){\n    var c=BOOK.CITIES[q.city];\n    alertBox.innerHTML=\'<div class="bk-alert">\'+c.name+\' has \'+c.props.length+\n      \' Sentral properties. <a href="/stay/\'+q.city+\'?\'+BOOK.qs({})+\'">Choose your \'+c.name+\' property &rarr;</a></div>\';\n    cur=BOOK.prop(c.props[0]);\n  }\n  if(!cur){\n    var cityMatch = q.city && props.filter(function(p){return p.city.toLowerCase().replace(/ /g,\'-\')===q.city})[0];\n    cur = cityMatch || props[0];\n  }\n  propSel.value=cur.slug;\n  if(q[\'in\']) document.getElementById(\'bkIn\').value=q[\'in\'];\n  if(q.out) document.getElementById(\'bkOut\').value=q.out;\n  if(q.adults) document.getElementById(\'bkAd\').value=q.adults;\n  if(q.children) document.getElementById(\'bkCh\').value=q.children;\n\n  document.getElementById(\'bkEdit\').addEventListener(\'submit\',function(e){\n    e.preventDefault();\n    location.search=\'?\'+BOOK.qs({property:propSel.value,city:null,\n      \'in\':document.getElementById(\'bkIn\').value,out:document.getElementById(\'bkOut\').value,\n      adults:document.getElementById(\'bkAd\').value,children:document.getElementById(\'bkCh\').value,\n      rooms:BOOK.roomsParam(sel)});\n  });\n\n  var nights=BOOK.nights(q[\'in\'],q.out);\n  document.getElementById(\'bkhContext\').textContent =\n    cur.name+\', \'+cur.city+(nights? \' · \'+BOOK.fmtDate(q[\'in\'])+\' → \'+BOOK.fmtDate(q.out)+\' · \'+nights+(nights>1?\' nights\':\' night\') : \' — choose dates to see availability\');\n\n  // room results — multi-room module (quantity per suite type)\n  var IMGS={\'studio\':\'/assets/ig-social-1.jpg\',\'one-bedroom\':\'/assets/ig-social-2.jpg\',\'two-bedroom\':\'/assets/ig-social-3.jpg\'};\n  var res=document.getElementById(\'bkResults\');\n  res.innerHTML = cur.rooms.map(function(r){\n    var detail=\'/book/room?\'+BOOK.qs({property:cur.slug,city:null,type:r.slug,rooms:BOOK.roomsParam(sel)});\n    return \'<div class="bk-card"><div class="bk-room">\'+\n      \'<img class="bk-room-img" src="\'+IMGS[r.slug]+\'" alt="\'+r.name+\' suite">\'+\n      \'<div class="bk-room-mid">\'+\n        \'<div class="bk-room-name">\'+r.name+\'</div>\'+\n        \'<div class="bk-specs">\'+r.specs+\'</div>\'+\n        \'<div class="bk-room-links"><a href="\'+detail+\'">Rates &amp; suite details &nbsp;&rarr;</a></div>\'+\n      \'</div>\'+\n      \'<div class="bk-room-side">\'+\n        \'<span class="bk-price-n">\'+BOOK.money(r.from)+\'</span><span class="bk-price-l">Sample &middot; from / night</span>\'+\n        \'<div class="bk-step-ctl"><span class="lbl">Rooms</span>\'+\n          \'<button type="button" data-dec="\'+r.slug+\'" aria-label="Remove a \'+r.name+\'">&minus;</button>\'+\n          \'<span class="n" id="n-\'+r.slug+\'">\'+(sel[r.slug]||0)+\'</span>\'+\n          \'<button type="button" data-inc="\'+r.slug+\'" aria-label="Add a \'+r.name+\'">+</button>\'+\n        \'</div>\'+\n      \'</div>\'+\n    \'</div></div>\';\n  }).join(\'\');\n  if(cur.minStay>1) alertBox.innerHTML+=\'<div class="bk-alert">\'+cur.name+\' hosts extended stays only &mdash; 30 nights or more.</div>\';\n\n  res.addEventListener(\'click\',function(e){\n    var inc=e.target.getAttribute(\'data-inc\'), dec=e.target.getAttribute(\'data-dec\'), k=inc||dec;\n    if(!k) return;\n    sel[k]=Math.max(0,Math.min(9,(sel[k]||0)+(inc?1:-1)));\n    document.getElementById(\'n-\'+k).textContent=sel[k];\n    rail();\n  });\n\n  function rail(){\n    document.getElementById(\'railProp\').textContent=cur.name+\', \'+cur.city;\n    document.getElementById(\'railDates\').textContent =\n      nights? BOOK.fmtDate(q[\'in\'])+\' → \'+BOOK.fmtDate(q.out)+\' · \'+nights+(nights>1?\' nights\':\' night\') : \'Choose dates above\';\n    var lines=\'\',total=0,count=0;\n    cur.rooms.forEach(function(r){\n      var n=sel[r.slug]||0; if(!n) return; count+=n;\n      var amt=r.from*n*(nights||1);\n      total+=amt;\n      lines+=\'<div class="bk-line"><span>\'+n+\' × \'+r.name+(nights?\' <small>(\'+nights+\' nights)</small>\':\'\')+\'</span><span>\'+BOOK.money(amt)+\'</span></div>\';\n    });\n    document.getElementById(\'railLines\').innerHTML = lines||\'<div class="bk-line"><small>Add rooms to build your stay.</small></div>\';\n    document.getElementById(\'railTotal\').textContent = count&&nights? BOOK.money(total):\'—\';\n    var ok = count>0 && nights && !(cur.minStay>1 && nights<30);\n    var go=document.getElementById(\'railGo\');\n    go.classList.toggle(\'off\',!ok);\n    go.href=\'/book/checkout?\'+BOOK.qs({property:cur.slug,city:null,rooms:BOOK.roomsParam(sel)});\n    if(cur.minStay>1&&nights&&nights<30)\n      document.getElementById(\'railLines\').innerHTML+=\'<div class="bk-line"><small>This property requires 30+ nights.</small></div>\';\n  }\n  rail();\n});\n</script>')

# ═══ 4. ROOM LIST + ROOM DETAIL — live StayNTouch rate plans at build ═══
PAGES['book-room.html']=('Suite Rates & Details — Book a Stay — Sentral',
header('Sentral &mdash; Book a Stay','Every rate for <em>this suite.</em>','rmContext',0)+'''
'''+RIBBON+'''
<div class="bk-wrap">
  <!-- PRODUCTION: rate plans + pricing pull live from StayNTouch (sale, early
       booking, direct) — same data pull as Search Availability, TBC w/ Nathan. -->
  <p style="margin:-8px 0 20px"><a class="bk-btn-g" id="rmBack" href="/book/search">&larr; All suites</a></p>
  <div class="bk-grid">
    <div>
      <div class="bk-card">
        <img class="bk-room-img" id="rmImg" style="height:320px;width:100%" src="/assets/ig-social-1.jpg" alt="Suite living area">
        <div class="bk-pad">
          <div class="bk-room-name" id="rmName" style="font-size:1.6rem"></div>
          <div class="bk-specs" id="rmSpecs"></div>
          <p style="font-size:.9375rem;color:#4a4643;margin-top:12px;max-width:64ch" id="rmDesc"></p>
        </div>
      </div>
      <div class="bk-card">
        <div class="bk-pad" style="padding-bottom:8px"><span class="bk-eyebrow">Choose your rate</span></div>
        <div id="rmPlans"></div>
      </div>
      <!-- Map view carried forward from the current room list (plan §4) -->
      <div class="bk-embed"><strong>Property map &mdash; carried forward</strong>
        <p>The map view from the current room list renders here per property. [FIELD] map embed.</p></div>
    </div>
    <aside class="bk-rail" aria-label="Your stay">
      <h3 id="railProp"></h3>
      <div class="bk-rail-sub" id="railDates"></div>
      <div class="bk-line"><small>Rates apply to the whole stay. Multi-room bookings continue from Suites &amp; Availability.</small></div>
      <div class="bk-note">Sample rates for design review</div>
    </aside>
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), cur=BOOK.prop(q.property)||BOOK.PROPERTIES[0];
  var r=cur.rooms.filter(function(x){return x.slug===q.type})[0]||cur.rooms[0];
  var nights=BOOK.nights(q['in'],q.out);
  var IMGS={'studio':'/assets/ig-social-1.jpg','one-bedroom':'/assets/ig-social-2.jpg','two-bedroom':'/assets/ig-social-3.jpg'};
  document.getElementById('rmImg').src=IMGS[r.slug]||IMGS.studio;
  document.getElementById('rmName').textContent=r.name;
  document.getElementById('rmSpecs').textContent=r.specs;
  document.getElementById('rmDesc').textContent='Furnished end to end — full kitchen, in-unit washer and dryer, dedicated workspace, and a real bedroom door. Sample copy; per-suite copy is a [FIELD].';
  document.getElementById('rmContext').textContent=cur.name+', '+cur.city+(nights? ' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night'):'');
  document.getElementById('rmBack').href='/book/search?'+BOOK.qs({type:null,plan:null});
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railDates').textContent=nights? BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night'):'Choose dates on the previous step';
  document.getElementById('rmPlans').innerHTML = BOOK.PLANS.map(function(pl){
    var nightly=r.from*pl.mult;
    var total=nights? ' · '+BOOK.money(nightly*nights)+' total' : '';
    return '<div class="bk-plan"><div>'+
      '<div class="bk-plan-name">'+pl.name+'</div>'+
      '<div class="bk-plan-note">'+pl.note+'</div></div>'+
      '<div style="display:flex;align-items:center;gap:18px">'+
      '<span class="bk-plan-price">'+BOOK.money(nightly)+'<span class="bk-price-l" style="display:block;text-align:right">sample / night'+total+'</span></span>'+
      '<a class="bk-btn" href="/book/checkout?'+BOOK.qs({property:cur.slug,rooms:r.slug+':1',plan:pl.slug,type:null})+'">Select &nbsp;&rarr;</a>'+
      '</div></div>';
  }).join('');
});
</script>''')

# ═══ 5. BOOKING DETAILS (CHECKOUT) — Storyblok shell + Shift4 embed ═══
PAGES['book-checkout.html']=('Checkout — Book a Stay — Sentral',
header('Sentral &mdash; Book a Stay','Almost <em>home.</em>','ckContext',1)+'''
'''+RIBBON+'''
<div class="bk-wrap">
  <div class="bk-grid">
    <div>
      <div class="bk-card"><div class="bk-pad">
        <span class="bk-eyebrow">Guest information</span>
        <!-- Native guest-info form (plan §5). -->
        <form id="ckForm" class="bk-field-grid" style="margin-top:12px">
          <div class="bk-f"><label for="ck-fn">First name</label><input id="ck-fn" autocomplete="given-name" required></div>
          <div class="bk-f"><label for="ck-ln">Last name</label><input id="ck-ln" autocomplete="family-name" required></div>
          <div class="bk-f"><label for="ck-em">Email</label><input id="ck-em" type="email" autocomplete="email" required></div>
          <div class="bk-f"><label for="ck-ph">Phone</label><input id="ck-ph" type="tel" autocomplete="tel" required></div>
          <div class="bk-f full"><label for="ck-rq">Special requests <span style="text-transform:none;letter-spacing:.02em">&mdash; optional</span></label><input id="ck-rq"></div>
        </form>
        <!-- SHIFT4 — the existing payment capture embeds here UNCHANGED (plan §5).
             The prototype deliberately renders no card fields: never collect
             payment data outside the Shift4 iframe. -->
        <div class="bk-embed"><strong>Shift4 payment capture</strong>
          <p>The current Shift4 payment embed drops in here unchanged. No card fields exist in this prototype by design.</p></div>
        <a class="bk-btn wide" id="ckGo" href="/book/confirmation">Complete Booking &nbsp;&rarr;</a>
        <div class="bk-note">Flexible cancellation on most rates &middot; no hidden fees</div>
      </div></div>
    </div>
    <aside class="bk-rail" aria-label="Stay summary">
      <h3 id="railProp"></h3>
      <div class="bk-rail-sub" id="railDates"></div>
      <div id="railLines"></div>
      <hr>
      <div id="railTaxes"></div>
      <div class="bk-total"><span>Total</span><span id="railTotal">&mdash;</span></div>
      <div class="bk-note">Sample rates &amp; tax lines &mdash; property-specific tax items are driven by property data at build</div>
    </aside>
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), cur=BOOK.prop(q.property)||BOOK.PROPERTIES[0];
  var sel=BOOK.parseRooms(q.rooms), plan=BOOK.plan(q.plan), nights=BOOK.nights(q['in'],q.out)||1;
  document.getElementById('ckContext').textContent=cur.name+', '+cur.city+' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out);
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railDates').textContent=BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night')+' · '+plan.name;
  var sub=0,lines='';
  cur.rooms.forEach(function(r){
    var n=sel[r.slug]||0; if(!n) return;
    var amt=r.from*plan.mult*n*nights; sub+=amt;
    lines+='<div class="bk-line"><span>'+n+' × '+r.name+' <small>('+nights+' × '+BOOK.money(r.from*plan.mult)+')</small></span><span>'+BOOK.money(amt)+'</span></div>';
  });
  if(!sub){ lines='<div class="bk-line"><small>No rooms selected — start from Suites &amp; Availability.</small></div>'; }
  document.getElementById('railLines').innerHTML=lines+(sub?'<div class="bk-line strong"><span>Subtotal</span><span>'+BOOK.money(sub)+'</span></div>':'');
  var taxes=0,tl='';
  if(sub) BOOK.TAXES.forEach(function(t){
    if(t.pct!=null){ var a=sub*t.pct/100; taxes+=a;
      tl+='<div class="bk-line"><span>'+t.label+' <small>'+(t.sample?'(sample '+t.pct+'%)':'')+'</small></span><span>'+BOOK.money(a)+'</span></div>';
    } else {
      tl+='<div class="bk-line"><span>'+t.label+'</span><span>'+(t.flat?BOOK.money(t.flat):'$0')+'</span></div>';
      if(t.note) tl+='<div class="bk-line"><small>'+t.note+'</small></div>';
    }
  });
  document.getElementById('railTaxes').innerHTML=tl;
  document.getElementById('railTotal').textContent=sub?BOOK.money(sub+taxes):'—';
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
        <p style="margin-top:20px"><a class="bk-btn" href="/stay/sol-modern">See your property &nbsp;&rarr;</a>
        <a class="bk-btn-g" href="/" style="margin-left:10px">Back to Sentral.com</a></p>
      </div></div>
    </div>
    <aside class="bk-rail" aria-label="Stay summary">
      <h3 id="railProp"></h3>
      <div class="bk-rail-sub" id="railDates"></div>
      <div id="railLines"></div>
      <div class="bk-note">Sample stay for design review</div>
    </aside>
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), cur=BOOK.prop(q.property)||BOOK.PROPERTIES[0];
  var sel=BOOK.parseRooms(q.rooms), plan=BOOK.plan(q.plan), nights=BOOK.nights(q['in'],q.out)||1;
  document.getElementById('cfNum').textContent='SENT-'+(Date.now().toString(36).toUpperCase().slice(-6));
  document.getElementById('cfContext').textContent=cur.name+', '+cur.city;
  document.getElementById('cfMsg').textContent=(q.guest?q.guest+', your':'Your')+' suite at '+cur.name+' is set for '+BOOK.fmtDate(q['in'])+'. Check-in opens at 4:00 PM with keyless entry — your code arrives the morning of arrival.';
  document.getElementById('cfPhone').textContent=cur.phone||'(833) 370-4161';
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railDates').textContent=BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night')+' · '+plan.name;
  var lines='';
  cur.rooms.forEach(function(r){ var n=sel[r.slug]||0; if(n) lines+='<div class="bk-line"><span>'+n+' × '+r.name+'</span><span>'+BOOK.money(r.from*plan.mult*n*nights)+'</span></div>'; });
  document.getElementById('railLines').innerHTML=lines||'<div class="bk-line"><small>Sample stay</small></div>';
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
  <div class="bk-props" id="ctProps"></div>
</div>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var q=BOOK.q(), c=BOOK.CITIES[q.city];
  if(!c){ location.replace('/book/search?'+BOOK.qs({})); return; }
  var nights=BOOK.nights(q['in'],q.out);
  document.getElementById('cityH').innerHTML=c.name+'. <em>Choose your Sentral.</em>';
  document.getElementById('ctContext').textContent=c.props.length+' properties'+(nights?' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · dates carry through':'');
  var IMGS=['/assets/ig-social-1.jpg','/assets/ig-social-2.jpg','/assets/ig-social-3.jpg'];
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

for fname,(title,body) in PAGES.items():
    open(os.path.join(ROOT,fname),'w').write(page(title,body))
    print('wrote',fname)
