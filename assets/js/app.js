/* Maths notes — loads topic-per-file Markdown and renders collapsible panels.
   Content lives in content/math/<topic>.md, listed in content/math/manifest.json.
   No build step: the browser fetches the files and renders them with marked. */
(function () {
  "use strict";

  var SUBJECT_DIR = "content/math/";

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
  var ALERT_RE = /^\s*\[!(TIP|WARNING|CAUTION|NOTE|IMPORTANT)\]\s*/;

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

      // strip the leading "[!TYPE]" marker from the first non-empty text node
      var walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT, null);
      var node = walker.nextNode();
      while (node && node.nodeValue.trim() === "") node = walker.nextNode();
      if (node) node.nodeValue = node.nodeValue.replace(ALERT_RE, "");

      // prepend the label only after the marker is stripped from the content
      var label = document.createElement("span");
      label.className = "label";
      label.textContent = spec.label;
      box.insertBefore(label, box.firstChild);

      bq.parentNode.replaceChild(box, bq);
    }
  }

  // markdown text -> { id, title, bodyHTML } (first H1 becomes the panel title)
  function toTopic(fileName, mdText) {
    var tmp = document.createElement("div");
    tmp.innerHTML = window.marked.parse(mdText);
    var h1 = tmp.querySelector("h1");
    var title = h1 ? h1.textContent.trim() : fileName.replace(/\.md$/, "");
    if (h1) h1.parentNode.removeChild(h1);
    upgradeCallouts(tmp);
    return { id: slugify(title), title: title, bodyHTML: tmp.innerHTML };
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
    body.innerHTML = topic.bodyHTML;
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
      "<strong>Couldn’t load the notes</strong>" +
      "These notes load from separate files, so open the site with a local server " +
      "(not by double-clicking the file):<br><br>" +
      "<code>python3 -m http.server</code><br>then visit <code>http://localhost:8000</code>" +
      "</div>";
    if (window.console) console.error("[notes]", err);
  }

  function init() {
    var mount = document.getElementById("app");
    if (!mount) return;
    if (!window.marked) { showError(mount, new Error("marked failed to load")); return; }

    fetch(SUBJECT_DIR + "manifest.json")
      .then(function (r) { if (!r.ok) throw new Error("manifest.json " + r.status); return r.json(); })
      .then(function (files) {
        return Promise.all(files.map(function (name) {
          return fetch(SUBJECT_DIR + name)
            .then(function (r) { if (!r.ok) throw new Error(name + " " + r.status); return r.text(); })
            .then(function (text) { return toTopic(name, text); });
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
