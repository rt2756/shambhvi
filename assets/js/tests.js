/* Chapter tests — self-marking, four levels per chapter.
   One engine drives two pages, chosen by which mount element exists:
     #tests-hub  (class<N>-tests.html)  the grid: every chapter × 4 levels, with saved scores
     #test-run   (test.html?c=7&f=1.integers&t=1)  one test: answer, Submit, then marks +
                 the right answer + a "why" for every question
   Data lives in content/class<N>/tests/<chapter>.json, listed in manifest.json there:
     { "title": "1. Integers",
       "tests": [ { "q": [ ...10 questions... ] }, ×4  (Simple, Hard, Harder, Hardest) ] }
   A question is either multiple choice or a number answer:
     { "t": "question", "o": ["RIGHT answer", "wrong", "wrong", "wrong"], "e": "why" }
     { "t": "question", "n": 42, "u": "cm", "e": "why" }
   The right option is ALWAYS written first; the page shuffles the options (the same
   way every time for a given question), so the answer key can't drift out of step.
   "k" is an optional self-check formula used only by tools/check_tests.py. */
(function () {
  "use strict";

  var LEVELS = [
    { name: "Simple",  icon: "🟢" },
    { name: "Hard",    icon: "🟡" },
    { name: "Harder",  icon: "🟠" },
    { name: "Hardest", icon: "🔴" }
  ];

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function dirFor(cls) { return "content/class" + cls + "/tests/"; }
  function keyFor(cls, file, t) { return "test:" + cls + ":" + file + ":" + t; }

  function loadState(key) {
    try { return JSON.parse(window.localStorage.getItem(key) || "{}") || {}; }
    catch (e) { return {}; }
  }
  function saveState(key, state) {
    try { window.localStorage.setItem(key, JSON.stringify(state)); } catch (e) {}
  }

  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.json();
    });
  }

  function showError(mount, err) {
    mount.innerHTML = '<div class="empty"><div class="big">📭</div>' +
      "<strong>Couldn’t load this test</strong>" +
      "Open the site with a local server (<code>python3 -m http.server</code>) or check the link.</div>";
    if (window.console) console.error("[tests]", err);
  }

  /* ---------- the hub: chapters × levels ---------- */
  function initHub(mount) {
    var cls = mount.dataset.class;
    var dir = dirFor(cls);
    getJSON(dir + "manifest.json")
      .then(function (files) {
        return Promise.all(files.map(function (name) {
          return getJSON(dir + name).then(function (data) {
            return { file: name.replace(/\.json$/, ""), data: data };
          });
        }));
      })
      .then(function (chapters) {
        mount.innerHTML = "";
        var done = 0, total = 0;
        var list = el("div", "test-list");
        chapters.forEach(function (ch) {
          var row = el("div", "test-row");
          row.appendChild(el("div", "test-chapter")).textContent = ch.data.title;
          var btns = el("div", "test-levels");
          (ch.data.tests || []).forEach(function (test, i) {
            var lvl = LEVELS[i] || { name: "Test " + (i + 1), icon: "📝" };
            var a = el("a", "test-btn lvl" + (i + 1));
            a.href = "test.html?c=" + encodeURIComponent(cls) +
              "&f=" + encodeURIComponent(ch.file) + "&t=" + (i + 1);
            var st = loadState(keyFor(cls, ch.file, i + 1));
            total++;
            var score = "";
            if (st.done) {
              done++;
              a.classList.add("done");
              score = '<span class="test-score">' + st.score + " / " + test.q.length + "</span>";
            } else if (st.answers && Object.keys(st.answers).length) {
              score = '<span class="test-score">in progress</span>';
            }
            a.innerHTML = '<span class="test-name">' + lvl.icon + " " + lvl.name + "</span>" + score;
            btns.appendChild(a);
          });
          row.appendChild(btns);
          list.appendChild(row);
        });
        var tally = el("p", "test-tally");
        tally.textContent = done + " of " + total + " tests done";
        mount.appendChild(tally);
        mount.appendChild(list);
      })
      .catch(function (err) { showError(mount, err); });
  }

  /* ---------- one test ---------- */

  // Small seeded generator, so a question's options shuffle the same way on every
  // visit (answers saved before a reload still point at the right option).
  function seeded(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return function () {
      h += 0x6D2B79F5;
      var t = Math.imul(h ^ (h >>> 15), 1 | h);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  // -> array of original option indexes in display order (index 0 is the right one)
  function shuffledOrder(n, seed) {
    var rnd = seeded(seed), order = [];
    for (var i = 0; i < n; i++) order.push(i);
    for (var j = n - 1; j > 0; j--) {
      var k = Math.floor(rnd() * (j + 1));
      var tmp = order[j]; order[j] = order[k]; order[k] = tmp;
    }
    return order;
  }

  // "−3", "1,250", "₹ 40", "3/4", "12.5%" -> number (NaN if it isn't one)
  function toNumber(s) {
    s = String(s == null ? "" : s).replace(/[−–—]/g, "-").replace(/[\s,₹%°]/g, "");
    if (s === "") return NaN;
    var frac = s.match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/);
    if (frac) return Number(frac[1]) / Number(frac[2]);
    return /^-?\d*\.?\d+$/.test(s) ? Number(s) : NaN;
  }
  function showNumber(n) { return String(n).replace("-", "−"); }

  function initRun(mount) {
    var p = new URLSearchParams(location.search);
    var cls = (p.get("c") || "").replace(/[^0-9]/g, "");
    var file = (p.get("f") || "").replace(/[^a-z0-9.\-]/gi, "");
    var t = parseInt(p.get("t"), 10) || 1;
    var hub = "class" + cls + "-tests.html";
    var key = keyFor(cls, file, t);

    getJSON(dirFor(cls) + file + ".json")
      .then(function (data) {
        var test = data.tests[t - 1];
        if (!test) throw new Error("no test " + t);
        var lvl = LEVELS[t - 1] || { name: "Test " + t, icon: "📝" };
        var Q = test.q;
        var state = loadState(key);
        if (!state.answers) state.answers = {};

        document.title = data.title + " — " + lvl.name + " test";
        var h = document.getElementById("test-title");
        if (h) h.textContent = data.title;
        var pill = document.getElementById("test-pill");
        if (pill) pill.textContent = "🎯 Class " + cls + " · Test " + t + " of " + data.tests.length;
        var back = document.getElementById("test-back");
        if (back) back.href = hub;

        mount.innerHTML = "";
        mount.appendChild(el("p", "test-intro",
          "<strong>" + lvl.icon + " " + lvl.name + "</strong> · " + Q.length +
          " questions · 1 mark each · no time limit. Answers save as you go. " +
          "Press <strong>Submit</strong> at the end to see your marks and the explanations."));

        var result = el("div", "test-result");
        result.hidden = true;
        mount.appendChild(result);

        var form = el("form", "test-form");
        form.addEventListener("submit", function (e) { e.preventDefault(); });
        var orders = [];
        Q.forEach(function (q, i) {
          var card = el("div", "qcard tq");
          card.appendChild(el("span", "qnum")).textContent = i + 1;
          var body = el("div", "qbody");
          body.appendChild(el("p", "tq-text", q.t));
          if (q.o) {
            var order = shuffledOrder(q.o.length, key + ":" + i);
            orders[i] = order;
            order.forEach(function (orig, pos) {
              var label = el("label", "opt");
              var input = el("input");
              input.type = "radio"; input.name = "q" + i; input.value = orig;
              if (String(state.answers[i]) === String(orig)) input.checked = true;
              label.appendChild(input);
              label.appendChild(el("span", "opt-text", "(" + "abcd"[pos] + ") " + q.o[orig]));
              body.appendChild(label);
            });
          } else {
            var wrap = el("div", "num-wrap");
            var box = el("input", "num-input");
            box.type = "text"; box.name = "q" + i; box.autocomplete = "off";
            box.placeholder = "Your answer";
            if (state.answers[i] != null) box.value = state.answers[i];
            wrap.appendChild(box);
            if (q.u) wrap.appendChild(el("span", "num-unit")).textContent = q.u;
            body.appendChild(wrap);
          }
          body.appendChild(el("div", "fb"));
          card.appendChild(body);
          form.appendChild(card);
        });
        mount.appendChild(form);

        var bar = el("div", "test-actions");
        var progress = el("span", "test-progress");
        var submitBtn = el("button", "test-submit");
        submitBtn.type = "button"; submitBtn.textContent = "Submit";
        var retryBtn = el("button", "toggle-all");
        retryBtn.type = "button"; retryBtn.textContent = "↻ Try again"; retryBtn.hidden = true;
        var hubLink = el("a", "toggle-all"); hubLink.href = hub; hubLink.textContent = "← All tests";
        bar.appendChild(progress); bar.appendChild(submitBtn);
        bar.appendChild(retryBtn); bar.appendChild(hubLink);
        if (t < data.tests.length) {
          var next = el("a", "toggle-all");
          next.href = "test.html?c=" + cls + "&f=" + encodeURIComponent(file) + "&t=" + (t + 1);
          next.textContent = "Next level →";
          bar.appendChild(next);
        }
        mount.appendChild(bar);

        function collect() {
          var answers = {};
          Q.forEach(function (q, i) {
            if (q.o) {
              var c = form.querySelector('input[name="q' + i + '"]:checked');
              if (c) answers[i] = c.value;
            } else {
              var v = form.querySelector('input[name="q' + i + '"]').value.trim();
              if (v) answers[i] = v;
            }
          });
          return answers;
        }
        function syncProgress() {
          progress.textContent = "Answered " + Object.keys(state.answers).length + " / " + Q.length;
        }

        function mark(scroll) {
          var score = 0, blank = 0;
          Q.forEach(function (q, i) {
            var card = form.children[i], fb = card.querySelector(".fb");
            var given = state.answers[i], ok, answer;
            if (q.o) {
              ok = String(given) === "0";
              answer = "(" + "abcd"[orders[i].indexOf(0)] + ") " + q.o[0];
            } else {
              ok = given != null && Math.abs(toNumber(given) - q.n) < 1e-6;
              answer = showNumber(q.n) + (q.u ? " " + q.u : "");
            }
            if (given == null) blank++;
            if (ok) score++;
            card.classList.add(ok ? "right" : "wrong");
            fb.innerHTML =
              (ok ? '<b class="ok">✓ Correct · 1 mark</b>'
                  : '<b class="bad">✗ ' + (given == null ? "Not answered" : "Wrong") + " · 0 marks</b>") +
              '<div class="fb-answer">Answer: <strong>' + answer + "</strong></div>" +
              '<div class="fb-why"><strong>Why:</strong> ' + q.e + "</div>";
          });
          Array.prototype.forEach.call(form.querySelectorAll("input"), function (x) { x.disabled = true; });
          var pct = Math.round(100 * score / Q.length);
          var cheer = pct === 100 ? "Perfect! 🌟" : pct >= 80 ? "Great work! 🎉" :
                      pct >= 50 ? "Good try — read the explanations for the red ones." :
                                  "Go through each explanation, then try again.";
          result.innerHTML = '<div class="test-marks">' + score + " / " + Q.length + "</div>" +
            "<div>" + cheer + (blank ? " · Left blank: " + blank : "") + "</div>";
          result.hidden = false;
          submitBtn.hidden = true; retryBtn.hidden = false;
          progress.textContent = "Marks: " + score + " / " + Q.length;
          state.done = true; state.score = score;
          saveState(key, state);
          if (scroll) result.scrollIntoView({ behavior: "smooth", block: "center" });
        }

        function onEdit() {
          if (state.done) return;
          state.answers = collect();
          saveState(key, state);
          syncProgress();
        }
        form.addEventListener("input", onEdit);
        form.addEventListener("change", onEdit);
        submitBtn.addEventListener("click", function () {
          if (state.done) return;
          state.answers = collect();
          mark(true);
        });
        retryBtn.addEventListener("click", function () {
          saveState(key, {});
          location.reload();
        });

        syncProgress();
        if (state.done) mark(false);
      })
      .catch(function (err) { showError(mount, err); });
  }

  function init() {
    var hub = document.getElementById("tests-hub");
    if (hub) initHub(hub);
    var run = document.getElementById("test-run");
    if (run) initRun(run);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
