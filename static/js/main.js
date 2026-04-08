/**
 * Тема, AOS, тосты и confetti. Загружается с defer после aos.js.
 */
(function () {
  var root = document.documentElement;
  var storageKey = 'theme';

  function getTheme() {
    try {
      var saved = window.localStorage.getItem(storageKey);
      return saved === 'dark' ? 'dark' : 'light';
    } catch (e) {
      return 'light';
    }
  }

  function setTheme(nextTheme) {
    root.classList.toggle('dark', nextTheme === 'dark');
    try {
      window.localStorage.setItem(storageKey, nextTheme);
    } catch (e) {}
  }

  function toggleTheme() {
    var next = root.classList.contains('dark') ? 'light' : 'dark';
    setTheme(next);
    return next;
  }

  setTheme(getTheme());
  window.toggleTheme = toggleTheme;

  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    var sunIcon = toggle.querySelector('[data-theme-icon="sun"]');
    var moonIcon = toggle.querySelector('[data-theme-icon="moon"]');
    var sync = function () {
      var current = root.classList.contains('dark') ? 'dark' : 'light';
      toggle.setAttribute('aria-pressed', current === 'dark' ? 'true' : 'false');
      toggle.setAttribute(
        'aria-label',
        current === 'dark' ? 'Включить светлую тему' : 'Включить темную тему'
      );
      if (sunIcon && moonIcon) {
        sunIcon.classList.toggle('is-active', current === 'light');
        moonIcon.classList.toggle('is-active', current === 'dark');
      }
    };
    sync();

    toggle.addEventListener('click', function () {
      toggleTheme();
      sync();
    });
  }

  var mqNarrow = typeof window.matchMedia === 'function' ? window.matchMedia('(max-width: 1023px)') : null;
  var narrow = mqNarrow ? mqNarrow.matches : false;
  var reduceMotion =
    typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (typeof AOS !== 'undefined') {
    if (reduceMotion) {
      AOS.init({ disable: true });
    } else {
      AOS.init({
        duration: narrow ? 420 : 560,
        easing: 'ease-out-cubic',
        once: true,
        offset: narrow ? 12 : 28,
        anchorPlacement: 'top-bottom',
      });
    }
  }

  document.querySelectorAll('[data-dismiss-flash]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var toast = btn.closest('.flash-message');
      if (!toast) return;
      toast.remove();
      var stack = document.querySelector('[data-messages-stack]');
      if (stack && stack.childElementCount === 0) {
        stack.remove();
      }
    });
  });

  var flashOk = document.querySelector('.flash-success');
  if (flashOk && !reduceMotion) {
    var loadConfetti = function () {
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js';
      s.async = true;
      s.onload = function () {
        if (typeof confetti !== 'function') return;
        var colors = ['#1d7dfc', '#4b98ff', '#64adff', '#82beff', '#a5d0ff'];
        confetti({
          particleCount: 72,
          spread: 70,
          origin: { y: 0.14 },
          ticks: 160,
          gravity: 0.95,
          colors: colors,
        });
        setTimeout(function () {
          confetti({
            particleCount: 36,
            angle: 60,
            spread: 45,
            origin: { x: 0, y: 0.25 },
            colors: colors,
          });
          confetti({
            particleCount: 36,
            angle: 120,
            spread: 45,
            origin: { x: 1, y: 0.25 },
            colors: colors,
          });
        }, 200);
      };
      document.head.appendChild(s);
    };

    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadConfetti, { timeout: 2500 });
    } else {
      setTimeout(loadConfetti, 400);
    }
  }
})();
