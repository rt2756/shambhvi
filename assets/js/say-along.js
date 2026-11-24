/* Say-along — the screen shows one big thing at a time and reads it aloud, then moves on.
   Part of Little Learners (ages 4–6). One page, say-along.html, six modes chosen by ?m=:
     count   1, 2, 3 … (from / to / count-by / up or down)   say: "21"  (or "2 … 1 … 21")
     abc     A a  🍎 Apple                                     say: "Ay" … "Ay for Apple"
     tables  6 × 2 = 12  (tables 1–20)                         say: "6 twos are 12"
     varna   क  🕊️ कबूतर  (Hindi alphabet, in Hindi)            say: "क" … "क से कबूतर"
     ginti   21  इक्कीस  (Hindi numbers 1–100, in Hindi)        say: "इक्कीस"
     cal     Monday … / January …                              say: "Monday"
   Every mode has two styles:
     👩‍🏫 Teach me  shows and says each one in turn.
     🙋 Ask me    hides the next one ("5 → ?", "B → ?", "3 × 5 = ?"), asks for it, and waits —
                  it shows the answer only when the grown-up presses 👀 Show answer (or taps the card).
   Each item, once said, flies to its place on the board on the right (a hundred chart, the
   A–Z or वर्णमाला chart, the tables side by side, a week or a year).
   Tables are read as groups ("six twos are twelve" = six lots of two), the way they are
   chanted in Indian classrooms, so the words carry the meaning, not just the sound.
   Speech is the browser's own (speechSynthesis): an Indian-English voice, and a Hindi voice
   for the Hindi modes. The next item starts only after the current one has been spoken,
   plus a pause set by the speed buttons. */
