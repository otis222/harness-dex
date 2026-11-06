// Harness 圖鑑：首頁依欄位篩選、程式碼區塊的複製按鈕。
// 沒有 JavaScript 時，頁面內容一樣完整可讀。
(function () {
  "use strict";

  var rows = document.querySelectorAll(".rows .row[data-slot]");
  var filters = document.querySelectorAll(".filter[data-slot]");
  var slots = document.querySelectorAll(".board .slot[data-slot]");
  var status = document.querySelector(".filter-status");
  var manifest = document.getElementById("manifest");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function slotName(id) {
    for (var i = 0; i < filters.length; i++) {
      if (filters[i].dataset.slot === id) return filters[i].dataset.name;
    }
    return id;
  }

  function apply(id, scroll) {
    var known = false;
    filters.forEach(function (f) { if (f.dataset.slot === id) known = true; });
    if (!known) id = "all";

    var shown = 0;
    rows.forEach(function (row) {
      var on = id === "all" || row.dataset.slot === id;
      row.hidden = !on;
      if (on) shown++;
    });
    filters.forEach(function (f) { f.setAttribute("aria-pressed", String(f.dataset.slot === id)); });
    slots.forEach(function (s) { s.classList.toggle("is-active", s.dataset.slot === id); });

    if (status) {
      status.textContent = id === "all"
        ? "共 " + shown + " 件"
        : "「" + slotName(id) + "」：" + shown + " 件。按「全部」看所有專案。";
    }
    if (scroll && manifest) {
      manifest.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    }
  }

  function fromHash() {
    var m = location.hash.match(/^#slot-([a-z-]+)$/);
    return m ? m[1] : "all";
  }

  if (rows.length) {
    filters.forEach(function (f) {
      f.addEventListener("click", function () {
        var id = f.dataset.slot;
        history.replaceState(null, "", id === "all" ? location.pathname : "#slot-" + id);
        apply(id, false);
      });
    });
    window.addEventListener("hashchange", function () {
      if (location.hash.indexOf("#slot-") === 0) apply(fromHash(), true);
    });
    apply(fromHash(), location.hash.indexOf("#slot-") === 0);
  }

  document.querySelectorAll("pre.code").forEach(function (pre) {
    var code = pre.querySelector("code");
    if (!code || !navigator.clipboard) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy";
    btn.textContent = "複製";
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        btn.textContent = "已複製";
      }, function () {
        btn.textContent = "請手動選取";
      });
      setTimeout(function () { btn.textContent = "複製"; }, 1800);
    });
    pre.appendChild(btn);
  });
})();
