/* Maths & English — loads topic-per-file Markdown and renders collapsible panels.
   Layouts share this one engine, chosen by the #app element's data-* attributes:
     data-content-dir   where the manifest + .md files live (default content/math/)
     data-mode          "notes" (running cheat sheets), "questions" (numbered Q cards),
                        "vocab" (flashcards: word on front, meaning on tap), or
                        "todo" (notes-style, with tick-off checkboxes saved on the device)
   Content lives in <content-dir>/<topic>.md, listed in <content-dir>/manifest.json.
   No build step: the browser fetches the files and renders them with marked. */
(function () {
  "use strict";

  var DEFAULT_DIR = "content/class7/math/";

  // "🔢 Numbers" -> "numbers"; "➗ Fractions & decimals" -> "fractions-decimals"
  function slugify(text) {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  }

  // GitHub-style alert types -> our .box callout styles + labels.
  var ALERTS = {
    TIP:       { cls: "tip",  label: "💡 Tip" },
    WARNING:   { cls: "warn", label: "⚠️ Common mistakes" },
    CAUTION:   { cls: "warn", label: "⚠️ Common mistakes" },
    NOTE:      { cls: "note", label: "📘 Note" },
    IMPORTANT: { cls: "eg",   label: "📝 Example" }
  };
  var ALERT_RE  = /^\s*\[!(TIP|WARNING|CAUTION|NOTE|IMPORTANT)\]\s*/;
  var ANSWER_RE = /^\s*\[!ANSWER\]\s*/;

  // Strip a leading "[!TYPE]" marker from the first non-empty text node inside el.
  function stripMarker(el, re) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var node = walker.nextNode();
    while (node && node.nodeValue.trim() === "") node = walker.nextNode();
    if (node) node.nodeValue = node.nodeValue.replace(re, "");
  }

  // Rewrite blockquotes that start with "[!TYPE]" into styled callout boxes.
  function upgradeCallouts(root) {
    var quotes = root.querySelectorAll("blockquote");
    for (var i = 0; i < quotes.length; i++) {
      var bq = quotes[i];
      var match = (bq.textContent || "").match(ALERT_RE);
      if (!match) continue;
      var spec = ALERTS[match[1]];

      var box = document.createElement("div");
      box.className = "box " + spec.cls;
      while (bq.firstChild) box.appendChild(bq.firstChild);
      stripMarker(box, ALERT_RE);

      // prepend the label only after the marker is stripped from the content
      var label = document.createElement("span");
      label.className = "label";
      label.textContent = spec.label;
      box.insertBefore(label, box.firstChild);

      bq.parentNode.replaceChild(box, bq);
    }
  }

  // Rewrite "[!ANSWER]" blockquotes into a tap-to-reveal panel. The summary text
  // defaults to "Show answer" (questions); vocab passes "Reveal meaning".
  function upgradeAnswers(root, label) {
    var quotes = root.querySelectorAll("blockquote");
    for (var i = 0; i < quotes.length; i++) {
      var bq = quotes[i];
      if (!ANSWER_RE.test(bq.textContent || "")) continue;

      var details = document.createElement("details");
      details.className = "answer";
      var summary = document.createElement("summary");
      summary.textContent = label || "Show answer";
      details.appendChild(summary);

      var body = document.createElement("div");
      body.className = "answer-body";
      while (bq.firstChild) body.appendChild(bq.firstChild);
      stripMarker(body, ANSWER_RE);
      details.appendChild(body);

      bq.parentNode.replaceChild(details, bq);
    }
  }

  // Split a chapter body into cards on top-level <hr> ("---"). Each card's
  // [!ANSWER] block becomes a tap-to-reveal panel. opts tunes the rendering:
  //   cardClass / bodyClass — CSS hooks; numbered — show a 1,2,3 badge;
  //   revealLabel — summary text for the reveal. Returns { fragment, count } so
  //   an empty file can fall back to a friendly "coming soon" state.
  function toCards(body, opts) {
    var chunks = [[]];
    Array.prototype.forEach.call(body.childNodes, function (node) {
      if (node.nodeType === 1 && node.tagName === "HR") chunks.push([]);
      else chunks[chunks.length - 1].push(node);
    });

    chunks = chunks.filter(function (nodes) {
      return nodes.some(function (n) {
        return n.nodeType === 1 || (n.nodeType === 3 && n.nodeValue.trim() !== "");
      });
    });

    var frag = document.createDocumentFragment();
    chunks.forEach(function (nodes, i) {
      var card = document.createElement("div");
      card.className = opts.cardClass;

      if (opts.numbered) {
        var num = document.createElement("span");
        num.className = "qnum";
        num.textContent = i + 1;
        card.appendChild(num);
      }

      var cbody = document.createElement("div");
      cbody.className = opts.bodyClass;
      nodes.forEach(function (n) { cbody.appendChild(n); });
      upgradeAnswers(cbody, opts.revealLabel);
      card.appendChild(cbody);

      frag.appendChild(card);
    });
    return { fragment: frag, count: chunks.length };
  }

  function emptyState(big, strong, msg) {
    var div = document.createElement("div");
    div.className = "empty";
    var b = document.createElement("div"); b.className = "big"; b.textContent = big;
    var s = document.createElement("strong"); s.textContent = strong;
    div.appendChild(b);
    div.appendChild(s);
    div.appendChild(document.createTextNode(msg));
    return div;
  }

  // markdown text -> { id, title, body } (first H1 becomes the panel title).
  // In questions/vocab mode the body is rebuilt as cards.
  function toTopic(fileName, mdText, mode) {
    var tmp = document.createElement("div");
    tmp.innerHTML = window.marked.parse(mdText);
    var h1 = tmp.querySelector("h1");
    var title = h1 ? h1.textContent.trim() : fileName.replace(/\.md$/, "");
    if (h1) h1.parentNode.removeChild(h1);
    upgradeCallouts(tmp);

    if (mode === "questions") {
      var cards = toCards(tmp, { cardClass: "qcard", bodyClass: "qbody", numbered: true, revealLabel: "Show answer" });
      tmp.innerHTML = "";
      tmp.appendChild(cards.count
        ? cards.fragment
        : emptyState("📝", "Questions coming soon",
            "Practice questions for this chapter haven’t been added yet."));
    } else if (mode === "vocab") {
      var words = toCards(tmp, { cardClass: "vcard", bodyClass: "vbody", numbered: false, revealLabel: "Reveal meaning" });
      tmp.innerHTML = "";
      tmp.appendChild(words.count
        ? words.fragment
        : emptyState("🔤", "Words coming soon",
            "Vocabulary for this level hasn’t been added yet."));
    }
    return { id: slugify(title), title: title, body: tmp };
  }

  function buildToc(topics) {
    var nav = document.createElement("nav");
    nav.className = "toc";
    topics.forEach(function (t) {
      var a = document.createElement("a");
      a.href = "#" + t.id;
      a.textContent = t.title;
      nav.appendChild(a);
    });
    return nav;
  }

  function buildControls(panels) {
    var wrap = document.createElement("div");
    wrap.className = "controls";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "toggle-all";
    var expanded = false;
    function sync() { btn.textContent = expanded ? "Collapse all" : "Expand all"; }
    btn.addEventListener("click", function () {
      expanded = !expanded;
      panels.forEach(function (p) { p.open = expanded; });
      sync();
    });
    sync();
    wrap.appendChild(btn);
    return wrap;
  }

  // How many cards each section reveals per day. Levels show a fresh batch of
  // 14; word roots show a single root. A section with N cards therefore cycles
  // back to the start every ceil(N / batch) days — 14 days when fully stocked
  // (levels = 196 words, roots = 14 roots).
  var WORDS_PER_DAY = 14;
  function batchSizeForTitle(title) {
    return /root/i.test(title) ? 1 : WORDS_PER_DAY;
  }

  // Days elapsed since Jan 0 — stable for the whole calendar day.
  function dayOfYear() {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    return Math.floor((now - start) / 86400000);
  }

  // Reveal only today's batch of cards in one section (hide the rest) and return
  // the batch's first card, used as that section's featured "of the day". The
  // batch advances by one each day and repeats after a full cycle.
  function applyDailyBatch(panel, doy) {
    var cards = panel.querySelectorAll(".vcard");
    if (!cards.length) return null;
    var summaryEl = panel.querySelector("summary");
    var n = batchSizeForTitle(summaryEl ? summaryEl.textContent : "");
    var batches = Math.ceil(cards.length / n);
    var batch = ((doy % batches) + batches) % batches;
    var startIdx = batch * n;
    Array.prototype.forEach.call(cards, function (card, i) {
      card.style.display = (i >= startIdx && i < startIdx + n) ? "" : "none";
    });
    return cards[startIdx] || null;
  }

  // Build a "word of the day" banner that features one card. Clicking it opens
  // that section and scrolls to the word.
  function buildDailyPick(panel, card) {
    if (!card) return null;

    var headEl = card.querySelector("h3, h2, h4, h1");
    var word = headEl ? headEl.textContent.trim() : "";
    if (!word) return null;

    // The first paragraph holds the definition ("Meaning:" / "Origin:"); show
    // it without its label.
    var meaningEl = card.querySelector(".answer-body p");
    var meaning = meaningEl ? meaningEl.textContent.trim() : "";
    meaning = meaning.replace(/^\s*(Meaning|Origin)\s*:\s*/i, "");

    var summaryEl = panel.querySelector("summary");
    var sectionTitle = summaryEl ? summaryEl.textContent.trim() : "";
    var shortName = sectionTitle.split(/[—–-]/)[0].trim();
    var isRoot = /root/i.test(sectionTitle);

    var banner = document.createElement("div");
    banner.className = "wotd clickable";
    var label = document.createElement("span");
    label.className = "wotd-label";
    label.textContent = isRoot
      ? "🌱 Root of the day"
      : "🌟 Word of the day" + (shortName ? " · " + shortName : "");
    var w = document.createElement("strong");
    w.className = "wotd-word";
    w.textContent = word;
    banner.appendChild(label);
    banner.appendChild(w);
    if (meaning) {
      var m = document.createElement("p");
      m.className = "wotd-meaning";
      m.textContent = meaning;
      banner.appendChild(m);
    }

    banner.addEventListener("click", function () {
      panel.open = true;
      card.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    return banner;
  }

  // Reveal today's batch in every section and stack a featured pick per section
  // in a responsive row at the top.
  function buildDailyPicks(panels) {
    var doy = dayOfYear();
    var wrap = document.createElement("div");
    wrap.className = "daily-picks";
    panels.forEach(function (panel) {
      var featured = applyDailyBatch(panel, doy);
      var banner = buildDailyPick(panel, featured);
      if (banner) wrap.appendChild(banner);
    });
    return wrap.children.length ? wrap : null;
  }

  function buildPanel(topic) {
    var details = document.createElement("details");
    details.className = "topic";
    details.id = topic.id;
    var summary = document.createElement("summary");
    summary.textContent = topic.title;
    details.appendChild(summary);
    var body = document.createElement("div");
    body.className = "topic-body";
    while (topic.body.firstChild) body.appendChild(topic.body.firstChild);
    details.appendChild(body);
    return details;
  }

  // Open (and scroll to) the panel named in the URL hash, e.g. #geometry
  function openFromHash() {
    var id = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === "DETAILS") {
      el.open = true;
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function showError(mount, err) {
    mount.innerHTML =
      '<div class="empty">' +
      '<div class="big">📭</div>' +
      "<strong>Couldn’t load this page</strong>" +
      "The content loads from separate files, so open the site with a local server " +
      "(not by double-clicking the file):<br><br>" +
      "<code>python3 -m http.server</code><br>then visit <code>http://localhost:8000</code>" +
      "</div>";
    if (window.console) console.error("[learn]", err);
  }

  // In "todo" mode the Markdown renders like notes, but GFM task-list checkboxes
  // ("- [ ] …") are made interactive and their checked state is remembered in
  // localStorage — keyed by the item's text, so it survives reloads and reordering.
  function wireTodos(root) {
    var boxes = root.querySelectorAll(".topic-body input[type=checkbox]");
    Array.prototype.forEach.call(boxes, function (box) {
      box.disabled = false;
      var li = box.closest("li");
      if (li) {
        li.classList.add("task");
        if (li.parentNode && li.parentNode.tagName === "UL") li.parentNode.classList.add("checklist");
      }
      var key = "todo:" + slugify(li ? li.textContent : (box.value || "")).slice(0, 80);
      try { if (window.localStorage.getItem(key) === "1") box.checked = true; } catch (e) {}
      if (li) li.classList.toggle("done", box.checked);
      box.addEventListener("change", function () {
        if (li) li.classList.toggle("done", box.checked);
        try { window.localStorage.setItem(key, box.checked ? "1" : "0"); } catch (e) {}
      });
    });
  }

  function init() {
    var mount = document.getElementById("app");
    if (!mount) return;
    if (!window.marked) { showError(mount, new Error("marked failed to load")); return; }

    var dir = mount.dataset.contentDir || DEFAULT_DIR;
    var mode = mount.dataset.mode || "notes";

    // { cache: "no-cache" } => always revalidate with the server, so edits to the
    // .md / manifest show up on a normal reload (no hard refresh needed).
    fetch(dir + "manifest.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("manifest.json " + r.status); return r.json(); })
      .then(function (files) {
        return Promise.all(files.map(function (name) {
          return fetch(dir + name, { cache: "no-cache" })
            .then(function (r) { if (!r.ok) throw new Error(name + " " + r.status); return r.text(); })
            .then(function (text) { return toTopic(name, text, mode); });
        }));
      })
      .then(function (topics) {
        var panels = topics.map(buildPanel);
        mount.innerHTML = "";
        mount.appendChild(buildToc(topics));
        mount.appendChild(buildControls(panels));
        panels.forEach(function (p) { mount.appendChild(p); });

        if (mode === "vocab") {
          var picks = buildDailyPicks(panels);
          if (picks) mount.insertBefore(picks, mount.firstChild);
        }

        if (mode === "todo") wireTodos(mount);

        // Clicking a chip opens its panel before the browser scrolls to it.
        mount.addEventListener("click", function (e) {
          var a = e.target.closest && e.target.closest('a[href^="#"]');
          if (!a) return;
          var el = document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1)));
          if (el && el.tagName === "DETAILS") el.open = true;
        });
        window.addEventListener("hashchange", openFromHash);
        openFromHash();
      })
      .catch(function (err) { showError(mount, err); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
