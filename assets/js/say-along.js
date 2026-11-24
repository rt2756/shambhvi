/* Say-along — the screen shows one big thing at a time and reads it aloud, then moves on.
   Part of Little Learners (ages 4–6). One page, say-along.html, three modes chosen by ?m=:
     count   1, 2, 3 … (from / to / count-by)         say: "21"
     abc     A a  🍎 Apple                             say: "Ay" … pause … "Ay for Apple"
     tables  6 × 2 = 12  (from table / to table)       say: "6 twos are 12"
   Every mode has two styles:
     👩‍🏫 Teach me  shows and says each one in turn.
     🙋 Ask me    hides the next one ("5 → ?", "B → ?", "3 × 5 = ?"), asks for it, and waits —
                  it shows the answer only when the grown-up presses 👀 Show answer (or taps the card).
   Tables are read as groups ("six twos are twelve" = six lots of two), the way they are
   chanted in Indian classrooms, so the words carry the meaning, not just the sound.
   Speech is the browser's own (speechSynthesis); the next item starts only after the
   current one has finished being spoken, plus a pause set by the speed buttons. */
(function () {
  "use strict";

  var LETTERS = [
    ["A", "Apple", "🍎"], ["B", "Ball", "⚽"], ["C", "Cat", "🐱"], ["D", "Dog", "🐶"],
    ["E", "Elephant", "🐘"], ["F", "Fish", "🐟"], ["G", "Grapes", "🍇"], ["H", "House", "🏠"],
    ["I", "Ice cream", "🍦"], ["J", "Juice", "🧃"], ["K", "Kite", "🪁"], ["L", "Lion", "🦁"],
    ["M", "Mango", "🥭"], ["N", "Nest", "🪺"], ["O", "Orange", "🍊"], ["P", "Parrot", "🦜"],
    ["Q", "Queen", "👸"], ["R", "Rabbit", "🐰"], ["S", "Sun", "☀️"], ["T", "Tiger", "🐯"],
    ["U", "Umbrella", "☂️"], ["V", "Van", "🚐"], ["W", "Watch", "⌚"], ["X", "Xylophone", "🎶"],
    ["Y", "Yo-yo", "🪀"], ["Z", "Zebra", "🦓"]
  ];
  // a lone "A" is often read as the word "a" (uh); spell the letter's name instead
  var LETTER_NAME = { A: "Ay" };
  function letterName(l) { return LETTER_NAME[l] || l; }
  var GROUPS_OF = ["", "ones", "twos", "threes", "fours", "fives", "sixes", "sevens", "eights", "nines", "tens"];
  var ONE_OF    = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];

  // rate = speaking speed; gap = pause before the next item;
  // breath = pause between the parts of one item ("C" … "C for Cat")
  var SPEEDS = {
    slow:     { label: "🐢 Slow",      rate: 0.7, gap: 1400, breath: 800 },
    normal:   { label: "🚶 Normal",    rate: 0.9, gap: 700,  breath: 550 },
    fast:     { label: "🐇 Fast",      rate: 1.1, gap: 250,  breath: 350 },
    veryfast: { label: "🚀 Very fast", rate: 1.5, gap: 60,   breath: 180 }
  };
  var STYLES = [["teach", "👩‍🏫 Teach me"], ["ask", "🙋 Ask me"]];
  // six colours, as CSS variables so the dark theme can swap in brighter versions
  var COLORS = ["var(--sa-c0)", "var(--sa-c1)", "var(--sa-c2)", "var(--sa-c3)", "var(--sa-c4)", "var(--sa-c5)"];

  var MODES = {
    count: {
      name: "Counting", emoji: "🔢",
      why: [
        ["Point and say each number together.", "Saying it while seeing the written number links the sound to the symbol — that link is what reading numbers is."],
        ["Try counting by 2s, 5s and 10s once 1s feel easy.", "Skip counting is the times table in disguise: counting by 2s is the 2 table, so tables later feel familiar, not new."],
        ["🙋 Ask me shows “5 → ?”: the child says what comes next, then you tap to see it.", "Knowing what comes after 5 without starting again from 1 is the real test of number order — it is exactly what “one more than” sums need."],
        ["🔊 Say: 2 · 3 · 23 reads the digits first, then the number.", "It shows that 23 is written with a 2 and a 3 — the first step to tens and ones. The chart on the right shows it too: each column is one ten (1–10, 11–20 …), and every number in a row ends in the same digit — each step to the right is 10 more."]
      ]
    },
    abc: {
      name: "Alphabet", emoji: "🔤",
      why: [
        ["Say the letter, then the word: “B — B for Ball”.", "The word gives the letter a sound to hang on — ball starts with the /b/ sound — which is the first step to reading words."],
        ["Show both shapes: big B and small b.", "Books use mostly small letters, so children need to know both are the same letter."],
        ["🙋 Ask me hides the next letter (“B → ?”) until you tap.", "Saying it before seeing it makes the child pull the order out of memory instead of copying what is on the screen — that is what makes it stick."]
      ]
    },
    tables: {
      name: "Tables", emoji: "✖️",
      why: [
        ["It says “six twos are twelve”, not “six two twelve”.", "“Six twos” means six lots of two — line up six pairs of spoons and count: twelve. The words keep the meaning, so the child can work an answer out, not only remember it."],
        ["Each answer is the last one plus the table number.", "6 × 3 = 18 because it is one more 6 than 6 × 2 = 12. If a child forgets a line, they can add on from the line before."],
        ["Use 👩‍🏫 Teach me first, then 🙋 Ask me: it says “3 fives are…?”, the child answers, then you tap to see it.", "Pulling an answer out of memory is what makes it stick — much more than hearing it again — and the reveal straight after tells the child at once whether they were right. Mixed up order stops them just counting on from the line before."]
      ]
    }
  };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function range(a, b, step) {
    var r = [];
    for (var i = a; i <= b; i += (step || 1)) r.push(i);
    return r;
  }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  /* ---------- the list of things to show and say ----------
     A plain item: { big, say, pic?, word?, pair? (two letters), line?+ans? (table row) }
     An Ask me item: { ask: true, qLine: "5 → ", qSay: "What comes after 5?", answer: plain item } */
  function buildItems(mode, s) {
    var out = [], ask = s.style === "ask";
    if (mode === "count") {
      var step = s.by, start = s.from, prev = null;
      if (step > 1) start = Math.ceil(s.from / step) * step;
      for (var n = start; n <= s.to; n += step) {
        // "Digits, then number": 23 is read "2 … 3 … 23", so the child hears the two digits
        // that make the number before its name (single digits are just said once)
        var say = s.say === "digits" && n >= 10 ? String(n).split("").concat([String(n)]) : String(n);
        var plain = { big: String(n), say: say, cell: "n" + n };
        // the first number is shown, so the child has somewhere to start from
        out.push(ask && prev != null ? { ask: true, qLine: prev + " → ", qSay: "What comes after " + prev + "?", answer: plain } : plain);
        prev = n;
      }
    } else if (mode === "abc") {
      LETTERS.forEach(function (l, i) {
        var name = letterName(l[0]);
        // two parts, spoken with a pause between: "C" … "C for Cat"
        var plain = { pair: [l[0], l[0].toLowerCase()], big: l[0] + " " + l[0].toLowerCase(), pic: l[2], word: l[1],
                      say: [name, name + " for " + l[1]], cell: "l" + l[0] };
        var before = i > 0 ? LETTERS[i - 1][0] : null;
        out.push(ask && before ? { ask: true, qLine: before + " → ", qSay: "What comes after " + letterName(before) + "?", answer: plain } : plain);
      });
    } else {
      for (var t = s.from; t <= s.to; t++) {
        out.push({ big: "Table of " + t, title: true, say: "Table of " + t });
        var rows = s.order === "mixed" ? shuffle(range(1, 10)) : range(1, 10);
        rows.forEach(function (m) {
          // the 1 table is one group, so it is singular: "1 three is 3" (not "1 threes are 3")
          var words = t === 1 ? "1 " + ONE_OF[m] + " is" : t + " " + GROUPS_OF[m] + " are";
          var line = t + " × " + m + " = ", ans = t * m;
          var plain = { line: line, ans: ans, big: line + ans, say: words + " " + ans, cell: "t" + t + "x" + m };
          out.push(ask ? { ask: true, qLine: line, qSay: words + "?", answer: plain } : plain);
        });
      }
    }
    return out;
  }

  /* ---------- the board: every item of the range, in its place ----------
     Each spoken item flies across and settles into its own cell, so by the end the
     whole chart is filled in: a hundred chart in columns of ten, an A–Z chart, or the tables
     side by side (one column per table). Cells have the same key as their item. */
  function buildBoard(mode, s) {
    var b = { cls: mode, cols: 10, head: [], cells: [] };
    if (mode === "count") {
      var step = s.by, inSeq = {};
      var start = step > 1 ? Math.ceil(s.from / step) * step : s.from;
      for (var n = start; n <= s.to; n += step) inSeq[n] = true;
      // one column per ten, filled top to bottom like the tables: 1–10 down the first
      // column, 11–20 down the next. Cells are added row by row, so row r, column c holds
      // the number (d0 + c) × 10 + r + 1.
      var d0 = Math.floor((s.from - 1) / 10), d1 = Math.ceil(s.to / 10) - 1;
      b.cols = d1 - d0 + 1;
      for (var r = 0; r < 10; r++) {
        for (var c = d0; c <= d1; c++) {
          var k = c * 10 + r + 1;
          // numbers we skip over (counting by 2s, 5s, 10s) stay faint, so the pattern shows
          b.cells.push(inSeq[k] ? { key: "n" + k, text: String(k) } : { ghost: true, text: k >= s.from && k <= s.to ? String(k) : "" });
        }
      }
    } else if (mode === "abc") {
      b.cols = 7;
      LETTERS.forEach(function (l) {
        b.cells.push({ key: "l" + l[0], pair: [l[0], l[0].toLowerCase()], pic: l[2] });
      });
    } else {
      b.cols = s.to - s.from + 1;
      for (var t = s.from; t <= s.to; t++) b.head.push("Table of " + t);
      for (var m = 1; m <= 10; m++) {
        for (t = s.from; t <= s.to; t++) b.cells.push({ key: "t" + t + "x" + m, text: t + " × " + m + " = " + (t * m) });
      }
    }
    return b;
  }

  /* ---------- speech ---------- */
  var synth = window.speechSynthesis || null;
  var voice = null;
  function pickVoice() {
    if (!synth) return;
    var vs = synth.getVoices();
    voice = vs.filter(function (v) { return /en[-_]IN/i.test(v.lang); })[0] ||
            vs.filter(function (v) { return /^en/i.test(v.lang); })[0] || null;
  }
  if (synth) { pickVoice(); synth.onvoiceschanged = pickVoice; }

  var lastUtterance = null;   // keep a reference: Chrome can drop onend for collected utterances
  var speechRun = 0, breathTimer = null;

  // speak one string, or a list of parts with a short pause (SPEEDS.breath) between them
  function speak(text, rate, done) {
    var parts = Array.isArray(text) ? text : [text], i = 0, mine = ++speechRun;
    function next() {
      if (mine !== speechRun) return;
      if (i >= parts.length) { if (done) done(); return; }
      speakOne(parts[i++], rate, function () {
        if (mine !== speechRun) return;
        if (i < parts.length) breathTimer = setTimeout(next, SPEEDS[speed].breath);
        else next();
      });
    }
    next();
  }

  function hush() {
    speechRun++;
    clearTimeout(breathTimer);
    if (synth) synth.cancel();
  }

  function speakOne(text, rate, done) {
    var finished = false, safety;
    function fin() {
      if (finished) return;
      finished = true;
      clearTimeout(safety);
      if (done) done();
    }
    if (!synth) { safety = setTimeout(fin, 900); return; }
    synth.cancel();
    var u = new SpeechSynthesisUtterance(text);
    if (voice) u.voice = voice;
    u.lang = voice ? voice.lang : "en-IN";
    u.rate = rate; u.pitch = 1.1;
    u.onend = fin; u.onerror = fin;
    lastUtterance = u;
    synth.speak(u);
    safety = setTimeout(fin, 9000);   // never get stuck if the browser forgets to say it ended
  }

  /* ---------- page ---------- */
  var mount, stage, playBtn, showBtn, settingsBox, whyBox, boardBox;
  var mode = "count", speed = "slow";
  var settings = {
    count:  { from: 1, to: 100, by: 1, style: "teach", say: "number" },
    abc:    { style: "teach" },
    tables: { from: 2, to: 5, style: "teach", order: "order" }
  };
  var items = [], idx = 0, playing = false, token = 0, timer = null;
  var revealed = false;   // Ask me: has the current answer been shown yet?
  var cellEls = {}, settled = {}, nowCell = null;

  function waiting(it) { return it && it.ask && !revealed; }
  function plainOf(it) { return it && it.ask ? it.answer : it; }

  /* ---------- board drawing and settling ---------- */
  function drawBoard() {
    var b = buildBoard(mode, settings[mode]);
    boardBox.innerHTML = "";
    boardBox.className = "sa-board sa-board-" + b.cls;
    boardBox.style.setProperty("--cols", b.cols);
    cellEls = {}; settled = {}; nowCell = null;
    b.head.forEach(function (h) { boardBox.appendChild(el("div", "sa-cell head", h)); });
    b.cells.forEach(function (c) {
      var d = el("div", "sa-cell" + (c.ghost ? " ghost" : ""));
      if (c.ghost) { d.textContent = c.text; boardBox.appendChild(d); return; }
      if (c.pair) {
        d.appendChild(el("span", "sa-cell-pic", c.pic));
        d.appendChild(el("span", "sa-cell-pair", c.pair[0] + " " + c.pair[1]));
      } else {
        d.appendChild(el("span", "sa-cell-text", c.text));
      }
      cellEls[c.key] = d;
      boardBox.appendChild(d);
    });
  }

  function markNow(i) {
    if (nowCell) nowCell.classList.remove("now");
    var p = plainOf(items[i]);
    nowCell = p && p.cell ? cellEls[p.cell] : null;
    if (nowCell) nowCell.classList.add("now");
  }

  // item i has been fully shown: send it to its place on the board
  function settle(i, animate) {
    var p = plainOf(items[i]), cell = p && p.cell ? cellEls[p.cell] : null;
    if (!cell || settled[p.cell]) return;
    settled[p.cell] = true;
    var color = COLORS[i % COLORS.length];
    function land() { cell.classList.add("on"); cell.style.color = color; }
    var from = stage.querySelector(".sa-big"), dur = Math.min(600, SPEEDS[speed].gap);
    var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!animate || !from || dur < 150 || calm || !from.animate) { land(); return; }
    var a = from.getBoundingClientRect(), z = cell.getBoundingClientRect();
    var flyer = from.cloneNode(true);
    flyer.classList.add("sa-fly");
    flyer.style.cssText += ";position:fixed;margin:0;left:" + a.left + "px;top:" + a.top + "px;width:" + a.width +
      "px;height:" + a.height + "px;font-size:" + getComputedStyle(from).fontSize;
    document.body.appendChild(flyer);
    var dx = (z.left + z.width / 2) - (a.left + a.width / 2), dy = (z.top + z.height / 2) - (a.top + a.height / 2);
    var sc = Math.max(0.08, Math.min(z.width / a.width, z.height / a.height));
    var anim = flyer.animate([
      { transform: "translate(0,0) scale(1)", opacity: 1 },
      { transform: "translate(" + dx + "px," + dy + "px) scale(" + sc + ")", opacity: 0.6 }
    ], { duration: dur, easing: "cubic-bezier(.55,0,.3,1)" });
    var landed = false;
    function done() { if (landed) return; landed = true; flyer.remove(); land(); }
    anim.onfinish = anim.oncancel = done;
    setTimeout(done, dur + 150);   // animations can stall (e.g. a hidden tab) — land it anyway
  }

  function render(i, ready) {
    var it = items[i];
    stage.innerHTML = "";
    showBtn.disabled = !waiting(it) || !!ready;
    markNow(i);
    if (!it) { stage.className = "sa-stage"; return; }
    var asking = waiting(it), show = it.ask && !asking ? it.answer : it;
    var text = asking ? it.qLine + "?" : show.big;
    stage.className = "sa-stage" + (ready ? " ready" : "") + (show.title ? " title" : "") +
      (!show.title && text.length > 6 ? " long" : "") +   // "6 × 10 = 60" needs a smaller size to fit
      (asking && !ready ? " asking" : "");

    var big = el("div", "sa-big");
    if (!show.title) big.style.color = COLORS[i % COLORS.length];
    if (asking) {
      big.appendChild(document.createTextNode(it.qLine));
      big.appendChild(el("span", "sa-ans", "?"));
    } else if (show.pair) {
      // two letters side by side with a real gap, so "C c" doesn't read as one mark
      big.className += " sa-pair";
      big.appendChild(el("span", null, show.pair[0]));
      big.appendChild(el("span", null, show.pair[1]));
    } else if (show.line) {
      big.appendChild(document.createTextNode(show.line));
      big.appendChild(el("span", "sa-ans" + (it.ask ? " shown" : ""), String(show.ans)));
    } else {
      big.textContent = show.big;
    }
    if (!asking && show.pic) stage.appendChild(el("div", "sa-pic", show.pic));
    stage.appendChild(big);
    if (!asking && show.word) stage.appendChild(el("div", "sa-word", show.word));
    if (ready) stage.appendChild(el("div", "sa-hint", "Press ▶ to start"));
  }

  function showDone() {
    showBtn.disabled = true;
    markNow(-1);
    stage.innerHTML = "";
    stage.className = "sa-stage done";
    stage.appendChild(el("div", "sa-pic", "🎉"));
    stage.appendChild(el("div", "sa-big", "Well done!"));
  }

  function setPlaying(p) {
    playing = p;
    playBtn.textContent = p ? "⏸ Pause" : (idx > 0 && idx < items.length ? "▶ Go on" : "▶ Start");
    playBtn.classList.toggle("on", p);
  }

  function step() {
    var mine = token, it = items[idx];
    if (it.ask && revealed) { reveal(mine); return; }   // resumed on an answer already shown
    render(idx);
    speak(it.ask ? it.qSay : it.say, SPEEDS[speed].rate, function () {
      if (mine !== token || !playing) return;
      if (it.ask) return;   // wait for 👀 Show answer (or a tap on the card) — never by itself
      settle(idx, true);
      advance(mine);
    });
  }

  function reveal(mine) {
    revealed = true;
    render(idx);
    speak(items[idx].answer.say, SPEEDS[speed].rate, function () {
      if (mine !== token || !playing) return;
      settle(idx, true);
      advance(mine);
    });
  }

  function advance(mine) {
    if (idx >= items.length - 1) { finish(); return; }
    timer = setTimeout(function () {
      if (mine !== token || !playing) return;
      idx++;
      revealed = false;
      step();
    }, SPEEDS[speed].gap);
  }

  function play() {
    if (idx >= items.length) { idx = 0; revealed = false; drawBoard(); }   // playing again: empty board
    token++;
    setPlaying(true);
    step();
  }

  function stop() {
    token++;
    clearTimeout(timer);
    hush();
    setPlaying(false);
  }

  function finish() {
    idx = items.length;
    setPlaying(false);
    showDone();
    speak("Well done!", SPEEDS[speed].rate);
  }

  // tapping the card (or ⏭ / →) on a hidden Ask me answer shows it — and, while playing,
  // the next question follows by itself
  function showAnswer() {
    var was = playing;
    stop();
    if (was) { setPlaying(true); reveal(token); return; }
    revealed = true;
    render(idx);
    var i = idx;
    speak(items[i].answer.say, SPEEDS[speed].rate, function () { if (!playing && idx === i) settle(i, true); });
  }

  function jump(d) {
    if (d > 0 && waiting(items[idx])) { showAnswer(); return; }
    var was = playing;
    stop();
    if (idx < items.length && !waiting(items[idx])) settle(idx, false);   // leaving a shown item: it goes to its place
    idx = Math.max(0, Math.min(items.length - 1, (idx >= items.length ? items.length - 1 : idx) + d));
    revealed = false;
    if (was) { play(); return; }
    render(idx);
    var it = items[idx];
    speak(it.ask ? it.qSay : it.say, SPEEDS[speed].rate);
  }

  function restart() {
    stop();
    idx = 0;
    revealed = false;
    drawBoard();
    play();
  }

  function rebuild() {
    stop();
    items = buildItems(mode, settings[mode]);
    idx = 0;
    revealed = false;
    drawBoard();
    render(0, true);
    setPlaying(false);
  }

  /* ---------- controls ---------- */
  function select(label, values, current, onChange) {
    var wrap = el("label", "sa-field");
    wrap.appendChild(el("span", null, label));
    var s = el("select");
    values.forEach(function (v) {
      var o = el("option", null, String(v[1] != null ? v[1] : v));
      o.value = String(v[0] != null ? v[0] : v);
      if (+o.value === current) o.selected = true;
      s.appendChild(o);
    });
    s.addEventListener("change", function () { onChange(+s.value); });
    wrap.appendChild(s);
    return wrap;
  }
  function chips(cls, list, current, onPick) {
    var box = el("div", "sa-chips " + cls);
    list.forEach(function (c) {
      var b = el("button", "sa-chip" + (c[0] === current ? " on" : ""), c[1]);
      b.type = "button";
      b.addEventListener("click", function () { onPick(c[0]); });
      box.appendChild(b);
    });
    return box;
  }

  function drawSettings() {
    settingsBox.innerHTML = "";
    var s = settings[mode];

    var row1 = el("div", "sa-row");
    row1.appendChild(chips("sa-style", STYLES, s.style, function (v) { s.style = v; drawSettings(); drawWhy(); rebuild(); }));
    if (mode === "count") {
      row1.appendChild(chips("sa-say", [["number", "🔊 Say: 23"], ["digits", "🔊 Say: 2 · 3 · 23"]], s.say, function (v) {
        s.say = v; drawSettings(); rebuild();
      }));
    }
    settingsBox.appendChild(row1);
    showBtn.hidden = s.style !== "ask";

    var row2 = el("div", "sa-row");
    if (mode === "count") {
      row2.appendChild(select("From", range(1, 91, 10), s.from, function (v) {
        s.from = v; if (s.to < v) s.to = Math.min(100, v + 9); drawSettings(); rebuild();
      }));
      row2.appendChild(select("To", range(10, 100, 10), s.to, function (v) {
        s.to = v; if (s.from > v) s.from = Math.max(1, v - 9); drawSettings(); rebuild();
      }));
      row2.appendChild(select("Count by", [[1, "1s"], [2, "2s"], [5, "5s"], [10, "10s"]], s.by, function (v) {
        s.by = v; rebuild();
      }));
    } else if (mode === "tables") {
      row2.appendChild(select("Table of", range(1, 10), s.from, function (v) {
        s.from = v; if (s.to < v) s.to = v; drawSettings(); rebuild();
      }));
      row2.appendChild(select("Up to", range(1, 10), s.to, function (v) {
        s.to = v; if (s.from > v) s.from = v; drawSettings(); rebuild();
      }));
      row2.appendChild(select("Order", [[0, "1 → 10"], [1, "Mixed up"]], s.order === "mixed" ? 1 : 0, function (v) {
        s.order = v ? "mixed" : "order"; rebuild();
      }));
    } else {
      row2.appendChild(el("span", "sa-note", "A to Z, each with a picture word"));
    }
    var speeds = Object.keys(SPEEDS).map(function (k) { return [k, SPEEDS[k].label]; });
    row2.appendChild(chips("sa-speeds", speeds, speed, function (v) { speed = v; drawSettings(); }));
    settingsBox.appendChild(row2);
  }

  function drawWhy() {
    whyBox.innerHTML = "";
    whyBox.appendChild(el("summary", null, "📘 For the grown-up: how to use it, and why"));
    var ul = el("ul");
    MODES[mode].why.forEach(function (w) {
      var li = el("li");
      li.appendChild(el("strong", null, w[0]));
      var why = el("div", "ll-why");
      why.appendChild(el("b", null, "Why: "));
      why.appendChild(document.createTextNode(w[1]));
      li.appendChild(why);
      ul.appendChild(li);
    });
    whyBox.appendChild(ul);
  }

  function setMode(m, push) {
    if (!MODES[m]) m = "count";
    mode = m;
    if (push) history.replaceState(null, "", "say-along.html?m=" + m);
    document.title = MODES[m].name + " — Say-along — Little Learners";
    Array.prototype.forEach.call(document.querySelectorAll(".sa-tab"), function (t) {
      t.classList.toggle("on", t.getAttribute("data-m") === m);
    });
    drawSettings();
    drawWhy();
    rebuild();
  }

  function init() {
    mount = document.getElementById("sa");
    if (!mount) return;
    mount.innerHTML = "";

    // 🌙 / ☀️ next to the page links; the head script already applied the saved or system theme
    var nav = document.querySelector(".nav-toggle");
    if (nav) {
      var th = el("button", "sa-theme");
      th.type = "button";
      var paint = function () {
        var dark = document.documentElement.getAttribute("data-theme") === "dark";
        th.textContent = dark ? "☀️" : "🌙";
        th.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
        th.title = th.getAttribute("aria-label");
      };
      th.addEventListener("click", function () {
        var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try { window.localStorage.setItem("sa-theme", next); } catch (e) {}
        paint();
      });
      paint();
      nav.parentNode.insertBefore(th, nav.nextSibling);
    }

    var tabs = el("div", "sa-tabs");
    Object.keys(MODES).forEach(function (k) {
      var b = el("button", "sa-tab", MODES[k].emoji + " " + MODES[k].name);
      b.type = "button";
      b.setAttribute("data-m", k);
      b.addEventListener("click", function () { setMode(k, true); });
      tabs.appendChild(b);
    });
    mount.appendChild(tabs);

    settingsBox = el("div", "sa-settings");
    mount.appendChild(settingsBox);

    // left: the big card and its buttons; right: the board everything settles into
    var main = el("div", "sa-main"), left = el("div", "sa-left");
    main.appendChild(left);
    mount.appendChild(main);

    stage = el("div", "sa-stage");
    stage.setAttribute("aria-live", "polite");
    stage.addEventListener("click", function () {   // tap the card to show a hidden Ask me answer
      if (waiting(items[idx]) && stage.className.indexOf("ready") < 0) showAnswer();
    });
    left.appendChild(stage);

    var ctl = el("div", "sa-controls");
    function btn(text, label, fn, cls) {
      var b = el("button", "sa-btn" + (cls ? " " + cls : ""), text);
      b.type = "button";
      b.setAttribute("aria-label", label);
      b.addEventListener("click", fn);
      ctl.appendChild(b);
      return b;
    }
    btn("⏮", "Back one", function () { jump(-1); });
    playBtn = btn("▶ Start", "Start or pause", function () { playing ? stop() : play(); }, "main");
    showBtn = btn("👀 Show answer", "Show the answer", function () { if (waiting(items[idx])) showAnswer(); }, "show");
    btn("⏭", "Next one", function () { jump(1); });
    btn("↺", "Start over", restart);
    left.appendChild(ctl);

    boardBox = el("div", "sa-board");
    boardBox.setAttribute("aria-label", "Everything so far, in its place");
    main.appendChild(boardBox);

    if (!synth) mount.appendChild(el("p", "sa-note", "This browser can’t speak, so it will just show each one — read them out together!"));

    whyBox = el("details", "ll-parent");
    mount.appendChild(whyBox);

    document.addEventListener("keydown", function (e) {
      if (e.target && /^(SELECT|INPUT|TEXTAREA|BUTTON)$/.test(e.target.tagName) && e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      if (e.key === " ") { e.preventDefault(); playing ? stop() : play(); }
      else if (e.key === "ArrowRight" || e.key === "Enter") { e.preventDefault(); jump(1); }
      else if (e.key === "ArrowLeft") jump(-1);
    });

    setMode(new URLSearchParams(location.search).get("m") || "count", false);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
