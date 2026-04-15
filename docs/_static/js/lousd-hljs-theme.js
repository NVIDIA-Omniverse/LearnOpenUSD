/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 *
 * Toggle Highlight.js stylesheets to match Sphinx/Pygments light vs dark (data-theme).
 * Notebook outputs embed CDN Highlight.js links; this disables those and applies one
 * managed github / github-dark theme so colors stay consistent when the reader switches theme.
 */
(function () {
  'use strict';

  var HLJS_LIGHT =
    'https://unpkg.com/@highlightjs/cdn-assets@11.9.0/styles/github.min.css';
  var HLJS_DARK =
    'https://unpkg.com/@highlightjs/cdn-assets@11.9.0/styles/github-dark.min.css';
  var ID_LIGHT = 'lousd-hljs-github-light';
  var ID_DARK = 'lousd-hljs-github-dark';

  function isDarkTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  function ensureLink(id, href) {
    var el = document.getElementById(id);
    if (!el) {
      el = document.createElement('link');
      el.rel = 'stylesheet';
      el.href = href;
      el.id = id;
      document.head.appendChild(el);
    }
    return el;
  }

  function sync() {
    var dark = isDarkTheme();
    var lightLink = ensureLink(ID_LIGHT, HLJS_LIGHT);
    var darkLink = ensureLink(ID_DARK, HLJS_DARK);
    lightLink.disabled = dark;
    darkLink.disabled = !dark;

    document.querySelectorAll('link[href*="@highlightjs/cdn-assets"][rel="stylesheet"]').forEach(
      function (l) {
        if (l.id === ID_LIGHT || l.id === ID_DARK) {
          return;
        }
        l.disabled = true;
      }
    );
  }

  /* Body (notebook embeds) is not parsed yet when this script runs in <head>. */
  function syncWhenReady() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', sync);
    } else {
      sync();
    }
  }

  syncWhenReady();
  new MutationObserver(sync).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  });
})();
