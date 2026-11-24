/* Light / dark theme for every page.
   Loaded in each page's <head> (not deferred), so the theme is set on <html data-theme="…">
   before anything paints — no white flash in dark mode. The first visit follows the device
   setting; pressing 🌙 / ☀️ (added next to the page links) saves the choice in localStorage. */
(function () {
  "use strict";
  var KEY = "theme";
  var root = document.documentElement;

  function saved() {
    try {
      return window.localStorage.getItem(KEY) || window.localStorage.getItem("sa-theme");  // sa-theme: Say-along's old key
    } catch (e) { return null; }
  }
  function system() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  root.setAttribute("data-theme", saved() || system());

  function addToggle() {
    var nav = document.querySelector(".nav-toggle");
    if (!nav || document.querySelector(".theme-toggle")) return;
    var b = document.createElement("button");
    b.type = "button";
    b.className = "theme-toggle";
    function paint() {
      var dark = root.getAttribute("data-theme") === "dark";
      b.textContent = dark ? "☀️" : "🌙";
      b.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      b.title = b.getAttribute("aria-label");
    }
    b.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { window.localStorage.setItem(KEY, next); } catch (e) {}
      paint();
    });
    paint();
    nav.parentNode.insertBefore(b, nav.nextSibling);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", addToggle);
  else addToggle();
})();
