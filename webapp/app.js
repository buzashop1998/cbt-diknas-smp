/* CBT KSM MTs - app.js (vanilla, file:// friendly) */
(function () {
  'use strict';

  var PKGS = (window.KSM_PACKAGES || {});
  var state = {
    pkg: null, questions: [], answers: {}, flags: {}, idx: 0,
    remain: 0, timerId: null, nama: '', kelas: ''
  };
  var YEAR_ORDER = [2023, 2022, 2021, 2020];

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function fmtTime(sec) {
    sec = Math.max(0, sec);
    var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    var p = function (n) { return (n < 10 ? '0' : '') + n; };
    return p(h) + ':' + p(m) + ':' + p(s);
  }

  /* ---------- HOME ---------- */
  var filterYear = 'all';
  function renderHome() {
    var keys = Object.keys(PKGS).filter(function (k) {
      return PKGS[k] && PKGS[k].questions && PKGS[k].questions.length > 0;
    });
    // filters
    var years = [];
    keys.forEach(function (k) {
      var y = PKGS[k].year;
      if (years.indexOf(y) < 0) years.push(y);
    });
    years.sort(function (a, b) { return b - a; });
    var fh = '<button class="chip' + (filterYear === 'all' ? ' active' : '') + '" data-y="all">Semua Tahun</button>';
    years.forEach(function (y) {
      fh += '<button class="chip' + (String(filterYear) === String(y) ? ' active' : '') + '" data-y="' + y + '">' + y + '</button>';
    });
    $('filters').innerHTML = fh;
    Array.prototype.forEach.call($('filters').children, function (btn) {
      btn.onclick = function () { filterYear = btn.getAttribute('data-y'); renderHome(); };
    });

    var html = '';
    years.forEach(function (y) {
      if (filterYear !== 'all' && String(filterYear) !== String(y)) return;
      keys.filter(function (k) { return PKGS[k].year === y; }).sort(function (a, b) {
        return (a + b).localeCompare ? (mapelOrder(PKGS[a]) - mapelOrder(PKGS[b]) || a.localeCompare(b)) : 0;
      }).forEach(function (k) {
        var p = PKGS[k];
        var pg = 0, isi = 0;
        p.questions.forEach(function (q) { if (q.type === 'isian') isi++; else pg++; });
        html += '<button class="pkg" data-k="' + esc(k) + '">' +
          '<span class="p-title">' + esc(p.title) + '</span>' +
          '<span class="p-sub">' + esc(p.tingkat) + ' &bull; Waktu ' + p.duration + ' menit</span>' +
          '<span class="p-badges">' +
          '<span class="badge b-count">' + p.questions.length + ' soal</span>' +
          (pg ? '<span class="badge b-type">' + pg + ' PG</span>' : '') +
          (isi ? '<span class="badge b-type">' + isi + ' Isian</span>' : '') +
          '<span class="badge b-time">&#9200; ' + p.duration + ' mnt</span>' +
          '</span></button>';
      });
    });
    if (!html) html = '<p class="hint">Paket tidak ditemukan.</p>';
    $('pkg-list').innerHTML = html;
    Array.prototype.forEach.call($('pkg-list').children, function (btn) {
      btn.onclick = function () { tryStart(btn.getAttribute('data-k')); };
    });
  }
  function mapelOrder(p) {
    var m = p.mapel || '';
    if (m.indexOf('Matematika') === 0) return 0;
    if (m.indexOf('IPA') === 0) return 1;
    return 2;
  }

  /* ---------- START ---------- */
  function tryStart(key) {
    var p = PKGS[key]; if (!p) return;
    var nama = $('inp-nama').value.trim();
    if (!nama) {
      $('ident-hint').textContent = 'Isi dulu nama peserta sebelum memulai ujian.';
      $('ident-hint').className = 'hint err';
      $('inp-nama').focus();
      return;
    }
    $('ident-hint').textContent = '';
    $('ident-hint').className = 'hint';
    state.nama = nama;
    state.kelas = $('inp-kelas').value.trim();
    beginExam(key, p);
  }

  function beginExam(key, p) {
    state.pkg = key;
    state.questions = p.questions.slice().sort(function (a, b) { return a.n - b.n; });
    state.answers = {}; state.flags = {}; state.idx = 0;
    state.remain = p.duration * 60;
    $('exam-name').textContent = state.nama + (state.kelas ? ' - ' + state.kelas : '');
    $('exam-pkg').textContent = p.title + ' | ' + state.questions.length + ' soal | ' + p.duration + ' menit';
    show('page-exam');
    renderQuestion();
    renderNav();
    clearInterval(state.timerId);
    updateTimer();
    state.timerId = setInterval(tick, 1000);
    window.scrollTo(0, 0);
  }

  function tick() {
    state.remain--;
    updateTimer();
    if (state.remain <= 0) {
      clearInterval(state.timerId);
      finalize(true);
    }
  }
  function updateTimer() {
    var t = $('timer');
    t.textContent = fmtTime(state.remain);
    t.className = 'timer' + (state.remain <= 300 ? ' warn' : '');
  }

  /* ---------- EXAM ---------- */
  function renderQuestion() {
    var q = state.questions[state.idx];
    $('q-num').textContent = 'Soal ' + (state.idx + 1) + ' / ' + state.questions.length;
    $('q-type').textContent = q.type === 'isian' ? 'Isian Singkat' : 'Pilihan Ganda';
    $('q-text').textContent = q.t;
    var imgs = '';
    (q.img || []).forEach(function (src) { imgs += '<img src="' + esc(src) + '" alt="gambar soal" loading="lazy">'; });
    $('q-imgs').innerHTML = imgs;

    var opts = '';
    if (q.type === 'pg') {
      ['A', 'B', 'C', 'D', 'E'].forEach(function (L) {
        if (!q.o || q.o[L] == null || String(q.o[L]).trim() === '') return;
        var sel = state.answers[q.n] === L ? ' sel' : '';
        opts += '<div class="opt' + sel + '" data-l="' + L + '"><span class="letter">' + L + '.</span><span>' + esc(q.o[L]) + '</span></div>';
      });
      opts += '<input type="text" style="display:none">';
      $('q-opts').innerHTML = opts;
      Array.prototype.forEach.call($('q-opts').querySelectorAll('.opt'), function (el) {
        el.onclick = function () {
          state.answers[q.n] = el.getAttribute('data-l');
          renderQuestion(); renderNav();
        };
      });
    } else {
      opts = '<div class="opt" style="cursor:default; border:none; padding:0"><input type="text" id="isian-input" placeholder="Ketik jawabanmu di sini" value="' + esc(state.answers[q.n] || '') + '"></div>';
      $('q-opts').innerHTML = opts;
      var inp = $('isian-input');
      inp.oninput = function () { state.answers[q.n] = inp.value; renderNavSoft(); };
      inp.onkeydown = function (e) { if (e.key === 'Enter') { e.preventDefault(); goNext(); } };
    }

    $('btn-flag').className = 'btn ghost' + (state.flags[q.n] ? ' flag-on' : '');
    $('btn-flag').textContent = state.flags[q.n] ? 'Hapus Tanda Ragu' : 'Tandai Ragu';
    $('btn-prev').disabled = state.idx === 0;
    $('btn-prev').style.opacity = state.idx === 0 ? .45 : 1;
    renderNav();
  }

  function renderNavSoft() {
    var q = state.questions[state.idx];
    var item = $('nav-' + q.n);
    if (item) {
      var answered = state.answers[q.n] != null && String(state.answers[q.n]).trim() !== '';
      item.className = 'nav-item' + (answered ? ' done' : '') + (state.flags[q.n] ? ' flag' : '') + (item === document.querySelector('.nav-item.cur') ? ' cur' : '');
    }
  }

  function renderNav() {
    var html = '';
    state.questions.forEach(function (q, i) {
      var answered = state.answers[q.n] != null && String(state.answers[q.n]).trim() !== '';
      var cls = 'nav-item' + (answered ? ' done' : '') + (state.flags[q.n] ? ' flag' : '') + (i === state.idx ? ' cur' : '');
      html += '<div class="' + cls + '" id="nav-' + q.n + '" data-i="' + i + '">' + q.n + '</div>';
    });
    $('nav-grid').innerHTML = html;
    Array.prototype.forEach.call($('nav-grid').children, function (el) {
      el.onclick = function () { state.idx = parseInt(el.getAttribute('data-i'), 10); renderQuestion(); window.scrollTo(0, 0); };
    });
  }

  function goNext() {
    if (state.idx < state.questions.length - 1) { state.idx++; renderQuestion(); window.scrollTo(0, 0); }
  }
  function goPrev() {
    if (state.idx > 0) { state.idx--; renderQuestion(); window.scrollTo(0, 0); }
  }

  /* ---------- FINISH & RESULT ---------- */
  function normalize(s) {
    return String(s == null ? '' : s).trim().toLowerCase()
      .replace(/,/g, '.').replace(/\s+/g, ' ')
      .replace(/^(rp|rp\.|rp )/g, '').trim();
  }
  function toNum(s) {
    var t = normalize(s).replace(/[^0-9.\-]/g, '');
    if (!t || t === '-' || t === '.') return null;
    var n = parseFloat(t);
    return isNaN(n) ? null : n;
  }
  function isCorrect(q, ans) {
    if (ans == null || String(ans).trim() === '') return false;
    if (q.type === 'pg') return normalize(ans) === normalize(q.a);
    var a1 = normalize(ans), a2 = normalize(q.a);
    if (a1 === a2) return true;
    var n1 = toNum(a1), n2 = toNum(a2);
    if (n1 !== null && n2 !== null) {
      if (n1 === n2) return true;
      var scale = Math.max(Math.abs(n2), 1);
      return Math.abs(n1 - n2) / scale < 0.005;
    }
    return false;
  }

  function finalize(auto) {
    clearInterval(state.timerId);
    var p = PKGS[state.pkg];
    var total = state.questions.length;
    var answered = 0, wrong = 0, correct = 0, isiCorrect = 0, isiTotal = 0;
    state.questions.forEach(function (q) {
      var ans = state.answers[q.n];
      var filled = ans != null && String(ans).trim() !== '';
      if (filled) answered++;
      if (q.type === 'isian') isiTotal++;
      if (isCorrect(q, ans)) { correct++; if (q.type === 'isian') isiCorrect++; }
      else if (filled) wrong++;
    });
    var empty = total - answered;
    var score = total ? Math.round(correct / total * 1000) / 10 : 0;

    $('res-meta').innerHTML = esc(state.nama) + (state.kelas ? ' &bull; ' + esc(state.kelas) : '') +
      '<br>' + esc(p.title) + (auto ? ' &bull; <b>waktu habis (dikumpulkan otomatis)</b>' : '');
    $('score-circle').style.setProperty('--pct', score);
    $('score-val').textContent = score;
    $('res-detail').innerHTML =
      '<div class="s-box s-ok"><small>Benar</small><b>' + correct + '</b></div>' +
      '<div class="s-box s-bad"><small>Salah</small><b>' + wrong + '</b></div>' +
      '<div class="s-box s-empty"><small>Kosong</small><b>' + empty + '</b></div>' +
      '<div class="s-box s-isi"><small>Isian Benar</small><b>' + isiCorrect + '/' + isiTotal + '</b></div>';

    var html = '';
    state.questions.forEach(function (q, i) {
      var ans = state.answers[q.n];
      var filled = ans != null && String(ans).trim() !== '';
      var ok = isCorrect(q, ans);
      var status = ok ? '<span class="c-status ok">Benar</span>'
        : (filled ? '<span class="c-status bad">Salah</span>' : '<span class="c-status empty">Kosong</span>');
      var jawabmu = q.type === 'pg'
        ? (filled ? esc(ans) + '. ' + esc((q.o && q.o[ans]) || '') : '<i>tidak dijawab</i>')
        : (filled ? esc(ans) : '<i>tidak dijawab</i>');
      var kunci = q.type === 'pg'
        ? esc(q.a) + '. ' + esc((q.o && q.o[q.a]) || '')
        : esc(q.a);
      var imgs = '';
      (q.img || []).forEach(function (src) { imgs += '<img src="' + esc(src) + '" alt="gambar" loading="lazy">'; });
      html += '<div class="c-item" data-i="' + i + '">' +
        '<div class="c-head"><span class="c-num">' + q.n + '.</span>' + status +
        '<span style="color:var(--muted); font-size:12px">' + (q.type === 'pg' ? 'Pilihan Ganda' : 'Isian') + '</span>' +
        '<span style="margin-left:auto; color:var(--muted)">&#9660;</span></div>' +
        '<div class="c-body">' +
        '<div class="c-ans" style="font-size:14px; white-space:pre-wrap">' + esc(q.t) + '</div>' +
        (imgs ? '<div class="c-imgs">' + imgs + '</div>' : '') +
        (q.type === 'pg' ? '<div class="c-ans"><b>Pilihan:</b><br>' +
          ['A', 'B', 'C', 'D', 'E'].filter(function (L) { return q.o && q.o[L]; }).map(function (L) {
            return L + '. ' + esc(q.o[L]);
          }).join('<br>') + '</div>' : '') +
        '<div class="c-ans"><b>Jawabanmu:</b> ' + jawabmu + '</div>' +
        '<div class="c-ans"><b>Kunci:</b> ' + kunci + '</div>' +
        (q.pemb ? '<div class="c-pemb"><b>Pembahasan:</b> ' + esc(q.pemb) + '</div>' : '') +
        '</div></div>';
    });
    $('correction-list').innerHTML = html;
    Array.prototype.forEach.call($('correction-list').children, function (item) {
      item.querySelector('.c-head').onclick = function () { item.classList.toggle('open'); };
    });
    // buka otomatis yang salah/kosong
    Array.prototype.forEach.call($('correction-list').children, function (item) {
      var q = state.questions[parseInt(item.getAttribute('data-i'), 10)];
      if (!isCorrect(q, state.answers[q.n])) item.classList.add('open');
    });
    show('page-result');
    window.scrollTo(0, 0);
  }

  /* ---------- NAV ---------- */
  function show(id) {
    ['page-home', 'page-exam', 'page-result'].forEach(function (p) {
      $(p).classList.toggle('hidden', p !== id);
    });
  }

  function confirmModal(title, msg, cb) {
    $('modal-title').textContent = title;
    $('modal-msg').textContent = msg;
    $('modal').classList.remove('hidden');
    $('modal-yes').onclick = function () { $('modal').classList.add('hidden'); cb(); };
    $('modal-no').onclick = function () { $('modal').classList.add('hidden'); };
  }

  /* ---------- EVENTS ---------- */
  $('btn-next').onclick = goNext;
  $('btn-prev').onclick = goPrev;
  $('btn-flag').onclick = function () {
    var q = state.questions[state.idx];
    state.flags[q.n] = !state.flags[q.n];
    renderQuestion();
  };
  $('btn-finish').onclick = function () {
    var total = state.questions.length, answered = 0;
    state.questions.forEach(function (q) {
      var a = state.answers[q.n];
      if (a != null && String(a).trim() !== '') answered++;
    });
    confirmModal('Kumpulkan Jawaban?',
      'Kamu sudah menjawab ' + answered + ' dari ' + total + ' soal. ' +
      (answered < total ? 'Soal yang belum dijawab akan dinilai SALAH. ' : '') +
      'Lanjutkan ke halaman koreksi?',
      function () { finalize(false); });
  };
  $('btn-home').onclick = function () { show('page-home'); renderHome(); window.scrollTo(0, 0); };
  $('btn-again').onclick = function () { beginExam(state.pkg, PKGS[state.pkg]); };
  document.addEventListener('keydown', function (e) {
    if (!$('page-exam').classList.contains('hidden') && e.target.tagName !== 'INPUT') {
      if (e.key === 'ArrowRight') goNext();
      if (e.key === 'ArrowLeft') goPrev();
    }
  });

  /* ---------- LIGHTBOX GAMBAR (klik untuk perbesar, zoom desktop+mobile) ---------- */
  var lb = { open: false, z: 1, baseW: 0, baseH: 0 };
  function lbEl(id) { return $(id); }
  function lbApply() {
    var img = lbEl('lb-img');
    if (lb.z <= 1) {
      img.classList.remove('zoomed');
      img.style.width = '';
      img.style.maxWidth = '98vw';
      img.style.maxHeight = 'calc(100vh - 60px)';
      lb.z = Math.max(lb.z, 1);
    } else {
      img.classList.add('zoomed');
      img.style.maxWidth = 'none';
      img.style.maxHeight = 'none';
      img.style.width = Math.round(lb.baseW * lb.z) + 'px';
    }
    img.style.setProperty('--lb-zoom', lb.z);
  }
  function lbMeasure() {
    var img = lbEl('lb-img'), stage = lbEl('lb-stage');
    if (!img.naturalWidth) return;
    var maxW = stage.clientWidth - 24, maxH = stage.clientHeight - 24;
    var r = Math.min(maxW / img.naturalWidth, maxH / img.naturalHeight, 1);
    lb.baseW = Math.round(img.naturalWidth * r);
    lb.baseH = Math.round(img.naturalHeight * r);
  }
  function lbOpen(src) {
    var img = lbEl('lb-img');
    img.src = src;
    lb.z = 1;
    lbApply();
    lbEl('lightbox').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    lb.open = true;
  }
  function lbClose() {
    lbEl('lightbox').classList.add('hidden');
    document.body.style.overflow = '';
    lb.open = false;
  }
  function lbZoomTo(z, keepScroll) {
    var stage = lbEl('lb-stage');
    var cx = keepScroll !== false ? (stage.scrollLeft + stage.clientWidth / 2) / Math.max(stage.scrollWidth, 1) : 0.5;
    var cy = keepScroll !== false ? (stage.scrollTop + stage.clientHeight / 2) / Math.max(stage.scrollHeight, 1) : 0.5;
    lb.z = Math.min(8, Math.max(1, z));
    lbApply();
    requestAnimationFrame(function () {
      stage.scrollLeft = cx * stage.scrollWidth - stage.clientWidth / 2;
      stage.scrollTop = cy * stage.scrollHeight - stage.clientHeight / 2;
    });
  }
  lbEl('lb-in').onclick = function () { lbZoomTo(lb.z * 1.4); };
  lbEl('lb-out').onclick = function () { lbZoomTo(lb.z / 1.4); };
  lbEl('lb-reset').onclick = function () { lb.z = 1; lbApply(); };
  lbEl('lb-close').onclick = lbClose;
  lbEl('lb-stage').addEventListener('click', function (e) {
    if (e.target === this) { lbClose(); return; }
    if (e.target.id === 'lb-img') { lb.z > 1 ? lbClose() : lbZoomTo(2.5); }
  });
  lbEl('lb-img').addEventListener('dblclick', function (e) {
    e.preventDefault();
    lb.z > 1 ? lbZoomTo(1) : lbZoomTo(3);
  });
  lbEl('lb-img').addEventListener('load', function () { lbMeasure(); });
  lbEl('lb-stage').addEventListener('wheel', function (e) {
    if (!lb.open) return;
    e.preventDefault();
    lbZoomTo(lb.z * (e.deltaY < 0 ? 1.15 : 1 / 1.15));
  }, { passive: false });
  document.addEventListener('keydown', function (e) {
    if (!lb.open) return;
    if (e.key === 'Escape') lbClose();
    if (e.key === '+' || e.key === '=') lbZoomTo(lb.z * 1.4);
    if (e.key === '-' || e.key === '_') lbZoomTo(lb.z / 1.4);
  });
  // klik gambar soal (halaman ujian & koreksi) membuka lightbox
  document.addEventListener('click', function (e) {
    var img = e.target.closest ? e.target.closest('.q-imgs img, .c-imgs img, .q-text img') : null;
    if (img && img.tagName === 'IMG') lbOpen(img.getAttribute('src'));
  });

  renderHome();
})();
