/* Maths — loads topic-per-file Markdown and renders collapsible panels.
   Two layouts share this one engine, chosen by the #app element's data-* attributes:
     data-content-dir   where the manifest + .md files live (default content/math/)
     data-mode          "notes" (running cheat sheets) or "questions" (numbered Q cards)
   Content lives in <content-dir>/<topic>.md, listed in <content-dir>/manifest.json.
   No build step: the browser fetches the files and renders them with marked. */
(function () {
  "use strict";

  var DEFAULT_DIR = "content/math/";

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

  // Rewrite "[!ANSWER]" blockquotes into a tap-to-reveal "Show answer" panel.
  function upgradeAnswers(root) {
    var quotes = root.querySelectorAll("blockquote");
    for (var i = 0; i < quotes.length; i++) {
      var bq = quotes[i];
      if (!ANSWER_RE.test(bq.textContent || "")) continue;

      var details = document.createElement("details");
      details.className = "answer";
      var summary = document.createElement("summary");
      summary.textContent = "Show answer";
      details.appendChild(summary);

      var body = document.createElement("div");
      body.className = "answer-body";
      while (bq.firstChild) body.appendChild(bq.firstChild);
      stripMarker(body, ANSWER_RE);
      details.appendChild(body);

      bq.parentNode.replaceChild(details, bq);
    }
  }

  // questions mode: split a chapter body into numbered question cards.
  // Questions are separated by a top-level <hr> ("---"); each card's [!ANSWER]
  // block becomes a collapsible "Show answer". Returns { fragment, count } so an
  // empty file can fall back to a friendly "coming soon" state.
  function toQuestionCards(body) {
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
      card.className = "qcard";

      var num = document.createElement("span");
      num.className = "qnum";
      num.textContent = i + 1;
      card.appendChild(num);

      var qbody = document.createElement("div");
      qbody.className = "qbody";
      nodes.forEach(function (n) { qbody.appendChild(n); });
      upgradeAnswers(qbody);
      card.appendChild(qbody);

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
  // In questions mode the body is rebuilt as numbered question cards.
  function toTopic(fileName, mdText, mode) {
    var tmp = document.createElement("div");
    tmp.innerHTML = window.marked.parse(mdText);
    var h1 = tmp.querySelector("h1");
    var title = h1 ? h1.textContent.trim() : fileName.replace(/\.md$/, "");
    if (h1) h1.parentNode.removeChild(h1);
    upgradeCallouts(tmp);

    if (mode === "questions") {
      var cards = toQuestionCards(tmp);
      tmp.innerHTML = "";
      tmp.appendChild(cards.count
        ? cards.fragment
        : emptyState("📝", "Questions coming soon",
            "Practice questions for this chapter haven’t been added yet."));
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
    if (window.console) console.error("[maths]", err);
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
