/* Little Learners — tap-the-picture games for ages 4–6 (pre-school up to Class 1).
   One page (little.html), three views chosen by the URL:
     little.html               the hub: every topic, grouped, with stars earned
     little.html?f=1.counting  one topic: 3 rounds to play + notes for the grown-up
     little.html?f=…&r=2       playing round 2 of that topic
   Data: content/little/manifest.json (ordered file list) + one JSON per topic:
     { "title", "emoji", "group": "maths" | "words" | "world",
       "parent": [ { "learn": "...", "why": "..." } ],   // what to learn + why it matters
       "ask":    [ "spoken question to try at home", ... ],
       "rounds": [ [ question ×5 ], ×3 ] }               // Start, Grow, Class 1 ready
   A question: { "t": "text (shown + read aloud)", "p": "big picture (optional)",
                 "o": ["RIGHT answer first", "wrong", ...], "h": "hint / why",
                 "x": true  -> don't read the options aloud (reading questions) }
   The page shuffles the options. A star is earned only for a right FIRST tap; the best
   score per round is kept in localStorage. Check the data with tools/check_little.py. */
(function () {
  "use strict";

  var DIR = "content/little/";
  var GROUPS = [
    { id: "maths", name: "Numbers & Maths", emoji: "🔢" },
    { id: "words", name: "Letters & Words", emoji: "🔤" },
    { id: "world", name: "Me & My World",  emoji: "🌍" }
  ];
  var ROUNDS = [
    { name: "Start",          icon: "🌱" },
    { name: "Grow",           icon: "🌿" },
    { name: "Class 1 ready",  icon: "🌳" }
  ];
  var CHEERS = ["Well done!", "Super!", "Yay, you got it!", "Great job!", "Brilliant!"];

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.json();
    });
  }
  function best(file, r) {
    try { var v = window.localStorage.getItem("little:" + file + ":" + r); return v == null ? null : +v; }
    catch (e) { return null; }
  }
  function saveBest(file, r, score) {
    try {
      var old = best(file, r);
      if (old == null || score > old) window.localStorage.setItem("little:" + file + ":" + r, String(score));
    } catch (e) {}
  }
  function stars(n, of) {
    var s = "";
    for (var i = 0; i < of; i++) s += i < n ? "⭐" : "☆";
    return s;
  }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ---------- reading aloud ---------- */
  var synth = window.speechSynthesis || null;
  var voice = null;
  function pickVoice() {
    if (!synth) return;
    var vs = synth.getVoices();
    voice = vs.filter(function (v) { return /en[-_]IN/i.test(v.lang); })[0] ||
            vs.filter(function (v) { return /^en/i.test(v.lang); })[0] || null;
  }
  if (synth) { pickVoice(); synth.onvoiceschanged = pickVoice; }
  // emoji are for the eyes; read the words only
  function speakable(s) {
    return String(s)
      .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{1F1E6}-\u{1F1FF}️‍⃣]/gu, "")
      .replace(/₹\s?(\d+)/g, "$1 rupees")
      .replace(/_{2,}/g, " blank ")
      .replace(/[–—]/g, ", ")
      .replace(/\s+/g, " ").trim();
  }
  function say(text) {
    if (!synth) return;
    text = speakable(text);
    if (!text) return;
    synth.cancel();
    var u = new SpeechSynthesisUtterance(text);
    if (voice) u.voice = voice;
    u.lang = voice ? voice.lang : "en-IN";
    u.rate = 0.85; u.pitch = 1.1;
    synth.speak(u);
  }

  /* ---------- views ---------- */
  var mount, topics = [];

  function topicByFile(f) {
    for (var i = 0; i < topics.length; i++) if (topics[i].file === f) return topics[i];
    return null;
  }
  function go(url, push) {
    if (synth) synth.cancel();
    if (push) history.pushState(null, "", url);
    route();
    window.scrollTo(0, 0);
  }
  function route() {
    var p = new URLSearchParams(location.search);
    var t = topicByFile(p.get("f"));
    var r = parseInt(p.get("r"), 10);
    document.body.classList.toggle("ll-in", !!t);   // shrink the header inside a topic
    if (!t) return showHub();
    if (r >= 1 && r <= t.data.rounds.length) return play(t, r);
    showTopic(t);
  }
  function link(text, url, cls) {
    var a = el("a", cls, text);
    a.href = url;
    a.addEventListener("click", function (e) { e.preventDefault(); go(url, true); });
    return a;
  }

  function showHub() {
    document.title = "Little Learners — tap-and-learn games";
    mount.innerHTML = "";
    var earned = 0, possible = 0;
    GROUPS.forEach(function (g) {
      var list = topics.filter(function (t) { return t.data.group === g.id; });
      if (!list.length) return;
      mount.appendChild(el("h2", "ll-group", g.emoji + " " + g.name));
      var grid = el("div", "ll-grid");
      list.forEach(function (t) {
        var got = 0, of = 0;
        t.data.rounds.forEach(function (qs, i) { got += best(t.file, i + 1) || 0; of += qs.length; });
        earned += got; possible += of;
        var a = link("", "little.html?f=" + encodeURIComponent(t.file), "ll-card" + (got ? " started" : ""));
        a.appendChild(el("span", "ll-card-emoji", t.data.emoji));
        a.appendChild(el("strong", null, t.data.title));
        a.appendChild(el("span", "ll-card-stars", "⭐ " + got + " / " + of));
        grid.appendChild(a);
      });
      mount.appendChild(grid);
    });
    var tally = el("p", "test-tally", "⭐ " + earned + " of " + possible + " stars collected");
    mount.insertBefore(tally, mount.firstChild);
  }

  function showTopic(t) {
    var d = t.data;
    document.title = d.title + " — Little Learners";
    mount.innerHTML = "";
    mount.appendChild(link("← All topics", "little.html", "ll-back"));
    var head = el("div", "ll-topic-head");
    head.appendChild(el("div", "ll-topic-emoji", d.emoji));
    head.appendChild(el("h2", null, d.title));
    mount.appendChild(head);

    var rounds = el("div", "ll-rounds");
    d.rounds.forEach(function (qs, i) {
      var lvl = ROUNDS[i] || { name: "Round " + (i + 1), icon: "🎯" };
      var b = best(t.file, i + 1);
      var a = link("", "little.html?f=" + encodeURIComponent(t.file) + "&r=" + (i + 1), "ll-round" + (b != null ? " done" : ""));
      a.appendChild(el("span", "ll-round-icon", lvl.icon));
      a.appendChild(el("strong", null, lvl.name));
      a.appendChild(el("span", "ll-round-stars", b != null ? stars(b, qs.length) : qs.length + " questions"));
      rounds.appendChild(a);
    });
    mount.appendChild(rounds);

    var learn = el("details", "ll-parent");
    learn.open = true;
    learn.appendChild(el("summary", null, "📘 For the grown-up: what to learn, and why"));
    var ul = el("ul");
    d.parent.forEach(function (p) {
      var li = el("li");
      li.appendChild(el("strong", null, p.learn));
      var why = el("div", "ll-why");
      why.appendChild(el("b", null, "Why: "));
      why.appendChild(document.createTextNode(p.why));
      li.appendChild(why);
      ul.appendChild(li);
    });
    learn.appendChild(ul);
    mount.appendChild(learn);

    var ask = el("details", "ll-parent ll-ask");
    ask.open = true;
    ask.appendChild(el("summary", null, "🗣️ Ask out loud — at home, no screen"));
    var ol = el("ol");
    d.ask.forEach(function (q) { ol.appendChild(el("li", null, q)); });
    ask.appendChild(ol);
    mount.appendChild(ask);
  }

  function play(t, r) {
    var qs = t.data.rounds[r - 1];
    var lvl = ROUNDS[r - 1] || { name: "Round " + r, icon: "🎯" };
    var topicUrl = "little.html?f=" + encodeURIComponent(t.file);
    var i = 0, score = 0;
    document.title = lvl.name + " · " + t.data.title + " — Little Learners";

    function renderQ() {
      var q = qs[i], firstTry = true, solved = false;
      mount.innerHTML = "";
      var bar = el("div", "ll-playbar");
      bar.appendChild(link("✕", topicUrl, "ll-quit"));
      var dots = el("div", "ll-dots");
      for (var k = 0; k < qs.length; k++) dots.appendChild(el("span", k < i ? "done" : k === i ? "now" : ""));
      bar.appendChild(dots);
      bar.appendChild(el("span", "ll-playname", lvl.icon + " " + t.data.title));
      mount.appendChild(bar);

      var card = el("div", "ll-q");
      if (q.p) card.appendChild(el("div", "ll-pic", q.p));
      var line = el("div", "ll-qline");
      line.appendChild(el("p", "ll-qtext", q.t));
      var opts = shuffle(q.o.map(function (o, j) { return { text: o, right: j === 0 }; }));
      function readAll() {
        var spoken = opts.map(function (o) { return speakable(o.text); });
        var canRead = !q.x && spoken.every(function (s) { return s; });
        say(canRead ? q.t + " ... Is it: " + spoken.join(", or ") + "?" : q.t);
      }
      if (synth) {
        var sp = el("button", "ll-speak", "🔊");
        sp.type = "button";
        sp.setAttribute("aria-label", "Read the question aloud");
        sp.addEventListener("click", readAll);
        line.appendChild(sp);
      }
      card.appendChild(line);

      var grid = el("div", "ll-opts");
      var fb = el("div", "ll-fb");
      opts.forEach(function (o) {
        var b = el("button", "ll-opt" + (speakable(o.text).length <= 2 ? " big" : ""), o.text);
        b.type = "button";
        b.addEventListener("click", function () {
          if (solved || b.disabled) return;
          if (o.right) {
            solved = true;
            if (firstTry) score++;
            b.classList.add("right");
            var cheer = firstTry ? CHEERS[Math.floor(Math.random() * CHEERS.length)] : "Yes, that's it!";
            fb.className = "ll-fb ok";
            fb.innerHTML = "";
            fb.appendChild(el("strong", null, (firstTry ? "⭐ " : "✅ ") + cheer));
            if (q.h) fb.appendChild(el("p", null, q.h));
            var next = el("button", "test-submit ll-next", i + 1 < qs.length ? "Next ▶" : "See my stars ⭐");
            next.type = "button";
            next.addEventListener("click", function () { i++; i < qs.length ? renderQ() : finish(); });
            fb.appendChild(next);
            say(cheer + " " + (q.h || ""));
            next.focus({ preventScroll: true });
          } else {
            firstTry = false;
            b.classList.add("wrong");
            b.disabled = true;
            fb.className = "ll-fb try";
            fb.innerHTML = "";
            fb.appendChild(el("strong", null, "🤔 Not this one — try again!"));
            if (q.h) fb.appendChild(el("p", null, "Hint: " + q.h));
            say("Try again! " + (q.h || ""));
          }
        });
        grid.appendChild(b);
      });
      card.appendChild(grid);
      card.appendChild(fb);
      mount.appendChild(card);
      if (i > 0) readAll();   // the first question waits for the 🔊 tap (browsers block un-tapped speech)
    }

    function finish() {
      saveBest(t.file, r, score);
      mount.innerHTML = "";
      var box = el("div", "ll-done");
      box.appendChild(el("div", "ll-done-stars", stars(score, qs.length)));
      var msg = score === qs.length ? "Wow — all " + score + " stars!" :
                score >= qs.length - 2 ? "Great work! " + score + " stars!" :
                score + (score === 1 ? " star" : " stars") + ". Let's play it again!";
      box.appendChild(el("h2", null, msg));
      var acts = el("div", "test-actions");
      var again = el("button", "test-submit", "🔁 Play again");
      again.type = "button";
      again.addEventListener("click", function () { i = 0; score = 0; renderQ(); });
      acts.appendChild(again);
      if (r < t.data.rounds.length) {
        var lv = ROUNDS[r] || { name: "Next round", icon: "▶" };
        acts.appendChild(link(lv.icon + " " + lv.name, topicUrl + "&r=" + (r + 1), "toggle-all"));
      }
      acts.appendChild(link("← " + t.data.title, topicUrl, "toggle-all"));
      box.appendChild(acts);
      mount.appendChild(box);
      say(msg);
    }

    renderQ();
  }

  function init() {
    mount = document.getElementById("ll");
    if (!mount) return;
    getJSON(DIR + "manifest.json")
      .then(function (files) {
        return Promise.all(files.map(function (name) {
          return getJSON(DIR + name).then(function (data) {
            return { file: name.replace(/\.json$/, ""), data: data };
          });
        }));
      })
      .then(function (list) {
        topics = list;
        window.addEventListener("popstate", route);
        route();
      })
      .catch(function (err) {
        mount.innerHTML = '<div class="empty"><div class="big">📭</div><strong>Couldn’t load the games</strong>' +
          "Open the site with a local server (<code>python3 -m http.server</code>).</div>";
        if (window.console) console.error("[little]", err);
      });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
