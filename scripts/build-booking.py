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
      '<link rel="stylesheet" href="/booking.css?v=7">\n'
      '<script src="/assets/booking-demo.js?v=4" defer></script>\n'
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
SROOMS=[
 ('studio','Studio','Sleeps 2 · 1 Queen Bed · 1 Bath · 517 Sq Ft',189,4,'/assets/bk-room-studio.jpg',['/assets/bk-room-1br.jpg','/assets/bk-city-1.jpg','/assets/bk-city-2.jpg']),
 ('one-bedroom','One Bedroom','Sleeps 2 · 1 Queen Bed · 1 Bath · 673 Sq Ft',229,7,'/assets/bk-room-1br.jpg',['/assets/bk-room-studio.jpg','/assets/bk-city-2.jpg','/assets/bk-city-3.jpg']),
 ('two-bedroom','Two Bedroom','Sleeps 4 · 2 Queen Beds · 2 Baths · 1,053 Sq Ft',319,2,'/assets/bk-room-2br.jpg',['/assets/bk-city-1.jpg','/assets/bk-city-3.jpg','/assets/bk-room-studio.jpg'])]
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
def _card(slug,name,spec,base,left,img,thumbs):
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
      '<div class="bk-room2-media"><img class="bk-room2-img" src="'+img+'" alt="'+name+' suite">'
      '<div class="bk-thumbs">'+''.join('<img src="'+t+'" alt="" loading="lazy">' for t in thumbs)+'</div></div>'
      '<div class="bk-room2-mid"><div class="bk-room-name">'+name+'</div>'
      '<div class="bk-specs">'+_specspans(spec)+'</div>'
      '<div class="bk-room-links"><a href="/book/room?property=sol-modern&type='+slug+'">More details &nbsp;&rarr;</a></div>'
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
      var slug=bk.getAttribute('data-book'), all={};
      for(var s in stay) all[s]=stay[s];
      all[slug]=state(slug);                          // add / replace this suite in the stay
      location.href='/book/checkout?'+BOOK.qs({property:cur.slug,city:null,rooms:BOOK.roomsParam(all)});
    }
  });
  document.getElementById('bkSort').addEventListener('change',function(){
    var dir=this.value==='desc'?-1:1;
    [].slice.call(res.children)
      .sort(function(a,b){ return dir*((+a.getAttribute('data-base'))-(+b.getAttribute('data-base'))); })
      .forEach(function(c){ res.appendChild(c); });
  });
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
        <img class="bk-room-img" id="rmImg" style="height:320px;width:100%" src="/assets/bk-room-studio.jpg" alt="Suite living area">
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
  var IMGS={'studio':'/assets/bk-room-studio.jpg','one-bedroom':'/assets/bk-room-1br.jpg','two-bedroom':'/assets/bk-room-2br.jpg'};
  document.getElementById('rmImg').src=IMGS[r.slug]||IMGS.studio;
  document.getElementById('rmName').textContent=r.name;
  document.getElementById('rmSpecs').textContent=r.specs;
  document.getElementById('rmDesc').textContent='Furnished end to end — full kitchen, in-unit washer and dryer, dedicated workspace, and a real bedroom door. Sample copy; per-suite copy is a [FIELD].';
  document.getElementById('rmContext').textContent=cur.name+', '+cur.city+(nights? ' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night'):'');
  document.getElementById('rmBack').href='/book/search?'+BOOK.qs({type:null,plan:null});
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railDates').textContent=nights? BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night'):'Choose dates on the previous step';
  document.getElementById('rmPlans').innerHTML = BOOK.PLANS.map(function(pl){
    var nightly=BOOK.planPrice(r,pl);
    var total=nights? ' · '+BOOK.money(nightly*nights)+' total' : '';
    return '<div class="bk-plan"><div>'+
      '<div class="bk-plan-name">'+pl.name+'</div>'+
      '<div class="bk-plan-note">'+pl.note+'</div></div>'+
      '<div style="display:flex;align-items:center;gap:18px">'+
      '<span class="bk-plan-price"><s style="color:#9a948e;font-size:.9375rem">'+BOOK.money(r.from)+'</s> '+BOOK.money(nightly)+'<span class="bk-price-l" style="display:block;text-align:right">sample · avg / night'+total+'</span></span>'+
      '<a class="bk-btn" href="/book/checkout?'+BOOK.qs({property:cur.slug,rooms:r.slug+':1:'+pl.slug,type:null,plan:null})+'">Select &nbsp;&rarr;</a>'+
      '</div></div>';
  }).join('');
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
header('Sentral &mdash; Book a Stay','Almost <em>home.</em>','ckContext',1)+'''
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
  var sel=BOOK.parseRooms(q.rooms), nights=BOOK.nights(q['in'],q.out)||1;
  var ad=+q.adults||2, ch=+q.children||0;
  document.getElementById('ckContext').textContent=cur.name+', '+cur.city+' · '+BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out);
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railAddr').textContent=cur.address||(cur.city+', '+cur.state);
  // Suites — text only (no photo), each with its rate plan + Modify
  var back='/book/search?'+BOOK.qs({}), rooms='', sub=0, count=0;
  cur.rooms.forEach(function(r){
    var st=sel[r.slug]; if(!st||!st.n) return;
    var pl=BOOK.plan(st.plan), nightly=BOOK.planPrice(r,pl); sub+=nightly*st.n*nights; count+=st.n;
    rooms+='<div class="bk-suite"><div><b>'+(st.n>1?st.n+' × ':'')+r.name+'</b><small>'+pl.name+'</small></div>'+
      '<a href="'+back+'">Modify</a></div>';
  });
  if(!count) rooms='<div class="bk-line"><small>No suites selected — start from Suites &amp; Availability.</small></div>';
  rooms+='<a class="bk-addroom" href="'+back+'">+ Add another suite</a>';
  document.getElementById('railRooms').innerHTML=rooms;
  function fact(k,v){ return '<div><dt>'+k+'</dt><dd>'+v+'</dd></div>'; }
  document.getElementById('railFacts').innerHTML=
    fact('Check-in',BOOK.fmtDate(q['in'])+'<small>4:00 PM</small>')+
    fact('Check-out',BOOK.fmtDate(q.out)+'<small>11:00 AM</small>')+
    fact('Nights',nights)+
    fact('Guests',ad+(ad>1?' adults':' adult')+', '+ch+(ch===1?' child':' children'))+
    (count>1?fact('Rooms',count):'');
  // Price breakdown — rate total (incl. select fees) + property tax lines
  var lines='', total=sub;
  if(sub){
    lines+='<div class="bk-line"><span>Nightly total <small>'+nights+(nights>1?' nights':' night')+'</small></span><span>'+BOOK.money(sub)+'</span></div>';
    lines+='<div class="bk-line"><small>Includes <button type="button" class="bk-fees-link" data-fees>Select Fees</button></small></div>';
    BOOK.TAXES.forEach(function(t){
      var a=t.pct!=null? sub*t.pct/100 : (t.flat||0)*nights*count; total+=a;
      lines+='<div class="bk-line"><span>'+t.label+(t.sample?' <small>(sample '+(t.pct!=null?t.pct+'%':'')+')</small>':'')+'</span><span>'+BOOK.money(a)+'</span></div>';
    });
    if(q.promo) lines+='<div class="bk-line"><span>Discount code <small>'+q.promo.toUpperCase()+'</small></span><span><small>validated by StayNTouch at build</small></span></div>';
  }
  document.getElementById('railLines').innerHTML=lines;
  document.getElementById('railTotal').textContent=sub?BOOK.money(total):'—';
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
  var sel=BOOK.parseRooms(q.rooms), nights=BOOK.nights(q['in'],q.out)||1;
  document.getElementById('cfNum').textContent='SENT-'+(Date.now().toString(36).toUpperCase().slice(-6));
  document.getElementById('cfContext').textContent=cur.name+', '+cur.city;
  document.getElementById('cfMsg').textContent=(q.guest?q.guest+', your':'Your')+' suite at '+cur.name+' is set for '+BOOK.fmtDate(q['in'])+'. Check-in opens at 4:00 PM with keyless entry — your code arrives the morning of arrival.';
  document.getElementById('cfPhone').textContent=cur.phone||'(833) 370-4161';
  document.getElementById('railProp').textContent=cur.name+', '+cur.city;
  document.getElementById('railDates').textContent=BOOK.fmtDate(q['in'])+' → '+BOOK.fmtDate(q.out)+' · '+nights+(nights>1?' nights':' night');
  var lines='';
  cur.rooms.forEach(function(r){ var st=sel[r.slug]; if(st&&st.n){ var pl=BOOK.plan(st.plan); lines+='<div class="bk-line"><span>'+st.n+' × '+r.name+' <small>'+(pl.short||pl.name)+'</small></span><span>'+BOOK.money(BOOK.planPrice(r,pl)*st.n*nights)+'</span></div>'; } });
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
  <form class="bk-editbar" id="ctEdit">
    <div class="bk-f"><label for="ctIn">Check-in</label><input id="ctIn" type="date"></div>
    <div class="bk-f"><label for="ctOut">Check-out</label><input id="ctOut" type="date"></div>
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
  document.getElementById('ctEdit').addEventListener('submit',function(e){
    e.preventDefault();
    location.search='?'+BOOK.qs({city:q.city,
      'in':document.getElementById('ctIn').value, out:document.getElementById('ctOut').value,
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
 'charlotte':   ('Charlotte',   [('inkwell','Inkwell','Charlotte, NC','','NoDa',_LINE,_AM),
                                 ('joinery-north','Joinery North','Charlotte, NC','','Optimist Park',_LINE,_AM),
                                 ('joinery-west','Joinery West','Charlotte, NC','','Optimist Park',_LINE,_AM)]),
 'austin':      ('Austin',      [('sentral-east-austin-1630','Sentral East Austin 1630','Austin, TX',' · 30+ nights','East Austin',_LINE,_AM),
                                 ('sentral-east-austin-1614','Sentral East Austin 1614','Austin, TX','','East Austin',_LINE,_AM)]),
 'los-angeles': ('Los Angeles', [('sentral-dtla-755','Sentral DTLA 755','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM),
                                 ('sentral-dtla-732','Sentral DTLA 732','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM),
                                 ('figueroa-eight','Figueroa Eight','Los Angeles, CA',' · 31+ nights','Downtown LA',_LINE,_AM)]),
 'miami':       ('Miami',       [('alea','Alea','Miami, FL','','[FIELD] Neighborhood',_LINE,_AM),
                                 ('sentral-wynwood','Sentral Wynwood','Miami, FL','','Wynwood',_LINE,_AM)]),
}
# Property pages: only the Sol Modern template is built so far, so every VIEW
# PROPERTY lands on it for review. PRODUCTION: /stay/{property-slug}.
PROP_PAGE={'sol-modern':'/stay/sol-modern'}
PIN='<svg class="bk-pin" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M12 22s7-6.4 7-12a7 7 0 0 0-14 0c0 5.6 7 12 7 12z" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
IMGS=['/assets/bk-city-1.jpg','/assets/bk-city-2.jpg','/assets/bk-city-3.jpg']
for cslug,(cname,props) in CITY_DATA.items():
    cards='\n'.join(
        '    <div class="bk-prop" data-prop="'+ps+'">\n'
        '      <img class="bk-prop-img" src="'+IMGS[i%3]+'" alt="'+pn+'">\n'
        '      <div class="bk-prop-body"><div class="bk-prop-name">'+pn+'</div>\n'
        '      <div class="bk-prop-meta">'+meta+note+'</div>\n'
        '      <div class="bk-prop-hood">'+PIN+'<span>'+hood+'</span></div>\n'
        '      <p class="bk-prop-line">'+line+'</p>\n'
        '      <details class="bk-prop-am"><summary>Amenities</summary><ul>'+''.join('<li>'+a+'</li>' for a in am)+'</ul></details>\n'
        '      <div class="bk-prop-ctas"><a class="bk-prop-cta" data-avail href="/book/search?property='+ps+'">Check availability &nbsp;&rarr;</a>'
        '<a class="bk-prop-cta ghost" href="'+PROP_PAGE.get(ps,'/stay/sol-modern')+'">View property &nbsp;&rarr;</a></div></div>\n'
        '    </div>' for i,(ps,pn,meta,note,hood,line,am) in enumerate(props))
    body=(header('Sentral &mdash; Book a Stay',cname+'. <em>Choose your Sentral.</em>','ctContext')
      +'\n'+RIBBON+'''
