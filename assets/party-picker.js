/* ── SENTRAL ROOMS & GUESTS PICKER ─────────────────────────────────────────
   One component for every booking widget (home bar, property pages, city
   selectors, search). Guests choose how many rooms and the adults/children in
   EACH room (Mirt 10-14: matches the live engine), so search only shows suites
   that fit each room. 4+ suites = group booking (Reservation Policies), so
   the picker caps at 3 rooms and points larger parties to the group RFP.
   URL state: ?party=2-0,1-1  (adults-children per room, in room order) plus
   adults/children totals for anything that only reads totals.
   Usage: PartyPicker.mount(el, {party:'2-0', onChange:fn}) → el.partyValue()
──────────────────────────────────────────────────────────────────────────── */
window.PartyPicker=(function(){
  var MAX_ROOMS=3, MAX_A=6, MAX_C=4, uid=0;
  function parse(str,adults,children){
    var out=[];
    (str||'').split(',').forEach(function(p){
      var m=/^(\d+)-(\d+)$/.exec(p.trim()); if(!m) return;
      out.push({a:Math.max(1,Math.min(MAX_A,+m[1])),c:Math.max(0,Math.min(MAX_C,+m[2]))});
    });
    if(!out.length) out=[{a:Math.max(1,+adults||2),c:Math.max(0,+children||0)}];
    return out.slice(0,MAX_ROOMS);
  }
  function str(arr){ return arr.map(function(r){return r.a+'-'+r.c}).join(','); }
  function totals(arr){ return arr.reduce(function(t,r){t.a+=r.a;t.c+=r.c;return t},{a:0,c:0}); }
  function guests(r){ return r.a+(r.a>1?' adults':' adult')+(r.c?', '+r.c+(r.c>1?' children':' child'):''); }
  function label(arr){
    var t=totals(arr);
    return arr.length+(arr.length>1?' Rooms':' Room')+' · '+t.a+(t.a>1?' Adults':' Adult')+', '+t.c+(t.c===1?' Child':' Children');
  }
  function mount(el,opts){
    opts=opts||{};
    var party=parse(opts.party,opts.adults,opts.children), id='pp'+(++uid);
    el.classList.add('pp');
    el.innerHTML='<button type="button" class="pp-btn" aria-haspopup="true" aria-expanded="false" aria-controls="'+id+'"'+
      (opts.labelledby?' aria-labelledby="'+opts.labelledby+' '+id+'-v"':'')+'><span id="'+id+'-v"></span></button>'+
      '<div class="pp-panel" id="'+id+'" role="group" aria-label="Rooms and guests" hidden><div class="pp-rooms"></div>'+
      '<div class="pp-foot"><button type="button" class="pp-add">+ Add a room</button><button type="button" class="pp-done">Done</button></div>'+
      '<p class="pp-group" hidden>Booking 4 or more suites? <a href="/group-travel.html#rfp-form">Request group rates &rarr;</a></p></div>';
    var btn=el.querySelector('.pp-btn'), panel=el.querySelector('.pp-panel'), list=el.querySelector('.pp-rooms');
    function stepper(i,k,min,max,name){
      var v=party[i][k];
      return '<div class="pp-row"><span class="pp-k">'+name+(k==='c'?' <small>0–17</small>':'')+'</span>'+
        '<span class="pp-ctl"><button type="button" data-i="'+i+'" data-k="'+k+'" data-d="-1" aria-label="Fewer '+name.toLowerCase()+', room '+(i+1)+'"'+(v<=min?' disabled':'')+'>&minus;</button>'+
        '<span class="pp-n" aria-live="polite">'+v+'</span>'+
        '<button type="button" data-i="'+i+'" data-k="'+k+'" data-d="1" aria-label="More '+name.toLowerCase()+', room '+(i+1)+'"'+(v>=max?' disabled':'')+'>+</button></span></div>';
    }
    function render(){
      list.innerHTML=party.map(function(r,i){
        return '<div class="pp-room"><div class="pp-room-h"><b>Room '+(i+1)+'</b>'+
          (party.length>1?'<button type="button" class="pp-rm" data-rm="'+i+'">Remove</button>':'')+'</div>'+
          stepper(i,'a',1,MAX_A,'Adults')+stepper(i,'c',0,MAX_C,'Children')+'</div>';
      }).join('');
      el.querySelector('.pp-add').hidden=party.length>=MAX_ROOMS;
      el.querySelector('.pp-group').hidden=party.length<MAX_ROOMS;
      document.getElementById(id+'-v').textContent=label(party);
      if(opts.onChange) opts.onChange(party.slice());
    }
    function toggle(open){
      panel.hidden=!open; btn.setAttribute('aria-expanded',open);
      if(open){ var f=panel.querySelector('button:not([disabled])'); if(f) f.focus(); }
    }
    btn.addEventListener('click',function(){ toggle(panel.hidden); });
    panel.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b) return;
      if(b.hasAttribute('data-d')){
        var i=+b.getAttribute('data-i'),k=b.getAttribute('data-k'),d=+b.getAttribute('data-d');
        party[i][k]=Math.max(k==='a'?1:0,Math.min(k==='a'?MAX_A:MAX_C,party[i][k]+d)); render();
        var again=list.querySelector('[data-i="'+i+'"][data-k="'+k+'"][data-d="'+d+'"]');
        (again&&!again.disabled?again:list.querySelector('[data-i="'+i+'"][data-k="'+k+'"]:not([disabled])')).focus();
      } else if(b.hasAttribute('data-rm')){ party.splice(+b.getAttribute('data-rm'),1); render(); btn.focus(); toggle(true); }
      else if(b.classList.contains('pp-add')){ party.push({a:1,c:0}); render(); toggle(true); }
      else if(b.classList.contains('pp-done')){ toggle(false); btn.focus(); }
    });
    document.addEventListener('click',function(e){ if(!panel.hidden&&!el.contains(e.target)) toggle(false); });
    el.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!panel.hidden){ toggle(false); btn.focus(); } });
    el.partyValue=function(){ return party.slice(); };
    el.partyOpen=function(){ toggle(true); };
    render();
    return el;
  }
  /* Query-string fields for a party: party + totals (for pages that read totals) */
  function params(arr){ var t=totals(arr); return {party:str(arr),adults:String(t.a),children:String(t.c)}; }
  return {parse:parse,str:str,totals:totals,guests:guests,label:label,params:params,mount:mount,MAX_ROOMS:MAX_ROOMS};
})();
