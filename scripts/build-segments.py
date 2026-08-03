#!/usr/bin/env python3
"""
Segment landing page generator — Sentral group-business split.

Generates business-travel.html / group-travel.html / corporate-housing.html
from ONE shared template + per-segment config objects (below). This script is
the static-site equivalent of the brief's `/[segment]` shared component set:
no page markup is hand-authored per segment — edit a config, re-run, commit.

Run from repo root:  python3 scripts/build-segments.py
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'scripts', 'segment-partials')

def part(name):
    return open(os.path.join(P, name)).read()

# ─────────────────────────────────────────────────────────────────────────────
# SEGMENT CONFIGS  (mirrors the brief's `type Segment`)
# Copy marked PLACEHOLDER gates launch, not build.
# ─────────────────────────────────────────────────────────────────────────────
SEGMENTS = [
 dict(
  slug='business-travel',
  navLabel='Business Travel &amp; Corporate Housing',
  title='Business Travel &amp; Corporate Housing — Sentral',
  hero=dict(
    eyebrow='Sentral — Business Travel &amp; Corporate Housing',
    headlineLines=['Elevated stays for', 'the modern', 'professional.'],
    body='Solo travelers, project teams, executives, and relocating employees who expect more than a hotel room. Furnished suites and fully managed 30+ night corporate placements in the country&rsquo;s top business destinations — for a night, a quarter, or a year.',
    media=dict(src='/assets/sol-modern-stay-header.mp4', poster='/assets/stay-hero-poster.jpg', tagName='Sol Modern', tagCity='Phoenix, AZ'),
  ),
  rfp=dict(
    thirdFieldType='travelers',
    thirdFieldLabel='Number of travelers',
    thirdFieldOptions=None,  # open integer, no minimum
    occasionOptions=['Recurring travel program','Project-based travel','Single traveler','Event or conference','Relocation','Extended assignment','Executive placement'],
    lengthOfStayOptions=['1 – 29 nights','30 – 60 nights','61 – 90 nights','91 – 180 nights','180+ nights'],
    submitLabel='Start My Inquiry',
    leadSource='web-business-travel',
  ),
  whyUs=dict(
    eyebrow='Why Sentral for Business Travel',
    headlineLines=['Consistency in', 'every market you', 'operate in.'],
    body=[
      'Business travel breaks down when every city means a different property, a different standard, and a different point of contact. Sentral runs its communities on one operating platform — the suite your team checks into in Nashville works exactly like the one in Denver, down to the in-unit laundry and the coffee.',
      'We work directly with travel managers, TMCs, and RMCs: preferred corporate rates, direct billing, consolidated invoicing, and a single account contact across every market. No minimums, no thresholds — one traveler is a program.',
      'And for 30+ night placements, traditional corporate housing hands your employee a lease, a furniture vendor, and a utilities checklist — Sentral hands them keys. Furniture, kitchenware, linens, WiFi, and utilities already running: one rate, one invoice, nothing to set up or return.',
    ],
    image=dict(src='/assets/group-hero-poster.jpg', alt='Forme Houston at night', tagName='Forme', tagCity='Houston, TX'),
    imagePosition='right',
  ),
  detail=[dict(
    eyebrow='01 — Business Travel',
    headlineLines=['A simplified approach', 'to business travel.'],
    kicker='Purpose-built for the way work travels now.',
    subhead='Furnished apartment suites with hotel-caliber service — turnkey accommodations in top business destinations.',
    body='Hotels were built for two-night stays; your travelers increasingly stay two weeks. Sentral suites give them a full kitchen, in-unit laundry, real workspace, and separation between where they sleep and where they take calls — at rates that outperform extended-stay hotels as trips get longer. Whether you&rsquo;re booking one consultant on a recurring route, rotating project crews through a market, or placing an executive for a quarter, the experience is the same: seamless digital check-in, a 24/7 on-site hospitality team, and amenity spaces that make travel feel less like travel. Stay a few nights, a few months, or longer — the suite is ready when your traveler lands, and the invoice arrives the way your finance team wants it.',
    bullets=[
      'Turnkey furnished suites with full kitchens and in-unit laundry',
      'Seamless check-in and 24/7 on-site hospitality team',
      'Co-working stations and elevated amenity spaces',
      'Pet-friendly with flexible term stays',
      'Preferred corporate partnership rates and direct billing',
    ],
    image=dict(src='/assets/ig-social-2.jpg', alt='Rooftop pool at a Sentral community', tagName='Sentral Community — TBC', tagCity='City TBC'),
    imagePosition='left',
  ),
  dict(
    eyebrow='02 — Corporate Housing',
    headlineLines=['The home-away-from-home', 'for your team.'],
    kicker='Placements that feel like moving up, not moving out.',
    subhead='Premium furnished residences for relocating employees, project teams, and extended assignments — 30+ nights, fully managed.',
    body='A relocation is a vulnerable moment: new city, new role, and — too often — a beige apartment with rented furniture. Sentral placements put your people in the same residences our long-term residents choose, inside communities with real hospitality teams, fitness centers, coworking lounges, and programming that makes a new city feel navigable by the second week. Stays start at 30 nights and flex to whatever the assignment needs — extend, shorten, or move markets without renegotiating from scratch. Multi-unit blocks keep project teams together on shared floors; centralized operating standards mean the Denver placement and the Nashville placement are the same placement. And because we operate every building ourselves, your account contact and the on-site team work for the same company: no vendor chains, no finger-pointing, no surprises on the invoice.',
    bullets=[
      'Class A communities with centralized operating standards',
      'Move-in ready — full kitchens, linens, everything included',
      'Flexible 30+ night stays structured for corporate placements',
      'Multi-unit group block capability for team housing',
      'One invoice — furniture, utilities, WiFi, and housekeeping options included',
    ],
    image=dict(src='/assets/ig-social-3.jpg', alt='Resident walking a dog at a Sentral community', tagName='Sentral Community — TBC', tagCity='City TBC'),
    imagePosition='right',
  )],
  logoWall=dict(enabled=True, heading='Trusted by travel &amp; housing programs nationwide',
    logos=['Global Consulting Firm','Fortune 100 Technology Co.','Enterprise TMC Partner','Relocation Management Co.','Global Engineering Firm','National Healthcare System']),
  testimonials=[  # PLACEHOLDER quotes — marketing to source real ones
    dict(quote='Our consultants stopped asking for hotel alternatives — they ask which cities have a Sentral. Same suite standard in every market, one invoice at the end of the month.',
         name='Placeholder', title='Director of Travel', company='national consulting firm'),
    dict(quote='Our relocating hires used to spend their first month fighting utility companies. Now they land, get keys, and start work. Retention on relocations is up.',
         name='Placeholder', title='Global Mobility Manager', company='Fortune 500 employer'),
  ],
  occasionsGrid=False,
  faq=[
    dict(q='Is there a minimum number of travelers or rooms?',
         a='No. Business travel programs start at a single traveler. Whether you have one consultant on a recurring route or a rotating bench of hundreds, the same rates, billing, and support apply.'),
    dict(q='How does billing work for corporate accounts?',
         a='We offer direct billing with consolidated monthly invoicing across all markets and stays, mapped to your cost centers. Individual travelers can also pay by card with folios delivered automatically.'),
    dict(q='Can we book through our TMC or GDS?',
         a='We work alongside TMCs and relocation management companies today, and can operate within your existing approval workflows. Talk to us about your program&rsquo;s booking path — we&rsquo;ll meet it where it is.'),
    dict(q='What&rsquo;s included in the suite?',
         a='Every suite is fully furnished with a complete kitchen, kitchenware, linens, towels, in-unit or on-site laundry, high-speed WiFi, and streaming-ready TVs. Utilities are included — one rate, no setup.'),
    dict(q='How fast can a traveler check in after booking?',
         a='Suites are move-in ready. With digital check-in and 24/7 on-site teams, same-week arrivals are routine, and same-day is often possible depending on the market.'),
    dict(q='How do 30+ night corporate housing placements work?',
         a='Stays of 30 nights or more are structured as fully managed corporate placements — furniture, utilities, WiFi, and amenities included on one invoice. Under 30 nights, the same suites are available on nightly business-travel terms, so there&rsquo;s no gap between the two programs.'),
    dict(q='Can placements be extended or shortened mid-assignment?',
         a='Yes. Assignments change; your placements flex with them. Extensions, early departures, and market transfers are handled by your account contact without restarting paperwork.'),
    dict(q='Are the residences pet-friendly?',
         a='Yes. Pets are welcome across Sentral communities — because a three-month assignment shouldn&rsquo;t mean boarding the dog.'),
  ],
 ),
 dict(
  slug='group-travel',
  navLabel='Group Travel',
  title='Group Travel &amp; Room Blocks — Sentral',
  hero=dict(
    eyebrow='Sentral — Groups &amp; Room Blocks',
    headlineLines=['Six rooms to', 'full buyouts —', 'handled beautifully.'],
    body='Wedding weekends, team off-sites, sports travel, reunions. Our group sales team handles every detail, from block management to VIP check-in.',
    media=dict(src='/assets/forme-houston-group-header.mp4', poster='/assets/group-hero-poster.jpg', tagName='Forme', tagCity='Houston, TX'),
  ),
  rfp=dict(
    thirdFieldType='rooms',
    thirdFieldLabel='Rooms needed',
    thirdFieldOptions=['6 – 10','11 – 25','26 – 50','51+'],
    occasionOptions=['Wedding','Team off-site','Sports team','Reunion','Other'],
    submitLabel='Submit RFP',
    leadSource='web-group-travel',
  ),
  whyUs=dict(
    eyebrow='Why Sentral for Groups',
    headlineLines=['Your whole group,', 'under one roof —', 'and one contact.'],
    body=[
      'Group travel usually means a spreadsheet, a hotel block that half your guests book wrong, and a front desk that has never heard of you. Sentral assigns a dedicated group sales manager to every booking — one person who owns your block from first hold to final checkout.',
      'And because our communities are residential buildings with hospitality teams, your group actually gets to be together: shared floors, gathering spaces, terraces and lounges you can reserve, and suites where families and crews spread out instead of splitting across doubles.',
    ],
    image=dict(src='/assets/ig-social-1.jpg', alt='Residents socializing over billiards', tagName='Sentral Community — TBC', tagCity='City TBC'),
    imagePosition='right',
  ),
  detail=dict(
    eyebrow='02 — Groups &amp; Room Blocks',
    headlineLines=['Sentral has your', 'room blocks covered.'],
    kicker='From six rooms to the whole building.',
    subhead='Communities designed to bring people together in a more relaxed, elevated setting.',
    body='From intimate conference rooms to expansive outdoor terraces, fire pits, and rooftop lounges — Sentral communities are built for gathering. Your block lives in real apartments: full kitchens for the morning-of, living rooms for the night-before, and space for the people who make your event an event. Our group sales team manages every detail — block holds and release dates, rooming lists, staggered arrivals, welcome amenities in every suite, and on-site coordination the day your group lands. Whether it&rsquo;s a wedding weekend taking over a floor, a sports franchise on a road series, or a company off-site that needs breakout space by day and a rooftop by night, you get one contact, one contract, and a team that treats your group like the main event.',
    bullets=[
      'Dedicated group sales manager for every booking',
      'Flexible block sizes — 6 rooms to full-building buyouts',
      'Meeting spaces, terraces, and event-ready lounges',
      'Custom arrival experiences and amenity activations',
    ],
    image=dict(src='/assets/forme-houston-square-poster.jpg', alt='Evening pool deck at Forme Houston', tagName='Forme', tagCity='Houston, TX'),
    imagePosition='left',
  ),
  logoWall=dict(enabled=False, heading='', logos=[]),
  testimonials=[  # PLACEHOLDER quotes — marketing to source real ones
    dict(quote='We took forty rooms for a wedding weekend and it felt like we had the building to ourselves. One rooming list, one contact, zero guests calling me confused.',
         name='Placeholder', title='Mother of the bride', company='Nashville wedding block'),
    dict(quote='Our team stays together on every road trip now — same building, shared floor, film room in the resident lounge. The block process is the easiest in our league.',
         name='Placeholder', title='Director of Team Operations', company='professional sports franchise'),
  ],
  occasionsGrid=True,
  faq=[
    dict(q='What&rsquo;s the minimum block size?',
         a='Group blocks start at six rooms and scale to full-building buyouts. Under six rooms? Book direct on our Stay page — every guest still gets the same suites and service.'),
    dict(q='How do block holds and release dates work?',
         a='Your group sales manager sets a courtesy hold with an agreed release date. Unclaimed rooms release back without penalty on courtesy blocks; contracted blocks are structured to your event&rsquo;s needs.'),
    dict(q='Can guests book into the block themselves?',
         a='Yes — we set up a dedicated booking link or code for your group so guests reserve their own suites inside your block, and your rooming list updates automatically.'),
    dict(q='Do you host events on site?',
         a='Many communities have reservable lounges, terraces, and dining spaces for welcome parties, watch parties, and morning-afters. Your group sales manager will match spaces to your run of show.'),
    dict(q='Can you handle staggered arrivals and departures?',
         a='Yes. Blocks routinely span different arrival dates, stay lengths, and suite types — we manage the matrix so you don&rsquo;t have to.'),
  ],
 ),
]

# ─────────────────────────────────────────────────────────────────────────────
# SHARED RENDERING
# ─────────────────────────────────────────────────────────────────────────────
BASE_CSS   = part('base-style.css')
LATE_CSS   = part('late-style.css')
NAV        = part('nav.html')
FOOTER     = part('footer.html')
AWARDS     = part('awards.html')
OCCASIONS  = part('occasions.html')
GDIR       = part('gdir.html')
NAV_JS     = part('nav.js')

# destinations sentence per segment (brief: no six-room language on BT/CH)
GDIR_SENTENCE = 'Individual business travelers may search for dates and book direct. For groups of six or more, get your RFP started today.'
GDIR_VARIANTS = {
  'business-travel': 'From a single traveler to a fully managed 30+ night placement &mdash; every Sentral destination below is ready for your program.',
  'group-travel': GDIR_SENTENCE,
}

SEG_CSS = """
/* ══ SEGMENT PAGES (generated) ══ */
/* readability (owner 2026-07-22): bright hero copy + labels, darker light-surface metas */
.hero .hero-sub{color:rgba(255,255,255,.88) !important;font-size:1.02rem !important;line-height:1.7 !important}
.hero .hero-eyebrow{color:var(--oat,#F2E8D5) !important;font-size:.78rem !important}
.rfp-mini-label{color:rgba(255,255,255,.82) !important;font-size:.75rem !important}
.rfp-mini-note{color:rgba(255,255,255,.6) !important;font-size:.75rem !important}
.hero-rfp-card{background:rgba(14,12,10,.94) !important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.hero-rfp-title{font-size:.9rem !important;color:var(--white) !important}
.rfp-mini-input{font-size:1rem !important;color:var(--white) !important;background:rgba(255,255,255,.1) !important}
.rfp-mini-note{color:rgba(255,255,255,.65) !important}
.seg-quote-title{color:rgba(255,255,255,.75) !important;font-size:.9rem}
.seg-logo{color:#6B6560}
.seg-logos-note{color:#6B6560}
.sticky-group,.sp-sticky{display:none !important}
.seg-subnav{position:sticky;top:64px;z-index:150;background:var(--black);border-bottom:1px solid var(--ruleW,rgba(255,255,255,.12));display:flex;justify-content:center;gap:8px;padding:0 24px}
.seg-subnav a{display:block;padding:16px 22px;font-size:.85rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.72);text-decoration:none;border-bottom:2px solid transparent;white-space:nowrap;transition:color .2s,border-color .2s}
.seg-subnav a:hover{color:var(--white)}
.seg-subnav a.active{color:var(--white);border-color:var(--slate-light,#5C8CA0)}
.hero{margin-top:0}
.hero-h .l3, .hero-h em.l3{font-style:italic;color:var(--slate-light,#5C8CA0)}
.rfp-mini-input:invalid:focus{outline:1px solid #b46} .rfp-error{display:none;color:#e7a5a5;font-size:.75rem;margin-top:6px}
.rfp-thanks{display:none;color:var(--white);font-size:.95rem;line-height:1.7;padding:12px 0}
/* why / detail splits */
.seg-cta{display:inline-block;margin-top:24px;border:1px solid var(--black);padding:14px 28px;font-size:.8rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--black);text-decoration:none;transition:background .2s,color .2s,border-color .2s}
.seg-cta:hover{background:#3D6478;border-color:#3D6478;color:var(--white)}
.seg-split{background:var(--cream);padding:88px 0}
.seg-split-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.seg-split-img{position:relative;aspect-ratio:4/3;background-size:cover;background-position:center;width:100%}
.seg-split-copy{max-width:620px}
.seg-split-copy.pad-l{padding-left:64px}.seg-split-copy.pad-r{padding-right:64px;justify-self:end}
.seg-eyebrow{display:block;font-size:.78rem;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--slate-deep,#3D6478);margin-bottom:14px}
.seg-h{font-family:var(--serif);font-size:clamp(1.9rem,3.2vw,2.8rem);font-weight:300;color:var(--black);line-height:1.12;margin-bottom:18px}
.seg-h .l3, .seg-h em.l3{font-style:italic;color:var(--slate-deep,#3D6478)}
.seg-kicker{font-family:var(--serif);font-size:1.15rem;font-style:italic;color:var(--slate-deep,#3D6478);margin-bottom:10px}
.seg-subhead{font-size:1.02rem;font-weight:500;color:var(--black);margin-bottom:12px}
.seg-body{font-size:1rem;font-weight:300;color:#3A3633;line-height:1.75;margin-bottom:14px}
.seg-bullets{list-style:none;margin:18px 0 0;padding:0;display:flex;flex-direction:column;gap:10px}
.seg-bullets li{position:relative;padding-left:22px;font-size:.95rem;color:#3A3633}
.seg-bullets li::before{content:'';position:absolute;left:0;top:9px;width:10px;height:1.5px;background:var(--slate-deep,#3D6478)}
/* logo wall */
.seg-logos{background:var(--cream);padding:0 64px 88px}
.seg-logos-inner{max-width:1200px;margin:0 auto;text-align:center}
.seg-logos-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:2px;margin-top:28px}
.seg-logo{background:var(--white);padding:26px 18px;font-family:var(--serif);font-size:.95rem;color:#8a857e;display:flex;align-items:center;justify-content:center;text-align:center;filter:grayscale(1);transition:color .2s,filter .2s;min-height:84px}
.seg-logo:hover{color:var(--slate-deep,#3D6478);filter:none}
.seg-logos-note{margin-top:14px;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:#9a9490}
/* testimonials */
.seg-quotes{background:var(--black);padding:88px 64px}
.seg-quotes-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:56px}
.seg-quote-text{font-family:var(--serif);font-size:1.35rem;font-weight:300;font-style:italic;color:var(--white);line-height:1.5;margin-bottom:18px}
.seg-quote-text::before{content:'\\201C'}.seg-quote-text::after{content:'\\201D'}
.seg-quote-name{font-size:.9rem;font-weight:500;color:var(--white)}
.seg-quote-title{font-size:.82rem;color:rgba(255,255,255,.65);margin-top:2px}
/* faq */
.seg-faq{background:var(--cream);padding:88px 64px}
.seg-faq-inner{max-width:860px;margin:0 auto}
.seg-faq h2{margin-bottom:28px}
.seg-faq details{background:var(--white);border-top:2px solid var(--slate,#2D4A5C);margin-bottom:2px}
.seg-faq summary{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:20px 24px;cursor:pointer;list-style:none;font-size:1.05rem;font-weight:500;color:var(--black)}
.seg-faq summary::-webkit-details-marker{display:none}
.seg-faq summary::after{content:'';width:9px;height:9px;border-right:1.5px solid #6B6560;border-bottom:1.5px solid #6B6560;transform:rotate(45deg);transition:transform .2s;flex-shrink:0}
.seg-faq details[open] summary::after{transform:rotate(-135deg)}
.seg-faq .a{padding:0 24px 20px;font-size:1rem;line-height:1.75;color:#3A3633;max-width:70ch}
/* closing cta */
.seg-close{background:var(--black);padding:88px 64px;text-align:center}
.seg-close h2{font-family:var(--serif);font-size:clamp(1.9rem,3.2vw,2.8rem);font-weight:300;color:var(--white);line-height:1.15;margin-bottom:12px}
.seg-close h2 em{font-style:italic;color:var(--slate-light,#5C8CA0)}
.seg-close p{color:rgba(255,255,255,.82);font-size:1rem;margin-bottom:26px}
.seg-close a{display:inline-block;background:var(--white);color:var(--black);padding:15px 34px;font-size:.8rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;border-radius:2px;transition:background .2s,color .2s}
.seg-close a:hover{background:#3D6478;color:var(--white)}
a.gdir-cta{display:inline-block;text-decoration:none;text-align:center}
@media(max-width:900px){
  .seg-subnav{gap:0;padding:0 8px;overflow-x:auto}
  .seg-split{padding:64px 0}
  .seg-split-inner{grid-template-columns:1fr;gap:32px}
  .seg-split-copy.pad-l,.seg-split-copy.pad-r{padding:0 24px;justify-self:start}
  .seg-quotes,.seg-faq,.seg-close,.seg-logos{padding-left:24px;padding-right:24px}
}
"""

FORM_JS = """
/* Segment RFP form + analytics (generated) */
window.dataLayer = window.dataLayer || [];
(function(){
  var SEG = document.body.getAttribute('data-segment');
  function track(ev, extra){ var p={event:ev, segment:SEG}; if(extra) for(var k in extra) p[k]=extra[k]; window.dataLayer.push(p); }
  track('page_view');
  // scroll depth 25/50/75/100
  var fired={};
  window.addEventListener('scroll', function(){
    var h=document.documentElement, d=(h.scrollTop+window.innerHeight)/h.scrollHeight*100;
    [25,50,75,100].forEach(function(m){ if(d>=m && !fired[m]){ fired[m]=1; track('scroll_depth',{depth:m}); }});
  }, {passive:true});
  // form
  var form=document.getElementById('rfp-form-el'); if(!form) return;
  var started=false;
  form.addEventListener('focusin', function(){ if(!started){ started=true; track('rfp_start'); } });
  form.addEventListener('invalid', function(){ track('rfp_validation_failure'); }, true);
  form.addEventListener('submit', function(e){
    e.preventDefault();
    track('rfp_submit_success',{leadSource:form.leadSource.value});
    /* RFP submissions email Contact@sentral.com (owner decision 7-31) — composed
       via mailto so the sender's own mail client carries their identity. */
    var segName = SEG==='group-travel' ? 'Group Travel' : 'Business Travel & Corporate Housing';
    var subject = encodeURIComponent('RFP — '+segName+' — '+(form.occasion.value||''));
    var lines = ['Occasion: '+form.occasion.value,
                 'Destination: '+form.destination.value,
                 'Check-in: '+form.checkin.value];
    if(form.travelers) lines.push('Number of travelers: '+form.travelers.value);
    if(form.rooms) lines.push('Rooms needed: '+form.rooms.value);
    if(form.lengthOfStay) lines.push('Length of stay: '+form.lengthOfStay.value);
    lines.push('Lead source: '+form.leadSource.value);
    var body = encodeURIComponent(lines.join('\\n'));
    window.location.href = 'mailto:Contact@sentral.com?subject='+subject+'&body='+body;
    form.style.display='none';
    document.getElementById('rfp-thanks').style.display='block';
  });
  // closing CTA click
  document.querySelectorAll('[data-track="closing_cta"]').forEach(function(el){
    el.addEventListener('click', function(){ track('closing_cta_click'); });
  });
})();
/* hero video toggle */
(function(){
  var v=document.getElementById('segHeroVideo'),btn=document.getElementById('segHeroToggle');
  if(!v||!btn)return;
  var iP='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.5l9 5.5-9 5.5z"/></svg>';
  var iA='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 2.5h3.2v11H3.5zM9.3 2.5h3.2v11H9.3z"/></svg>';
  var userPaused=false;
  function ui(p){btn.innerHTML=p?iA:iP;btn.setAttribute('aria-label',p?'Pause background video':'Play background video');}
  function go(){v.play().then(function(){ui(true)}).catch(function(){ui(false)});}
  go();
  btn.addEventListener('click',function(){if(v.paused){userPaused=false;go()}else{userPaused=true;v.pause();ui(false)}});
  v.addEventListener('playing',function(){ui(true)});v.addEventListener('pause',function(){ui(false)});
})();
"""

DEST_OPTIONS = """<option value="" disabled selected>Select a market&hellip;</option>
<option>Atlanta, GA</option><option>Austin, TX</option><option>Charlotte, NC</option>
<option>Chicago, IL</option><option>Denver, CO</option><option>Houston, TX</option>
<option>Las Vegas, NV</option><option>Miami, FL</option><option>Nashville, TN</option>
<option>Philadelphia, PA</option><option>Phoenix, AZ</option><option>Scottsdale, AZ</option>
<option>Multiple markets</option>"""

def photo_tag(name, city):
    return f'<div class="photo-tag"><span class="photo-tag-name">{name}</span><span class="photo-tag-city">{city}</span></div>'

def third_field(rfp):
    if rfp['thirdFieldType'] == 'travelers':
        return (f'<div class="rfp-mini-field"><label class="rfp-mini-label" for="rfp-third">{rfp["thirdFieldLabel"]}</label>'
                f'<input class="rfp-mini-input" id="rfp-third" name="travelers" type="number" min="1" step="1" required placeholder="e.g. 3"></div>')
    opts = ''.join(f'<option>{o}</option>' for o in rfp['thirdFieldOptions'])
    name = 'rooms' if rfp['thirdFieldType'] == 'rooms' else 'lengthOfStay'
    return (f'<div class="rfp-mini-field"><label class="rfp-mini-label" for="rfp-third">{rfp["thirdFieldLabel"]}</label>'
            f'<select class="rfp-mini-input rfp-mini-select" id="rfp-third" name="{name}" required>'
            f'<option value="" disabled selected>Select&hellip;</option>{opts}</select></div>')

def extra_field(rfp):
    if not rfp.get('lengthOfStayOptions'):
        return ''
    opts = ''.join(f'<option>{o}</option>' for o in rfp['lengthOfStayOptions'])
    return (f'<div class="rfp-mini-field"><label class="rfp-mini-label" for="rfp-los">Length of stay</label>'
            f'<select class="rfp-mini-input rfp-mini-select" id="rfp-los" name="lengthOfStay" required>'
            f'<option value="" disabled selected>Select&hellip;</option>{opts}</select></div>')

def split_section(sec, klass, third_line_slate=False, extra=''):
    lines = sec['headlineLines']
    if len(lines) == 3:
        h = f'{lines[0]}<br>{lines[1]}<br><em class="l3">{lines[2]}</em>'
    else:
        h = '<br>'.join(lines)
    body = sec.get('body')
    if isinstance(body, list):
        body_html = ''.join(f'<p class="seg-body">{b}</p>' for b in body)
    else:
        body_html = f'<p class="seg-body">{body}</p>'
    bullets = ''
    if sec.get('bullets'):
        bullets = '<ul class="seg-bullets">' + ''.join(f'<li>{b}</li>' for b in sec['bullets']) + '</ul>'
    kicker = f'<div class="seg-kicker">{sec["kicker"]}</div>' if sec.get('kicker') else ''
    subhead = f'<p class="seg-subhead">{sec["subhead"]}</p>' if sec.get('subhead') else ''
    img = (f'<div class="seg-split-img" role="img" aria-label="{sec["image"]["alt"]}" '
           f'style="background-image:url(\'{sec["image"]["src"]}\')">'
           + photo_tag(sec['image']['tagName'], sec['image']['tagCity']) + '</div>')
    copy = (f'<div class="seg-split-copy {"pad-l" if sec["imagePosition"]=="right" else "pad-r"}">'
            f'<span class="seg-eyebrow">{sec["eyebrow"]}</span>'
            f'<h2 class="seg-h">{h}</h2>{kicker}{subhead}{body_html}{bullets}{extra}<a class="seg-cta" href="#rfp-form" data-track="closing_cta">Request Proposal &nbsp;&rarr;</a></div>')
    cols = (copy + img) if sec['imagePosition'] == 'right' else (img + copy)
    return f'<section class="seg-split {klass}"><div class="seg-split-inner">{cols}</div></section>'

def render(seg):
    hero, rfp = seg['hero'], seg['rfp']
    dets = seg['detail'] if isinstance(seg['detail'], list) else [seg['detail']]
    details_html = '\n\n'.join(split_section(d, 'seg-detail') for d in dets)
    hl = hero['headlineLines']
    occ = ''.join(f'<option>{o}</option>' for o in rfp['occasionOptions'])
    def nav_item(s):
        active = ' class="active" aria-current="page"' if s['slug'] == seg['slug'] else ''
        return '<a href="' + s['slug'] + '.html"' + active + '>' + s['navLabel'] + '</a>'
    subnav = ''.join(nav_item(s) for s in SEGMENTS)
    gdir = GDIR.replace(GDIR_SENTENCE, GDIR_VARIANTS[seg['slug']])
    gdir = gdir.replace('<button class="gdir-cta" onclick="openModal()">Request RFP &nbsp;&rarr;</button>',
                        '<a class="gdir-cta" href="#rfp-form" data-track="closing_cta">Request RFP &nbsp;&rarr;</a>')
    occasions = ''
    if seg['occasionsGrid']:
        occasions = re.sub(r'onclick="openModal\(\)"', 'onclick="document.getElementById(\'rfp-form\').scrollIntoView({behavior:\'smooth\'})"', OCCASIONS)
    logos = ''
    if seg['logoWall']['enabled']:
        tiles = ''.join(f'<div class="seg-logo" role="img" aria-label="{re.sub("<[^>]+>","",l)}">{l}</div>' for l in seg['logoWall']['logos'])
        logos = (f'<!-- LOGO WALL — PLACEHOLDER marks; swap for real logo files once usage rights are confirmed -->\n'
                 f'<section class="seg-logos" aria-label="Client logos"><div class="seg-logos-inner">'
                 f'<span class="seg-eyebrow">{seg["logoWall"]["heading"]}</span>'
                 f'<div class="seg-logos-grid">{tiles}</div>'
                 f'<div class="seg-logos-note">Client marks pending usage-rights confirmation</div>'
                 f'</div></section>')
    quotes = ''.join(
        f'<div class="seg-quote"><p class="seg-quote-text">{t["quote"]}</p>'
        f'<div class="seg-quote-name">{t["name"]}</div>'
        f'<div class="seg-quote-title">{t["title"]} &middot; {t["company"]}</div></div>'
        for t in seg['testimonials'])
    faq = ''.join(
        f'<details><summary>{f["q"]}</summary><div class="a">{f["a"]}</div></details>'
        for f in seg['faq'])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{seg['title']}</title>
<!-- GENERATED by scripts/build-segments.py — edit the segment config there, not this file. -->
<style>
{BASE_CSS}
{SEG_CSS}
</style>
<link rel="stylesheet" href="/overrides.css">
<style>
{LATE_CSS}
</style>
<link rel="preload" as="video" href="{hero['media']['src']}">
</head>
<body data-segment="{seg['slug']}">
{NAV}
<a class="skip-to-content" href="#rfp-form">Skip to the RFP form</a>

<nav class="seg-subnav" aria-label="Group business segments">{subnav}</nav>

<main id="main" tabindex="-1">
<section class="hero" id="hero">
  <video class="hero-video" id="segHeroVideo" autoplay muted loop playsinline preload="auto" poster="{hero['media']['poster']}" aria-hidden="true">
    <source src="{hero['media']['src']}" type="video/mp4">
  </video>
  <div class="hero-veil"></div>
  <button class="hero-motion-toggle" id="segHeroToggle" aria-label="Pause background video"></button>
  {photo_tag(hero['media']['tagName'], hero['media']['tagCity'])}
  <div class="hero-content">
    <div class="hero-left">
      <span class="hero-eyebrow">{hero['eyebrow']}</span>
      <h1 class="hero-h">{hl[0]}<br>{hl[1]}<br><em class="l3">{hl[2]}</em></h1>
      <p class="hero-sub">{hero['body']}</p>
    </div>
    <div class="hero-rfp" id="rfp-form">
      <div class="hero-rfp-card">
        <span class="hero-rfp-title">Submit an RFP</span>
        <form class="rfp-mini-form" id="rfp-form-el">
          <input type="hidden" name="leadSource" value="{rfp['leadSource']}">
          <div class="rfp-mini-field">
            <label class="rfp-mini-label" for="rfp-occasion">Occasion type</label>
            <select class="rfp-mini-input rfp-mini-select" id="rfp-occasion" name="occasion" required>
              <option value="" disabled selected>Select&hellip;</option>{occ}
            </select>
          </div>
          <div class="rfp-mini-field">
            <label class="rfp-mini-label" for="rfp-dest">Destination</label>
            <select class="rfp-mini-input rfp-mini-select" id="rfp-dest" name="destination" required>{DEST_OPTIONS}</select>
          </div>
          <div class="rfp-mini-field">
            <label class="rfp-mini-label" for="rfp-checkin">Check-in</label>
            <input class="rfp-mini-input" id="rfp-checkin" name="checkin" type="date" required>
          </div>
          {third_field(rfp)}
          {extra_field(rfp)}
          <button class="rfp-mini-btn" type="submit">{rfp['submitLabel']} &nbsp;&rarr;</button>
          <div class="rfp-mini-note">Our team responds within 1 business day</div>
        </form>
        <div class="rfp-thanks" id="rfp-thanks">Thanks &mdash; your inquiry is on its way to our team. We&rsquo;ll be in touch within one business day.</div>
      </div>
    </div>
  </div>
</section>


{split_section(seg['whyUs'], 'seg-why')}

{details_html}

{logos}

<section class="seg-quotes dark" aria-label="What partners say"><div class="seg-quotes-inner">{quotes}</div></section>

{occasions}

{gdir}

<section class="seg-faq" aria-label="Frequently asked questions"><div class="seg-faq-inner">
  <span class="seg-eyebrow">Good to know</span>
  <h2 class="seg-h">Frequently asked <em class="l3">questions.</em></h2>
  {faq}
</div></section>

<section class="seg-close dark">
  <h2>Ready when <em>your people are.</em></h2>
  <p>Tell us what you need &mdash; our team responds within one business day.</p>
  <a href="#rfp-form" data-track="closing_cta">Request Proposal &nbsp;&rarr;</a>
</section>
</main>

{FOOTER}
<script>
{NAV_JS}
</script>
<script>
{FORM_JS}
</script>
</body>
</html>
"""

for seg in SEGMENTS:
    out = os.path.join(ROOT, seg['slug'] + '.html')
    open(out, 'w').write(render(seg))
    print('wrote', seg['slug'] + '.html', os.path.getsize(out)//1024, 'KB')