<div class="bk-wrap">
  <form class="bk-editbar" id="ctEdit">
    <div class="bk-f"><label for="ctIn">Check-in</label><input id="ctIn" type="date"></div>
    <div class="bk-f"><label for="ctOut">Check-out</label><input id="ctOut" type="date"></div>
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
  [].forEach.call(document.querySelectorAll('.bk-prop'),function(c){
    c.querySelector('[data-avail]').href='/book/search?'+BOOK.qs({property:c.getAttribute('data-prop'),city:null});
  });
  document.getElementById('ctEdit').addEventListener('submit',function(e){
    e.preventDefault();
    location.search='?'+BOOK.qs({
      'in':document.getElementById('ctIn').value, out:document.getElementById('ctOut').value,
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

# — search: suite cards + property options + rail defaults —
cards=''.join(
 '<div class="bk-card"><div class="bk-room">'
 '<img class="bk-room-img" src="'+RIMG[slug]+'" alt="'+name+' suite">'
 '<div class="bk-room-mid">'
 '<div class="bk-room-name">'+name+'</div>'
 '<div class="bk-specs">'+spec_spans(spec)+'</div>'
 '<div class="bk-room-links"><a href="/book/room?property=sol-modern&type='+slug+'">Rates &amp; suite details &nbsp;&rarr;</a></div>'
 '</div>'
 '<div class="bk-room-side">'
 '<span class="bk-price-n">'+money(rate)+'</span><span class="bk-price-l">Sample &middot; from / night</span>'
 '<div class="bk-step-ctl"><span class="lbl">Rooms</span>'
 '<button type="button" data-dec="'+slug+'" aria-label="Remove a '+name+'"><span aria-hidden="true">&minus;</span></button>'
 '<span class="n" id="n-'+slug+'">0</span>'
 '<button type="button" data-inc="'+slug+'" aria-label="Add a '+name+'"><span aria-hidden="true">+</span></button>'
 '</div></div>'
 '</div></div>' for slug,name,spec,rate in ROOMS_PY)
options=''.join('<option value="'+s+'">'+l+'</option>' for s,l in PROPS_PY)
# book-search: cards/options/rail baked directly in its body (10-2 redesign)

# — room: studio detail + plan rows —
plan_rows=''.join(
 '<div class="bk-plan"><div>'
 '<div class="bk-plan-name">'+pname+'</div>'
 '<div class="bk-plan-note">'+note+'</div></div>'
 '<div style="display:flex;align-items:center;gap:18px">'
 '<span class="bk-plan-price"><s style="color:#9a948e;font-size:.9375rem">'+money(189)+'</s> '+money(round(189*mult))+'<span class="bk-price-l" style="display:block;text-align:right">sample &middot; avg / night</span></span>'
 '<a class="bk-btn" href="/book/checkout?property=sol-modern&rooms=studio:1:'+pslug+'">Select &nbsp;&rarr;</a>'
 '</div></div>' for pslug,pname,note,mult in PLANS_PY)
bake('book-room.html',[
 ('<div class="bk-room-name" id="rmName" style="font-size:1.6rem"></div>','<div class="bk-room-name" id="rmName" style="font-size:1.6rem">Studio</div>'),
 ('<div class="bk-specs" id="rmSpecs"></div>','<div class="bk-specs" id="rmSpecs">'+ROOMS_PY[0][2]+'</div>'),
 ('id="rmDesc"></p>','id="rmDesc">Furnished end to end &mdash; full kitchen, in-unit washer and dryer, dedicated workspace, and a real bedroom door. Sample copy; per-suite copy is a [FIELD].</p>'),
 ('<div id="rmPlans"></div>','<div id="rmPlans">'+plan_rows+'</div>'),
 ('<h3 id="railProp"></h3>','<h3 id="railProp">Sol Modern, Phoenix</h3>'),
 ('<div class="bk-rail-sub" id="railDates"></div>','<div class="bk-rail-sub" id="railDates">Choose dates on the previous step</div>'),
])

# — checkout: representative sample stay (1 × One Bedroom, Fall Sale, 3 nights, 2 adults) —
sub=183*3; ctax=round(sub*0.06); stax=round(sub*0.065)
bake('book-checkout.html',[
 ('<h3 id="railProp"></h3>','<h3 id="railProp">Sol Modern, Phoenix</h3>'),
 ('<div class="bk-rail-sub" id="railAddr"></div>','<div class="bk-rail-sub" id="railAddr">50 E. Fillmore Street, Phoenix, AZ 85004</div>'),
 ('<div id="railRooms"></div>','<div id="railRooms"><div class="bk-suite"><div><b>One Bedroom</b><small>Limited Time Fall Sale | Stay 2+ Nights &amp; Save up to 20%</small></div><a href="/book/search">Modify</a></div><a class="bk-addroom" href="/book/search">+ Add another suite</a></div>'),
 ('<dl class="bk-facts" id="railFacts"></dl>','<dl class="bk-facts" id="railFacts"><div><dt>Check-in</dt><dd>Sample date<small>4:00 PM</small></dd></div><div><dt>Check-out</dt><dd>Sample date<small>11:00 AM</small></dd></div><div><dt>Nights</dt><dd>3</dd></div><div><dt>Guests</dt><dd>2 adults, 0 children</dd></div></dl>'),
 ('<div id="railLines"></div>','<div id="railLines"><div class="bk-line"><span>Nightly total <small>3 nights</small></span><span>'+money(sub)+'</span></div><div class="bk-line"><small>Includes <button type="button" class="bk-fees-link" data-fees>Select Fees</button></small></div><div class="bk-line"><span>City tax <small>(sample 6%)</small></span><span>'+money(ctax)+'</span></div><div class="bk-line"><span>State tax <small>(sample 6.5%)</small></span><span>'+money(stax)+'</span></div></div>'),
 ('<span id="railTotal">&mdash;</span>','<span id="railTotal">'+money(sub+ctax+stax)+'</span>'),
])

# — confirmation: sample number + summary —
bake('book-confirm.html',[
 ('<div class="bk-confirm-n" id="cfNum">SENTRAL-DEMO</div>','<div class="bk-confirm-n" id="cfNum">SENT-SAMPLE</div>'),
 ('<p style="font-size:.9375rem;color:#4a4643;max-width:60ch" id="cfMsg"></p>','<p style="font-size:.9375rem;color:#4a4643;max-width:60ch" id="cfMsg">Your suite at Sol Modern is set. Check-in opens at 4:00 PM with keyless entry &mdash; your code arrives the morning of arrival.</p>'),
 ('<strong id="cfPhone"></strong>','<strong id="cfPhone">(833) 370-4161</strong>'),
 ('<h3 id="railProp"></h3>','<h3 id="railProp">Sol Modern, Phoenix</h3>'),
 ('<div class="bk-rail-sub" id="railDates"></div>','<div class="bk-rail-sub" id="railDates">Sample stay &middot; 3 nights</div>'),
 ('<div id="railLines"></div>','<div id="railLines"><div class="bk-line"><span>1 &times; One Bedroom <small>Fall Sale</small></span><span>'+money(183*3)+'</span></div></div>'),
])
