/* ── SENTRAL BOOKING FUNNEL — DEMO DATA + STATE ──────────────────────────────
   Design prototype only. Every rate, availability flag, and tax line here is
   SAMPLE DATA for review. PRODUCTION: pages 2 + 6 pull live from StayNTouch
   via SentralOS (method TBC with Nathan); page 5 embeds Shift4 unchanged.
   State passes page-to-page in the query string:
   ?property=&city=&in=&out=&adults=&children=&rooms=studio:1,one-bedroom:2&plan=
──────────────────────────────────────────────────────────────────────────── */
window.BOOK = (function(){
  /* sleeps = room capacity used to filter search per room (adults + children).
     PRODUCTION (Mirt 10-14): read max_capacity per room type from SentralOS
     (or the StayNTouch API) — never hard-code. Standard: studio/1BR = 2,
     2BR = 4, 3BR = 6, but units with a den are exceptions, so DB data wins.
     Children count toward capacity (confirmed in testing; SNT docs/QB check pending). */
  var ROOMS_STANDARD = [
    {slug:'studio',      name:'Studio',      sleeps:2, sqft:517,  beds:'1 Queen Bed',  baths:1, from:189, left:4, img:'/assets/bk-room-studio.jpg', thumbs:['/assets/bk-room-1br.jpg','/assets/bk-city-1.jpg','/assets/bk-city-2.jpg']},
    {slug:'one-bedroom', name:'One Bedroom', sleeps:2, sqft:673,  beds:'1 Queen Bed',  baths:1, from:229, left:7, img:'/assets/bk-room-1br.jpg', thumbs:['/assets/bk-room-studio.jpg','/assets/bk-city-2.jpg','/assets/bk-city-3.jpg']},
    {slug:'two-bedroom', name:'Two Bedroom', sleeps:4, sqft:1053, beds:'2 Queen Beds', baths:2, from:319, left:2, img:'/assets/bk-room-2br.jpg', thumbs:['/assets/bk-city-1.jpg','/assets/bk-city-3.jpg','/assets/bk-room-studio.jpg']}
  ];
  /* Suite descriptions for the search "Suite details" pop-up — PRODUCTION:
     StayNTouch room-type description. One Bedroom = live StayNTouch copy for
     Sol Modern (10-13); Studio / Two Bedroom are samples in the same voice. */
  var DESC={
    'studio':'The studio apartment features a full kitchen, including a refrigerator, microwave, dishwasher, silverware and cooking utensils designed to make you feel at home. All units include a washer/dryer, complimentary wi-fi and flat screen TVs for streaming your favorite shows. This apartment features 1 queen bed in an open living and sleeping layout. Layouts, furnishings, and views may vary by unit.',
    'one-bedroom':'The one bedroom apartment features a full kitchen, including a refrigerator, microwave, dishwasher, silverware and cooking utensils designed to make you feel at home. All units include a washer/dryer, complimentary wi-fi and flat screen TVs for streaming your favorite shows. This apartment features 1 queen bed inside the bedroom, a walk-in closet and a balcony. Layouts, furnishings, and views may vary by unit.',
    'two-bedroom':'The two bedroom apartment features a full kitchen, including a refrigerator, microwave, dishwasher, silverware and cooking utensils designed to make you feel at home. All units include a washer/dryer, complimentary wi-fi and flat screen TVs for streaming your favorite shows. This apartment features a queen bed in each of its two bedrooms and two full baths. Layouts, furnishings, and views may vary by unit.'
  };
  ROOMS_STANDARD.forEach(function(r){
    r.desc=DESC[r.slug];
    r.specs='Sleeps '+r.sleeps+' \u00b7 '+r.beds+' \u00b7 '+r.baths+' Bath'+(r.baths>1?'s':'')+' \u00b7 '+r.sqft.toLocaleString('en-US')+' Sq Ft';
  });
  function P(slug,name,city,st,extra){
    var o={slug:slug,name:name,city:city,state:st,rooms:ROOMS_STANDARD,minStay:1};
    for(var k in (extra||{})) o[k]=extra[k];
    return o;
  }
  /* guide = the property's TouchStay arrival guide (content hosted in
     Contentful; Mirt 10-14) — "View arrival information" on Reservation
     Details. [FIELD] per property; only Sentral Old Town confirmed so far.
     Inventory mirrors the live stay-with-us picker (sq ft / beds are Sol Modern
     samples for every property until each property's real room set is loaded). */
  var PROPERTIES=[
    P('sol-modern','Sol Modern','Phoenix','AZ',{address:'50 E. Fillmore Street, Phoenix, AZ 85004',phone:'(833) 370-4161'}),
    P('sentral-old-town','Sentral Old Town','Scottsdale','AZ',{address:'4735 North Scottsdale Road, Scottsdale, AZ 85251',guide:'https://guide.sentraloldtown.com'}),
    P('sentral-dtla-755','Sentral DTLA 755','Los Angeles','CA',{minStay:31}),
    P('sentral-dtla-732','Sentral DTLA 732','Los Angeles','CA',{minStay:31}),
    P('figueroa-eight','Figueroa Eight','Los Angeles','CA',{minStay:31}),
    P('sentral-union-station','Sentral Union Station','Denver','CO'),
    P('alea','Alea','Miami','FL'),
    P('sentral-wynwood','Sentral Wynwood','Miami','FL'),
    P('star-metals','Star Metals West Midtown','Atlanta','GA'),
    P('sentral-michigan-avenue','Sentral Michigan Avenue','Chicago','IL'),
    P('otonomus','Otonomus','Las Vegas','NV'),
    P('inkwell','Inkwell','Charlotte','NC'),
    P('joinery-north','Joinery North','Charlotte','NC'),
    P('joinery-west','Joinery West','Charlotte','NC'),
    P('the-battery','The Battery','Philadelphia','PA',{minStay:30}),
    P('sentral-sobro','Sentral SoBro','Nashville','TN'),
    P('sentral-east-austin-1630','Sentral East Austin 1630','Austin','TX',{minStay:30}),
    P('sentral-east-austin-1614','Sentral East Austin 1614','Austin','TX'),
    P('forme','Forme','Houston','TX'),
    P('sentral-first-hill','Sentral First Hill','Seattle','WA',{minStay:30})
  ];
  /* 1a. City STAY Selector — multi-property markets only */
  var CITIES={
    'austin':      {name:'Austin',      props:['sentral-east-austin-1630','sentral-east-austin-1614']},
    'charlotte':   {name:'Charlotte',   props:['inkwell','joinery-north','joinery-west']},
    'los-angeles': {name:'Los Angeles', props:['sentral-dtla-755','sentral-dtla-732','figueroa-eight']},
    'miami':       {name:'Miami',       props:['alea','sentral-wynwood']}
  };
  /* Rate plans mirror the offers on the live property pages.
     PRODUCTION: replace with live StayNTouch rate plans (sale / early booking / direct). */
  var PLANS=[
    {slug:'fall',   short:'Fall Sale',    name:'Limited Time Fall Sale | Stay 2+ Nights & Save up to 20%', mult:0.80, note:'Flexible rate. Blackout dates and terms apply.'},
    {slug:'campus', short:'Campus Bound', name:'Campus Bound',                                             mult:0.86, note:'For campus tours, games & parents\u2019 weekends. Terms apply.'},
    {slug:'direct', short:'Book Direct',  name:'Sentral.com Book Direct Rate | Save up to 10% off Best Rates', mult:0.90, note:'Book direct and save.'}
  ];
  /* Property-specific tax line items — SAMPLE percentages, [FIELD] per property.
     Rates INCLUDE select fees (transparent-pricing disclosure, see the
     "Select Fees" dialog), so no separate fee line. PRODUCTION: property data. */
  var TAXES=[
    {label:'City Tax',  pct:6,   sample:true},
    {label:'Local Tax', pct:1.5, sample:true},
    {label:'State Tax', pct:5,   sample:true}
  ];
  /* Select fees INCLUDED in the advertised rate, itemized at checkout (Laurie
     10-13, pending Mirt). SAMPLE amounts per room — [FIELD] per property;
     categories mirror the Included Fees disclosure (resort & destination /
     cleaning / residence). PRODUCTION: property data via SentralOS. */
  var FEES=[
    {label:'Resort & Destination Fee', perNight:15, sample:true},
    {label:'Cleaning Fee',             perStay:0,   sample:true},
    {label:'Residence Fee',            perStay:0,   sample:true}
  ];
  function q(){ var o={},s=new URLSearchParams(location.search); s.forEach(function(v,k){o[k]=v}); return o; }
  function qs(params){
    var cur=q(); for(var k in params){ if(params[k]===null) delete cur[k]; else cur[k]=params[k]; }
    return Object.keys(cur).filter(function(k){return cur[k]!==''&&cur[k]!=null})
      .map(function(k){return k+'='+encodeURIComponent(cur[k])}).join('&');
  }
  function prop(slug){ return PROPERTIES.filter(function(p){return p.slug===slug})[0]||null; }
  function plan(slug){ return PLANS.filter(function(p){return p.slug===slug})[0]||PLANS[0]; }
  function nights(i,o){
    var a=new Date(i),b=new Date(o),n=Math.round((b-a)/86400000);
    return (isFinite(n)&&n>0)?n:null;
  }
  function money(n){ return '$'+Math.round(n).toLocaleString('en-US'); }
  function cents(n){ return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}); }
  function parseRooms(str){
    var out={}; (str||'').split(',').forEach(function(pair){
      var kv=pair.split(':');
      if(kv[0]&&+kv[1]>0) out[kv[0]]={n:Math.min(9,+kv[1]), plan:kv[2]||'fall'};
    }); return out;
  }
  function roomsParam(sel){
    return Object.keys(sel).filter(function(k){return sel[k]&&sel[k].n>0})
      .map(function(k){return k+':'+sel[k].n+':'+(sel[k].plan||'fall')}).join(',');
  }
  /* Rooms in booking order: "studio:1:fall,two-bedroom:1:campus" → list.
     Room i is booked for party room i (Rooms & Guests picker). Old merged
     "slug:qty:plan" URLs still read fine. */
  function roomList(str){
    var out=[]; (str||'').split(',').forEach(function(p){
      var kv=p.split(':'); if(kv[0]&&+kv[1]>0) out.push({slug:kv[0],n:Math.min(9,+kv[1]),plan:kv[2]||'fall'});
    }); return out;
  }
  function listParam(list){ return list.map(function(it){return it.slug+':'+(it.n||1)+':'+(it.plan||'fall')}).join(','); }
  /* Party (adults/children per room) — ?party=2-0,1-1, else adults/children totals as one room */
  function party(qq){
    return window.PartyPicker ? window.PartyPicker.parse(qq.party,qq.adults,qq.children)
      : [{a:+qq.adults||2,c:+qq.children||0}];
  }
  function planPrice(r,pl){ return Math.round(r.from*pl.mult); }
  function fmtDate(d){
    if(!d) return '';
    var dt=new Date(d+'T12:00:00');
    return dt.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'});
  }
  /* Stay summary shared by Checkout + Confirmation: suites (text only, rate
     plan), stay facts, and Total Price Details itemized like the live engine
     (nightly total → included select fees → taxes on the full amount). */
  function summary(qq, opts){
    opts=opts||{};
    var cur=prop(qq.property)||PROPERTIES[0], list=roomList(qq.rooms), n=nights(qq['in'],qq.out)||1;
    var pty=party(qq), PP=window.PartyPicker, rooms='', sub=0, count=0;
    var tot=pty.reduce(function(t,r){t.a+=r.a;t.c+=r.c;return t},{a:0,c:0}), ad=tot.a, ch=tot.c;
    list.forEach(function(it,i){
      var r=cur.rooms.filter(function(x){return x.slug===it.slug})[0]; if(!r) return;
      var pl=plan(it.plan), amt=planPrice(r,pl)*it.n*n; sub+=amt; count+=it.n;
      var g=(list.length>1||pty.length>1)&&pty[i]&&PP? ' · '+PP.guests(pty[i]) : '';
      rooms+='<div class="bk-suite"><div><b>'+(list.length>1?'Room '+(i+1)+' · ':'')+(it.n>1?it.n+' × ':'')+r.name+'</b><small>'+pl.name+g+'</small></div>'+
        (opts.modify?'<a href="'+opts.modify+'">Modify</a>':'')+'</div>';
    });
    function fact(k,v){ return '<div><dt>'+k+'</dt><dd>'+v+'</dd></div>'; }
    var facts=fact('Check-in',fmtDate(qq['in'])+'<small>4:00 PM</small>')+
      fact('Check-out',fmtDate(qq.out)+'<small>11:00 AM</small>')+
      fact('Nights',n)+fact('Guests',ad+(ad>1?' adults':' adult')+', '+ch+(ch===1?' child':' children')+(count>1?'<small>across '+count+' rooms</small>':''))+
      (count>1?fact('Rooms',count):'');
    var lines='', total=sub;
    if(sub){
      var fl='', fees=0;
      FEES.forEach(function(f){
        var a=((f.perNight||0)*n+(f.perStay||0))*count; if(!a) return; fees+=a;
        fl+='<div class="bk-line"><span>'+f.label+(f.sample?' <small>(sample)</small>':'')+'</span><span>'+cents(a)+'</span></div>';
      });
      lines+='<div class="bk-line"><span>Nightly total <small>'+n+(n>1?' nights':' night')+'</small></span><span>'+cents(sub-fees)+'</span></div>'+fl;
      TAXES.forEach(function(t){
        var a=Math.round(sub*t.pct)/100; total+=a;
        lines+='<div class="bk-line"><span>'+t.label+(t.sample?' <small>(sample '+t.pct+'%)</small>':'')+'</span><span>'+cents(a)+'</span></div>';
      });
      if(qq.promo) lines+='<div class="bk-line"><span>Discount code <small>'+qq.promo.toUpperCase()+'</small></span><span><small>validated by StayNTouch at build</small></span></div>';
    }
    return {cur:cur,nights:n,count:count,sub:sub,total:total,rooms:rooms,facts:facts,lines:lines};
  }
  return {summary:summary,roomList:roomList,listParam:listParam,party:party,PROPERTIES:PROPERTIES,CITIES:CITIES,PLANS:PLANS,TAXES:TAXES,FEES:FEES,
          q:q,qs:qs,prop:prop,plan:plan,nights:nights,money:money,cents:cents,planPrice:planPrice,
          parseRooms:parseRooms,roomsParam:roomsParam,fmtDate:fmtDate};
})();
