/* ── SENTRAL BOOKING FUNNEL — DEMO DATA + STATE ──────────────────────────────
   Design prototype only. Every rate, availability flag, and tax line here is
   SAMPLE DATA for review. PRODUCTION: pages 2/4/6 pull live from StayNTouch
   via SentralOS (method TBC with Nathan); page 5 embeds Shift4 unchanged.
   State passes page-to-page in the query string:
   ?property=&city=&in=&out=&adults=&children=&rooms=studio:1,one-bedroom:2&plan=
──────────────────────────────────────────────────────────────────────────── */
window.BOOK = (function(){
  var ROOMS_STANDARD = [
    {slug:'studio',      name:'Studio',      sleeps:2, sqft:517,  beds:'1 queen bed',  baths:1, from:189},
    {slug:'one-bedroom', name:'One Bedroom', sleeps:2, sqft:673,  beds:'1 queen bed',  baths:1, from:229},
    {slug:'two-bedroom', name:'Two Bedroom', sleeps:4, sqft:1053, beds:'2 queen beds', baths:2, from:319}
  ];
  ROOMS_STANDARD.forEach(function(r){
    r.specs='Sleeps '+r.sleeps+' \u00b7 '+r.beds+' \u00b7 '+r.baths+' bath'+(r.baths>1?'s':'')+' \u00b7 '+r.sqft.toLocaleString('en-US')+' sq ft';
  });
  function P(slug,name,city,st,extra){
    var o={slug:slug,name:name,city:city,state:st,rooms:ROOMS_STANDARD,minStay:1};
    for(var k in (extra||{})) o[k]=extra[k];
    return o;
  }
  /* Inventory mirrors the live stay-with-us picker (sq ft / beds are Sol Modern
     samples for every property until each property's real room set is loaded). */
  var PROPERTIES=[
    P('sol-modern','Sol Modern','Phoenix','AZ',{address:'50 E. Fillmore Street, Phoenix, AZ 85004',phone:'(833) 370-4161'}),
    P('sentral-old-town','Sentral Old Town','Scottsdale','AZ'),
    P('sentral-dtla-755','Sentral DTLA 755','Los Angeles','CA',{minStay:30}),
    P('sentral-dtla-732','Sentral DTLA 732','Los Angeles','CA',{minStay:30}),
    P('figueroa-eight','Figueroa Eight','Los Angeles','CA',{minStay:30}),
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
    P('sentral-east-austin-1630','Sentral East Austin 1630','Austin','TX'),
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
    {slug:'direct', name:'Direct Rate',                 mult:1.00, note:'Best flexible rate. Free cancellation to 48 hours before arrival.'},
    {slug:'early',  name:'Advance Purchase — save 20%', mult:0.80, note:'Book 30+ days ahead. Pre-paid, non-refundable.'},
    {slug:'sale',   name:'Seasonal Sale — save 15%',    mult:0.85, note:'Limited dates. Blackout dates and terms apply.'}
  ];
  /* Property-specific tax line items — SAMPLE percentages, [FIELD] per property.
     PRODUCTION: driven by property data. */
  var TAXES=[
    {label:'State & local occupancy tax', pct:12.5, sample:true},
    {label:'Resort fee', flat:0, note:'None — the rate you see is the rate you pay'}
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
  function parseRooms(str){
    var out={}; (str||'').split(',').forEach(function(pair){
      var kv=pair.split(':'); if(kv[0]&&+kv[1]>0) out[kv[0]]=Math.min(9,+kv[1]);
    }); return out;
  }
  function roomsParam(sel){
    return Object.keys(sel).filter(function(k){return sel[k]>0})
      .map(function(k){return k+':'+sel[k]}).join(',');
  }
  function fmtDate(d){
    if(!d) return '';
    var dt=new Date(d+'T12:00:00');
    return dt.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'});
  }
  return {PROPERTIES:PROPERTIES,CITIES:CITIES,PLANS:PLANS,TAXES:TAXES,
          q:q,qs:qs,prop:prop,plan:plan,nights:nights,money:money,
          parseRooms:parseRooms,roomsParam:roomsParam,fmtDate:fmtDate};
})();