(function () {
  "use strict";

  /* ---------- data ---------- */
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

  // Hindi वर्णमाला, in the order (and rows) Hindi books print it. Picture words are chosen to
  // have a matching picture; ङ ञ ण अः have none (almost no everyday word starts with them).
  var VARNA = [
    { name: "स्वर · vowels", rows: [[
      ["अ", "अनानास", "🍍"], ["आ", "आम", "🥭"], ["इ", "इंजन", "🚂"], ["ई", "ईंट", "🧱"], ["उ", "उल्लू", "🦉"],
      ["ऊ", "ऊन", "🧶"], ["ऋ", "ऋषि", "🧘"], ["ए", "एक", "1️⃣"], ["ऐ", "ऐनक", "👓"], ["ओ", "ओस", "💧"],
      ["औ", "औरत", "👩"], ["अं", "अंगूर", "🍇"], ["अः"]
    ]] },
    { name: "व्यंजन · consonants", rows: [
      [["क", "कबूतर", "🕊️"], ["ख", "खरगोश", "🐇"], ["ग", "गमला", "🪴"], ["घ", "घड़ी", "⌚"], ["ङ"]],
      [["च", "चम्मच", "🥄"], ["छ", "छतरी", "☂️"], ["ज", "जहाज़", "🚢"], ["झ", "झंडा", "🇮🇳"], ["ञ"]],
      [["ट", "टमाटर", "🍅"], ["ठ", "ठेला", "🛒"], ["ड", "डमरू", "🪘"], ["ढ", "ढोल", "🥁"], ["ण"]],
      [["त", "तरबूज़", "🍉"], ["थ", "थैला", "🛍️"], ["द", "दरवाज़ा", "🚪"], ["ध", "धनुष", "🏹"], ["न", "नल", "🚰"]],
      [["प", "पतंग", "🪁"], ["फ", "फल", "🍌"], ["ब", "बतख़", "🦆"], ["भ", "भालू", "🐻"], ["म", "मछली", "🐟"]],
      [["य", "यज्ञ", "🔥"], ["र", "रस्सी", "🪢"], ["ल", "लोमड़ी", "🦊"], ["व", "वन", "🌳"]],
      [["श", "शेर", "🦁"], ["ष", "षट्कोण", "⬡"], ["स", "सेब", "🍎"], ["ह", "हाथी", "🐘"]],
      [["क्ष", "क्षत्रिय", "⚔️"], ["त्र", "त्रिशूल", "🔱"], ["ज्ञ", "ज्ञानी", "🧑‍🏫"]]
    ] }
  ];
  var VARNA_LIST = [];
  VARNA.forEach(function (g) { g.rows.forEach(function (r) { r.forEach(function (l) { VARNA_LIST.push(l); }); }); });

  // Hindi number names 1–100 (index = number). Some books spell a few differently
  // (छः / छह, चवालीस / चौवालीस, सड़सठ / सरसठ) — both are right.
  var HINDI_NUM = ("_ एक दो तीन चार पाँच छह सात आठ नौ दस " +
    "ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस बीस " +
    "इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस " +
    "इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस अड़तीस उनतालीस चालीस " +
    "इकतालीस बयालीस तैंतालीस चवालीस पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास " +
    "इक्यावन बावन तिरपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ साठ " +
    "इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ अड़सठ उनहत्तर सत्तर " +
    "इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी अस्सी " +
    "इक्यासी बयासी तिरासी चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी नब्बे " +
    "इक्यानवे बानवे तिरानवे चौरानवे पचानवे छियानवे सत्तानवे अट्ठानवे निन्यानवे सौ").split(" ");
  var DEVA_DIGITS = "०१२३४५६७८९";
  function devaDigits(n) { return String(n).replace(/\d/g, function (d) { return DEVA_DIGITS[+d]; }); }

  var EN_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
  var EN_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
  function numberName(n) {
    if (n === 100) return "one hundred";
    if (n < 20) return EN_ONES[n];
    var t = Math.floor(n / 10), o = n % 10;
    return EN_TENS[t] + (o ? "-" + EN_ONES[o] : "");
  }

  var GROUPS_OF = ["", "ones", "twos", "threes", "fours", "fives", "sixes", "sevens", "eights", "nines", "tens"];
  var ONE_OF    = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];

  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"];

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
        ["↓ Down counts backwards (20, 19, 18 …).", "Counting back is taking away one at a time — the start of subtraction — and it checks the child knows the order itself, not just the sing-song from 1."],
        ["🙋 Ask me shows “5 → ?”: the child says what comes next, then you tap to see it.", "Knowing what comes after 5 without starting again from 1 is the real test of number order — it is exactly what “one more than” sums need."],
        ["🔊 Say: 2 · 3 · 23 reads the digits first, then the number.", "It shows that 23 is written with a 2 and a 3 — the first step to tens and ones. The chart on the right shows it too: each column is one ten (1–10, 11–20 …), and every number in a row ends in the same digit — each step to the right is 10 more."],
        ["🔤 + word writes the number name under it (twenty-one).", "Class 1–2 worksheets ask children to read and write number names; seeing the word while hearing it is how the spelling goes in."]
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
        ["Use 👩‍🏫 Teach me first, then 🙋 Ask me: it says “3 fives are…?”, the child answers, then you tap to see it.", "Pulling an answer out of memory is what makes it stick — much more than hearing it again — and the reveal straight after tells the child at once whether they were right. Mixed up order stops them just counting on from the line before."],
        ["Tables 11 to 20: 13 × 4 is 10 × 4 plus 3 × 4.", "Every number from 11 to 20 is ten and a bit, so its table is the 10 table plus a small table the child already knows: 40 + 12 = 52. That is why the big tables come after 1–10."]
      ]
    },
    varna: {
      name: "वर्णमाला", emoji: "अ", lang: "hi", done: "शाबाश!",
      why: [
        ["Say the letter, then the word: “क … क से कबूतर”.", "The word gives the letter a sound to hang on — कबूतर starts with the क sound — the same trick as “B for Ball”."],
        ["The chart is laid out the way Hindi books print it: स्वर (vowels) first, then व्यंजन (consonants) in rows of five.", "Each row of five is said in the same part of the mouth — क ख ग घ ङ at the back of the throat, प फ ब भ म with the lips. Seeing the rows lets the child hear the pattern, so 33 consonants become a few families instead of one long list."],
        ["ङ, ञ, ण and अः have no picture word.", "Almost no everyday word starts with them — they mostly come inside words — so the chart just shows the letter. Say its sound together."],
        ["🙋 Ask me: “क के बाद क्या आता है?” — what comes after क?", "Recalling the next letter before seeing it is what fixes the order in memory."]
      ]
    },
    ginti: {
      name: "गिनती", emoji: "१", lang: "hi", done: "शाबाश!",
      why: [
        ["Hindi number names past 20 have no easy rule — they are learnt by saying them often.", "In English, 21–29 are all “twenty-something”; in Hindi each has its own name (इक्कीस, बाईस, तेईस …). Hearing and saying them every day is the only way in, which is exactly what this is for."],
        ["One rule does help: उन- means “one less”.", "उनतीस (29) is one less than तीस (30), उनचास (49) one less than पचास (50). Most numbers ending in 9 are named from the next ten this way — except 89, नवासी, and 99, निन्यानवे. Point it out once and ten hard words become one idea."],
        ["Switch the numerals to १ २ ३ to learn the Hindi digits too.", "Hindi books and some signs use them; the shapes are new even when the number is already known."],
        ["Some books spell a few differently (छः / छह, चवालीस / चौवालीस).", "Both are right — use whichever your child's school book uses."]
      ]
    },
    cal: {
      name: "Days & months", emoji: "📅",
      why: [
        ["Say the days every morning, starting from today.", "Days and months are a fixed order, like counting. Saying them from today (not always from Sunday) shows that the week goes round and round."],
        ["🙋 Ask me: “What comes after Monday?”", "Answering without singing from the start checks the child knows the order itself."],
        ["Find birthdays and festivals on the months chart.", "Hanging a month on something the child cares about gives the list a meaning, so it is remembered."]
      ]
    }
  };
  function lang() { return MODES[mode].lang || "en"; }

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
     A plain item: { big, say, cell, pic?, word?, pair? (two letters), line?+ans? (table row) }
     An Ask me item: { ask: true, qLine: "5 → ", qSay: "What comes after 5?", answer: plain item } */

  // turn an ordered list of plain items into Ask me items: the first one is shown, so the
  // child has somewhere to start; each later one is asked as "what comes after the one before"
  function askChain(plains, ask, label, question) {
    if (!ask) return plains;
    return plains.map(function (p, i) {
      if (i === 0) return p;
      var prev = plains[i - 1];
      return { ask: true, qLine: label(prev) + " → ", qSay: question(prev), answer: p };
    });
  }

  // the numbers counted, in the order they are said
  function countSeq(s) {
    var step = s.by || 1, start = step > 1 ? Math.ceil(s.from / step) * step : s.from, list = [];
    for (var n = start; n <= s.to; n += step) list.push(n);
    return s.dir === "down" ? list.reverse() : list;
  }

  function buildItems(mode, s) {
    var ask = s.style === "ask", down = s.dir === "down";
    if (mode === "count") {
      return askChain(countSeq(s).map(function (n) {
        // "Digits, then number": 23 is read "2 … 3 … 23", so the child hears the two digits
        // that make the number before its name (single digits are just said once)
        var say = s.say === "digits" && n >= 10 ? String(n).split("").concat([String(n)]) : String(n);
        return { n: n, big: String(n), say: say, cell: "n" + n, word: s.word === "on" ? numberName(n) : null };
      }), ask, function (p) { return p.big; }, function (p) {
        return (down ? "What comes before " : "What comes after ") + p.n + "?";
      });
    }
    if (mode === "ginti") {
      var show = s.digits === "deva" ? devaDigits : String;
      return askChain(countSeq(s).map(function (n) {
        return { n: n, big: show(n), say: HINDI_NUM[n], cell: "g" + n, word: HINDI_NUM[n] };
      }), ask, function (p) { return p.big; }, function (p) {
        return HINDI_NUM[p.n] + (down ? " से पहले क्या आता है?" : " के बाद क्या आता है?");
      });
    }
    if (mode === "abc") {
      return askChain(LETTERS.map(function (l) {
        var name = letterName(l[0]);
        // two parts, spoken with a pause between: "C" … "C for Cat"
        return { l: l[0], pair: [l[0], l[0].toLowerCase()], big: l[0] + " " + l[0].toLowerCase(), pic: l[2], word: l[1],
                 say: [name, name + " for " + l[1]], cell: "l" + l[0] };
      }), ask, function (p) { return p.l; }, function (p) { return "What comes after " + letterName(p.l) + "?"; });
    }
    if (mode === "varna") {
      return askChain(VARNA_LIST.map(function (l) {
        // "क" … "क से कबूतर"; letters with no picture word are just said
        return { l: l[0], big: l[0], pic: l[2] || null, word: l[1] || null,
                 say: l[1] ? [l[0], l[0] + " से " + l[1]] : l[0], cell: "v" + l[0] };
      }), ask, function (p) { return p.l; }, function (p) { return p.l + " के बाद क्या आता है?"; });
    }
    if (mode === "cal") {
      var names = s.what === "months" ? MONTHS : DAYS;
      return askChain(names.map(function (w) {
        return { w: w, big: w, say: w, cell: "c" + w };
      }), ask, function (p) { return p.w; }, function (p) { return "What comes after " + p.w + "?"; });
    }
    // tables
    var out = [];
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
    return out;
  }

  /* ---------- the board: every item of the range, in its place ----------
     Each spoken item flies across and settles into its own cell, so by the end the whole
     chart is filled in. Cells have the same key as their item. Cell kinds:
       { key, text } / { key, pair, pic } / { key, letter, pic }   a place an item settles into
       { ghost, text }   a faint number that is skipped over (counting by 2s, 5s, 10s)
       { label }         a row or column heading   { section }   a heading across the board
       { filler }        an empty space, to keep rows lined up */
  function hundredBoard(b, s, prefix, show) {
    var inSeq = {};
    countSeq(s).forEach(function (n) { inSeq[n] = true; });
    // one column per ten, filled top to bottom: 1–10 down the first column, 11–20 down the
    // next. Cells are added row by row, so row r, column c holds (d0 + c) × 10 + r + 1.
    var d0 = Math.floor((s.from - 1) / 10), d1 = Math.ceil(s.to / 10) - 1;
    b.cols = d1 - d0 + 1;
    for (var r = 0; r < 10; r++) {
      for (var c = d0; c <= d1; c++) {
        var k = c * 10 + r + 1;
        b.cells.push(inSeq[k] ? { key: prefix + k, text: show(k) } : { ghost: true, text: k >= s.from && k <= s.to ? show(k) : "" });
      }
    }
  }

  function buildBoard(mode, s) {
    var b = { cls: mode, cols: 10, cells: [] };
    if (mode === "count") {
      hundredBoard(b, s, "n", String);
    } else if (mode === "ginti") {
      hundredBoard(b, s, "g", s.digits === "deva" ? devaDigits : String);
    } else if (mode === "abc") {
      b.cols = 7;
      LETTERS.forEach(function (l) { b.cells.push({ key: "l" + l[0], pair: [l[0], l[0].toLowerCase()], pic: l[2] }); });
    } else if (mode === "varna") {
      // स्वर in rows of five, then each consonant family on its own row
      b.cols = 5;
      VARNA.forEach(function (g) {
        b.cells.push({ section: g.name });
        g.rows.forEach(function (row) {
          row.forEach(function (l) { b.cells.push({ key: "v" + l[0], letter: l[0], pic: l[2] || "" }); });
          for (var f = row.length % 5; f && f < 5; f++) b.cells.push({ filler: true });
        });
      });
    } else if (mode === "cal") {
      var names = s.what === "months" ? MONTHS : DAYS;
      b.cols = s.what === "months" ? 4 : 7;
      names.forEach(function (w) { b.cells.push({ key: "c" + w, text: s.what === "months" ? w : w.slice(0, 3) }); });
    } else {
      // tables: one column per table. Up to 5 tables fit whole rows ("6 × 3 = 18"); with
      // more, the cells show just the answer, with the table at the top and × 1 … × 10 down the side
      var n = s.to - s.from + 1, t, m;
      if (n <= 5) {
        b.cols = n;
        for (t = s.from; t <= s.to; t++) b.cells.push({ label: "Table of " + t });
        for (m = 1; m <= 10; m++) for (t = s.from; t <= s.to; t++) b.cells.push({ key: "t" + t + "x" + m, text: t + " × " + m + " = " + (t * m) });
      } else {
        b.cls += " compact";
        b.cols = n + 1;
        b.cells.push({ label: "×" });
        for (t = s.from; t <= s.to; t++) b.cells.push({ label: String(t) });
        for (m = 1; m <= 10; m++) {
          b.cells.push({ label: "× " + m });
          for (t = s.from; t <= s.to; t++) b.cells.push({ key: "t" + t + "x" + m, text: String(t * m) });
        }
      }
    }
    return b;
  }

  /* ---------- speech ---------- */
  var synth = window.speechSynthesis || null;
  var voices = { en: null, hi: null };
  function pickVoices() {
    if (!synth) return;
    var vs = synth.getVoices();
    voices.en = vs.filter(function (v) { return /en[-_]IN/i.test(v.lang); })[0] ||
                vs.filter(function (v) { return /^en/i.test(v.lang); })[0] || null;
    voices.hi = vs.filter(function (v) { return /^hi/i.test(v.lang); })[0] || null;
    if (typeof updateVoiceNote === "function") updateVoiceNote();
  }
  if (synth) { pickVoices(); synth.onvoiceschanged = pickVoices; }

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
    var l = lang(), v = voices[l];
    var u = new SpeechSynthesisUtterance(text);
    if (v) u.voice = v;
    u.lang = v ? v.lang : (l === "hi" ? "hi-IN" : "en-IN");
    u.rate = rate; u.pitch = 1.1;
    u.onend = fin; u.onerror = fin;
    lastUtterance = u;
    synth.speak(u);
    safety = setTimeout(fin, 9000);   // never get stuck if the browser forgets to say it ended
  }

  /* ---------- page ---------- */
  var mount, stage, playBtn, showBtn, settingsBox, whyBox, boardBox, voiceNote;
  var mode = "count", speed = "slow";
  var settings = {
    count:  { from: 1, to: 100, by: 1, dir: "up", style: "teach", say: "number", word: "off" },
    abc:    { style: "teach" },
    tables: { from: 2, to: 5, style: "teach", order: "order" },
    varna:  { style: "teach" },
    ginti:  { from: 1, to: 100, dir: "up", style: "teach", digits: "latin" },
    cal:    { style: "teach", what: "days" }
  };
  var items = [], idx = 0, playing = false, token = 0, timer = null;
  var revealed = false;   // Ask me: has the current answer been shown yet?
  var cellEls = {}, settled = {}, nowCell = null;

  function waiting(it) { return it && it.ask && !revealed; }
  function plainOf(it) { return it && it.ask ? it.answer : it; }

  // a Hindi mode on a device with no Hindi voice: say so, rather than read Hindi badly or not at all
  function updateVoiceNote() {
    if (!voiceNote) return;
    voiceNote.hidden = !(synth && lang() === "hi" && !voices.hi);
  }

  /* ---------- board drawing and settling ---------- */
  function drawBoard() {
    var b = buildBoard(mode, settings[mode]);
    boardBox.innerHTML = "";
    boardBox.className = "sa-board sa-board-" + b.cls;
    boardBox.style.setProperty("--cols", b.cols);
    cellEls = {}; settled = {}; nowCell = null;
    b.cells.forEach(function (c) {
      var d;
      if (c.section) d = el("div", "sa-cell section", c.section);
      else if (c.label != null) d = el("div", "sa-cell head", c.label);
      else if (c.filler) d = el("div", "sa-cell filler");
      else if (c.ghost) d = el("div", "sa-cell ghost", c.text);
      else {
        d = el("div", "sa-cell");
        if (c.pair) {
          d.appendChild(el("span", "sa-cell-pic", c.pic));
          d.appendChild(el("span", "sa-cell-pair", c.pair[0] + " " + c.pair[1]));
        } else if (c.letter) {
          d.appendChild(el("span", "sa-cell-pic", c.pic));
          d.appendChild(el("span", "sa-cell-letter", c.letter));
        } else {
          d.appendChild(el("span", "sa-cell-text", c.text));
        }
        cellEls[c.key] = d;
      }
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
      (!show.title && (text.length > 6 || show.w) ? " long" : "") +   // "6 × 10 = 60", "Wednesday" need a smaller size
      (asking && !ready ? " asking" : "") + (lang() === "hi" ? " hindi" : "");

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
    stage.appendChild(el("div", "sa-big", MODES[mode].done || "Well done!"));
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
    speak(MODES[mode].done || "Well done!", SPEEDS[speed].rate);
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
      if (o.value === String(current)) o.selected = true;
      s.appendChild(o);
    });
    s.addEventListener("change", function () { onChange(/^\d+$/.test(s.value) ? +s.value : s.value); });
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
  // From / To / Up-Down, shared by Counting and गिनती
  function rangeControls(row, s) {
    row.appendChild(select("From", range(1, 91, 10), s.from, function (v) {
      s.from = v; if (s.to < v) s.to = Math.min(100, v + 9); drawSettings(); rebuild();
    }));
    row.appendChild(select("To", range(10, 100, 10), s.to, function (v) {
      s.to = v; if (s.from > v) s.from = Math.max(1, v - 9); drawSettings(); rebuild();
    }));
    row.appendChild(select("Order", [["up", "↑ Up"], ["down", "↓ Down"]], s.dir, function (v) {
      s.dir = v; rebuild();
    }));
  }

  function drawSettings() {
    settingsBox.innerHTML = "";
    var s = settings[mode];

    var row1 = el("div", "sa-row");
    row1.appendChild(chips("sa-style", STYLES, s.style, function (v) { s.style = v; drawSettings(); rebuild(); }));
    if (mode === "count") {
      row1.appendChild(chips("sa-say", [["number", "🔊 Say: 23"], ["digits", "🔊 Say: 2 · 3 · 23"]], s.say, function (v) {
        s.say = v; drawSettings(); rebuild();
      }));
      row1.appendChild(chips("sa-wordchip", [["off", "23"], ["on", "🔤 23 + word"]], s.word, function (v) {
        s.word = v; drawSettings(); rebuild();
      }));
    }
    settingsBox.appendChild(row1);
    showBtn.hidden = s.style !== "ask";

    var row2 = el("div", "sa-row");
    if (mode === "count") {
      rangeControls(row2, s);
      row2.appendChild(select("Count by", [[1, "1s"], [2, "2s"], [5, "5s"], [10, "10s"]], s.by, function (v) {
        s.by = v; rebuild();
      }));
    } else if (mode === "ginti") {
      rangeControls(row2, s);
      row2.appendChild(select("Numerals", [["latin", "1 2 3"], ["deva", "१ २ ३"]], s.digits, function (v) {
        s.digits = v; rebuild();
      }));
    } else if (mode === "tables") {
      row2.appendChild(select("Table of", range(1, 20), s.from, function (v) {
        s.from = v; if (s.to < v) s.to = v; drawSettings(); rebuild();
      }));
      row2.appendChild(select("Up to", range(1, 20), s.to, function (v) {
        s.to = v; if (s.from > v) s.from = v; drawSettings(); rebuild();
      }));
      row2.appendChild(select("Order", [["order", "1 → 10"], ["mixed", "Mixed up"]], s.order, function (v) {
        s.order = v; rebuild();
      }));
    } else if (mode === "cal") {
      row2.appendChild(chips("sa-what", [["days", "📆 Days of the week"], ["months", "🗓️ Months of the year"]], s.what, function (v) {
        s.what = v; drawSettings(); rebuild();
      }));
    } else if (mode === "varna") {
      row2.appendChild(el("span", "sa-note", "स्वर and व्यंजन, each with a picture word — read in Hindi"));
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
    updateVoiceNote();
    rebuild();
  }

  function init() {
    mount = document.getElementById("sa");
    if (!mount) return;
    mount.innerHTML = "";

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

    voiceNote = el("p", "sa-note sa-voice-note",
      "This device has no Hindi voice, so the Hindi won’t be read out — read each one together. " +
      "(On a computer, Chrome or Edge usually has one; on a phone, add Hindi under text-to-speech settings.)");
    voiceNote.hidden = true;
    left.appendChild(voiceNote);

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
