const API_BASE = "http://127.0.0.1:8888";
const ENDPOINTS = {
  login: "/auth/login",
  register: "/utenti",
  sale: "/sale",
  checkout: "/checkout",
  cancel: "/prenotazione/utente",
  prenota: "/prenotazione"
};
const BODY = document.body; /* Riferimento al body */

/* ───────────────────────── Sessione: 20 minuti ───────────────────────── */
const SESSION_KEY = "ps_session_expiry";
const SESSION_DURATION_MS = 20 * 60 * 1000; // 20 minuti
let sessionHeartbeat = null;

function setSession(email, token) {
  if (token) localStorage.setItem("ps_token", token);
  if (email) localStorage.setItem("ps_email", email);
  localStorage.setItem("ps_logged_in", "true"); // flag utile
  localStorage.setItem(SESSION_KEY, String(Date.now() + SESSION_DURATION_MS));
  startSessionHeartbeat();
}
function isSessionActive() {
  const exp = parseInt(localStorage.getItem(SESSION_KEY) || "0", 10);
  return Number.isFinite(exp) && Date.now() < exp;
}
function bumpSession() {
  if (!isSessionActive()) return;
  localStorage.setItem(SESSION_KEY, String(Date.now() + SESSION_DURATION_MS));
}
function initSessionIfAny() {
  // ✅ basta l'email per ripristinare una sessione al refresh
  const hasCreds = !!localStorage.getItem("ps_email");
  if (hasCreds && !localStorage.getItem(SESSION_KEY)) {
    localStorage.setItem(SESSION_KEY, String(Date.now() + SESSION_DURATION_MS));
  }
}
function clearSession() {
  localStorage.removeItem("ps_token");
  localStorage.removeItem("ps_email");
  localStorage.removeItem("ps_logged_in");
  localStorage.removeItem(SESSION_KEY);
  stopSessionHeartbeat();
}
function forceLogoutWithMessage(msg) {
  clearSession();
  pageTest.style.display = "none";
  viewAuth.style.display = "grid";
  BODY.classList.add("auth-active");
  switchTab("login");
  const alertLogin = $("#alert-login");
  setAlert(alertLogin, "info", msg || "Sessione terminata.");
}
function startSessionHeartbeat() {
  stopSessionHeartbeat();
  const bumpHandler = () => bumpSession();
  window.__ps_bumpHandler = bumpHandler;
  const bumpEvents = ["click", "keydown", "mousemove", "touchstart", "scroll"];
  bumpEvents.forEach((ev) => window.addEventListener(ev, bumpHandler, false));
  sessionHeartbeat = setInterval(() => {
    if (!isSessionActive()) forceLogoutWithMessage("Sessione scaduta dopo 20 minuti di inattività.");
  }, 15000);
}
function stopSessionHeartbeat() {
  if (sessionHeartbeat) {
    clearInterval(sessionHeartbeat);
    sessionHeartbeat = null;
  }
  const bumpHandler = window.__ps_bumpHandler;
  if (bumpHandler) {
    const bumpEvents = ["click", "keydown", "mousemove", "touchstart", "scroll"];
    bumpEvents.forEach((ev) => window.removeEventListener(ev, bumpHandler, false));
    delete window.__ps_bumpHandler;
  }
}

/* ───────────────────────── Helpers fetch ───────────────────────── */
async function apiPost(path, bodyObj, token) {
  const res = await fetch(API_BASE + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(bodyObj)
  });
  let data;
  try { data = await res.json(); } catch { data = { detail: "Risposta non JSON" }; }
  if (!res.ok) throw { status: res.status, data };
  return data;
}
async function apiGet(path, params = {}, token) {
  const url = new URL(API_BASE + path);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
  });
  const res = await fetch(url.toString(), {
    method: "GET",
    headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
  });
  let data;
  try { data = await res.json(); } catch { data = { detail: "Risposta non JSON" }; }
  if (!res.ok) throw { status: res.status, data };
  return data;
}
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
function setAlert(el, type, msg) {
  el.className = `alert ${type}`;
  el.textContent = msg;
  el.style.display = "block";
}
function clearAlert(el) {
  el.textContent = "";
  el.className = "alert";
  el.style.display = "none";
}
function setLoading(spinnerEl, isLoading) {
  spinnerEl.style.display = isLoading ? "inline-block" : "none";
}

/* ───────── Email helpers ───────── */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
function isValidEmail(s) { return EMAIL_RE.test(String(s || "").trim()); }
function attachEmailValidation(inputEl) {
  if (!inputEl) return;
  inputEl.setAttribute("inputmode", "email");
  inputEl.setAttribute("autocomplete", "email");
  inputEl.addEventListener("input", () => {
    if (!inputEl.value || isValidEmail(inputEl.value)) inputEl.setCustomValidity("");
  });
  inputEl.addEventListener("blur", () => {
    if (inputEl.value && !isValidEmail(inputEl.value)) inputEl.setCustomValidity("Formato email non valido (es. nome@azienda.it).");
    else inputEl.setCustomValidity("");
  });
}

/* ───────── Nome/Cognome helpers ───────── */
/* Solo lettere (anche accentate) e apostrofo */
const NAME_RE = /^[A-Za-zÀ-ÖØ-öø-ÿ'’\- ]+$/;
function attachNameValidation(inputEl, fieldName = "Campo") {
  if (!inputEl) return;
  inputEl.addEventListener("input", () => {
    const v = inputEl.value.trim();
    if (!v || NAME_RE.test(v)) inputEl.setCustomValidity("");
    else inputEl.setCustomValidity(fieldName + " può contenere solo lettere, apostrofi, spazi e trattini (senza numeri o altri simboli).");
  });
  inputEl.addEventListener("blur", () => {
    const v = inputEl.value.trim();
    if (v && !NAME_RE.test(v)) inputEl.setCustomValidity(fieldName + " può contenere solo lettere, apostrofi, spazi e trattini (senza numeri o altri simboli).");
    else inputEl.setCustomValidity("");
  });
}

/* ─────────────────────── Helpers prenotazione: “prossima ora” ─────────────────────── */
function getNextSlotDate() {
  const now = new Date();
  const d = new Date(now);
  d.setMinutes(0, 0, 0);
  d.setHours(now.getHours() + 1);
  return d;
}
function hhmm(d) { return `${String(d.getHours()).padStart(2, "0")}:00`; }
function isTodayDateStr(yyyy_mm_dd) {
  const [y, m, d] = (yyyy_mm_dd || "").split("-").map((x) => parseInt(x, 10));
  if (!y || !m || !d) return false;
  const now = new Date();
  return now.getFullYear() === y && now.getMonth() + 1 === m && now.getDate() === d;
}
function addHoursToHHMM(hhmmStr, hours = 1) {
  const [h, m] = (hhmmStr || "0:0").split(":").map((n) => parseInt(n, 10) || 0);
  const d = new Date();
  d.setHours(h, m, 0, 0);
  d.setHours(d.getHours() + hours);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}
function updateTimeMinConstraint(showInfo = false) {
  const dateStr = $("#rooms-data").value;
  const inizioEl = $("#rooms-inizio");
  const fineEl = $("#rooms-fine");
  const next = getNextSlotDate();
  const now = new Date();

  if (isTodayDateStr(dateStr)) {
    if (next.getDate() !== now.getDate()) {
      inizioEl.setAttribute("min", "23:59");
      fineEl.setAttribute("min", "23:59");
      if (showInfo) {
        const alertSale = $("#alert-sale");
        clearAlert(alertSale);
        setAlert(alertSale, "info", "Per oggi non è più possibile prenotare: seleziona una data successiva.");
      }
      return;
    }
    const minStr = hhmm(next);
    inizioEl.setAttribute("min", minStr);
    fineEl.setAttribute("min", minStr);

    if (inizioEl.value && inizioEl.value < minStr) inizioEl.value = minStr;
    if (!fineEl.value || fineEl.value <= inizioEl.value) fineEl.value = addHoursToHHMM(inizioEl.value || minStr, 1);
  } else {
    inizioEl.removeAttribute("min");
    fineEl.removeAttribute("min");
  }
}

/* ─────────────────────────── Tabs & UI ─────────────────────────── */
$$(".tab").forEach((tab) => {
  tab.addEventListener("click", () => switchTab(tab.dataset.tab));
  tab.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); switchTab(tab.dataset.tab); }
  });
});
function switchTab(name) {
  $$(".tab").forEach((t) => {
    t.classList.toggle("active", t.dataset.tab === name);
    t.setAttribute("aria-selected", String(t.dataset.tab === name));
  });
  $("#form-login").style.display = name === "login" ? "grid" : "none";
  $("#form-register").style.display = name === "register" ? "grid" : "none";
  (name === "login" ? $("#login-email") : $("#reg-nome"))?.focus();
}

/* Toggle password */
$$(".pwd-toggle").forEach((btn) => {
  btn.addEventListener("click", () => {
    const target = document.getElementById(btn.dataset.target);
    if (!target) return;
    const isPwd = target.type === "password";
    target.type = isPwd ? "text" : "password";
    btn.textContent = isPwd ? "Nascondi" : "Mostra";
  });
});

/* Footer year */
$("#year").textContent = new Date().getFullYear();

/* ───────────────────────────── Login ───────────────────────────── */
const formLogin = $("#form-login");
const alertLogin = $("#alert-login");
const spinnerLogin = $("#spinner-login");
const loginEmailInput = $("#login-email");
attachEmailValidation(loginEmailInput);

formLogin.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearAlert(alertLogin);
  const email = $("#login-email").value.trim();
  const password = $("#login-password").value;

  if (!email || !password) return setAlert(alertLogin, "error", "Inserisci email e password.");
  if (!isValidEmail(email)) return setAlert(alertLogin, "error", "Inserisci un’email valida (es. nome@azienda.it).");

  setLoading(spinnerLogin, true);
  try {
    const data = await apiGet(ENDPOINTS.login, { email, password });
    const token = data.access_token || data.token || data.jwt || null;
    setSession(email, token || undefined); // ✅ sessione 20 min
    setAlert(alertLogin, "success", "Accesso eseguito! Reindirizzo all'area di test…");
    setTimeout(() => showTestPage({ email }, token, data), 600);
  } catch (err) {
    setAlert(alertLogin, "error", err?.data?.detail || "Credenziali non valide o errore server.");
  } finally {
    setLoading(spinnerLogin, false);
  }
});

/* ─────────────────────────── Registrazione ─────────────────────────── */
const formRegister = $("#form-register");
const alertRegister = $("#alert-register");
const spinnerRegister = $("#spinner-register");
const regEmailInput = $("#reg-email");
attachEmailValidation(regEmailInput);

/* CF: maiuscolo, alfanumerico, 16 chars, senza spazi */
const cfInput = $("#reg-cf");
if (cfInput) {
  cfInput.setAttribute("maxlength", "16");
  cfInput.setAttribute("minlength", "16");
  cfInput.setAttribute("pattern", "[A-Za-z0-9]{16}");
  cfInput.setAttribute("inputmode", "latin");
  cfInput.addEventListener("input", () => {
    const sanitized = cfInput.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
    cfInput.value = sanitized.slice(0, 16);
    if (/^[A-Z0-9]{0,16}$/.test(cfInput.value)) cfInput.setCustomValidity("");
  });
  cfInput.addEventListener("blur", () => {
    const v = cfInput.value.toUpperCase();
    cfInput.value = v;
    if (!/^[A-Z0-9]{16}$/.test(v)) cfInput.setCustomValidity("Il Codice Fiscale deve essere di 16 caratteri, solo lettere e numeri, senza spazi.");
    else cfInput.setCustomValidity("");
  });
}

/* Telefono: 10–15 totali, cifre; “+” opzionale SOLO in prima posizione */
const telInput = $("#reg-telefono");
if (telInput) {
  telInput.setAttribute("inputmode", "tel");
  telInput.setAttribute("minlength", "10");
  telInput.setAttribute("maxlength", "15"); // incluso '+'
  telInput.setAttribute("pattern", "^(?:\\+\\d{9,14}|\\d{10,15})$");
  telInput.addEventListener("input", () => {
    let v = telInput.value.replace(/[^\d+]/g, "");
    const plusCount = (v.match(/\+/g) || []).length;
    if (plusCount > 1) {
      const startsWithPlus = v[0] === "+";
      v = v.replace(/\+/g, "");
      v = (startsWithPlus ? "+" : "") + v;
    }
    if (v.includes("+") && v[0] !== "+") v = v.replace(/\+/g, "");
    if (v.length > 15) v = v.slice(0, 15);
    telInput.value = v;
    if (/^\+?\d{0,15}$/.test(v)) telInput.setCustomValidity("");
  });
  telInput.addEventListener("blur", () => {
    const v = telInput.value;
    const fullOk = /^(?:\+\d{9,14}|\d{10,15})$/.test(v);
    if (!fullOk) telInput.setCustomValidity("Numero non valido: 10–15 caratteri totali, solo cifre; “+” facoltativo solo all’inizio.");
    else telInput.setCustomValidity("");
  });
}

/* Nome e Cognome: solo lettere e apostrofi */
attachNameValidation($("#reg-nome"), "Nome");
attachNameValidation($("#reg-cognome"), "Cognome");

formRegister.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearAlert(alertRegister);

  const nome = $("#reg-nome").value.trim();
  const cognome = $("#reg-cognome").value.trim();
  const cf = $("#reg-cf").value.trim().toUpperCase();
  const email = $("#reg-email").value.trim();
  const numero_tel = $("#reg-telefono").value.trim();
  const password = $("#reg-password").value;
  const password2 = $("#reg-password2").value;

  if (!nome || !cognome || !cf || !email || !numero_tel || !password) {
    return setAlert(alertRegister, "error", "Compila tutti i campi obbligatori.");
  }
  if (!NAME_RE.test(nome)) {
    return setAlert(alertRegister, "error", "Il nome può contenere solo lettere, apostrofi, spazi e trattini (senza numeri o altri simboli).");
  }
  if (!NAME_RE.test(cognome)) {
    return setAlert(alertRegister, "error", "Il cognome può contenere solo lettere, apostrofi, spazi e trattini (senza numeri o altri simboli).");
  }
  if (!isValidEmail(email)) return setAlert(alertRegister, "error", "Email non valida (es. nome@azienda.it).");
  if (!/^[A-Z0-9]{16}$/.test(cf)) {
    return setAlert(alertRegister, "error", "Codice Fiscale non valido: 16 caratteri, solo lettere e numeri (maiuscolo), senza spazi.");
  }
  if (!/^(?:\+\d{9,14}|\d{10,15})$/.test(numero_tel)) {
    return setAlert(alertRegister, "error", "Numero non valido: 10–15 caratteri totali, solo cifre; “+” facoltativo solo all’inizio.");
  }
  if (password.length < 6) return setAlert(alertRegister, "error", "La password deve avere almeno 6 caratteri.");
  if (password !== password2) return setAlert(alertRegister, "error", "Le password non coincidono.");

  const attivo = true;
  setLoading(spinnerRegister, true);
  try {
    const bodyData = { nome, cognome, cf, email, attivo, password, numero_tel };
    await apiPost(ENDPOINTS.register, bodyData);
    try { localStorage.setItem("ps_cf", cf); } catch {}
    setAlert(alertRegister, "success", "Registrazione effettuata con successo! Ti reindirizzo al login…");
    setTimeout(() => {
      switchTab("login");
      $("#login-email").value = email;
      const aLogin = $("#alert-login");
      setAlert(aLogin, "success", "Registrazione effettuata con successo. Inserisci la password per accedere.");
      $("#login-password").focus();
    }, 900);
  } catch (err) {
    setAlert(alertRegister, "error", err?.data?.detail || "Registrazione non riuscita.");
  } finally {
    setLoading(spinnerRegister, false);
  }
});

/* ─────────────────────────── Post-login view ─────────────────────────── */
const viewAuth = $("#view-auth");
const pageTest = $("#page-test");
const testUser = $("#test-user");

function showTestPage(user, token, raw) {
  viewAuth.style.display = "none";
  pageTest.style.display = "block";
  BODY.classList.remove("auth-active");

  if (!isSessionActive()) { forceLogoutWithMessage("Sessione non valida o scaduta. Effettua nuovamente l'accesso."); return; }
  bumpSession();

  const email = user?.email || localStorage.getItem("ps_email") || "—";
  const userName = email.split("@")[0];
  testUser.textContent = userName.charAt(0).toUpperCase() + userName.slice(1);

  setDefaultAvailabilityInputs();
  updateTimeMinConstraint();
  const savedCf = localStorage.getItem("ps_cf");
  if (savedCf) { const cfEl = document.querySelector("#cf-utente"); if (cfEl) cfEl.value = savedCf; }
}

/* ─────────────────────────── Ricerca sale ─────────────────────────── */
const btnCercaSale = $("#btn-cerca-sale");
const spinnerSale = $("#spinner-sale");
const alertSale = $("#alert-sale");
const resultsSale = $("#rooms-results");
const inputPartecipanti = $("#rooms-partecipanti");

let currentInizio = "";
let currentFine = "";

btnCercaSale.addEventListener("click", async () => {
  if (!isSessionActive()) return forceLogoutWithMessage("Sessione scaduta. Effettua di nuovo l'accesso.");
  bumpSession();

  clearAlert(alertSale);
  updateTimeMinConstraint();
  const dateStr = $("#rooms-data").value;
  const next = getNextSlotDate();
  const now = new Date();
  if (isTodayDateStr(dateStr) && next.getDate() !== now.getDate()) {
    return setAlert(alertSale, "error", "Per oggi non è più possibile prenotare: seleziona una data successiva.");
  }

  const capRaw = $("#rooms-capienza").value;
  const needed = parseInt(inputPartecipanti?.value || "") || 0;
  const capParsed = parseInt(capRaw || "") || 0;
  const capienza = String(Math.max(capParsed, needed));
  const data = $("#rooms-data").value;
  let inizio = $("#rooms-inizio").value;
  let fine = $("#rooms-fine").value;
  if (!data || !inizio || !fine) return setAlert(alertSale, "error", "Inserisci data, orario di inizio e fine.");

  currentInizio = toWholeHour(inizio);
  $("#rooms-inizio").value = currentInizio;
  currentFine = toWholeHour(fine);
  $("#rooms-fine").value = currentFine;

  setLoading(spinnerSale, true);
  try {
    const token = localStorage.getItem("ps_token") || undefined;
    const resp = await apiGet(ENDPOINTS.sale, { capienza, data, inizio: currentInizio, fine: currentFine }, token);
    renderRoomsResults(resp);
    setAlert(alertSale, "success", "Ricerca completata. Di seguito le sale disponibili.");
  } catch (err) {
    resultsSale.innerHTML = "";
    setAlert(alertSale, "error", err?.data?.detail || "Errore durante la ricerca sale.");
  } finally {
    setLoading(spinnerSale, false);
  }
});

/* ─────────────────────────── Render tabelle ─────────────────────────── */
function renderRoomsResults(data) {
  const needed = parseInt(inputPartecipanti?.value || "") || 0;
  const filterByParticipants = (arr) => (needed > 0 ? arr.filter((r) => (parseInt(r?.capienza) || 0) >= needed) : arr);

  let arr = null;
  if (Array.isArray(data)) arr = data;
  else if (data && Array.isArray(data.sale)) arr = data.sale;

  if (arr) {
    const isRooms = arr.length > 0 &&
      ["nome", "capienza", "disponibilita_ore", "disponibilita_giorni"].every((k) => k in arr[0]);
    if (isRooms) {
      const a = filterByParticipants(arr);
      if (a.length === 0) {
        resultsSale.innerHTML = '<div class="help">Nessuna sala disponibile per i criteri selezionati (capienza e/o orario).</div>';
        return;
      }
      resultsSale.innerHTML = buildRoomsTable(a);
      return;
    }
    if (arr.length === 0) {
      resultsSale.innerHTML = '<div class="help">Nessuna sala disponibile per i criteri selezionati.</div>';
      return;
    }
    resultsSale.innerHTML = buildTableFromArray(arr);
    return;
  }
  resultsSale.innerHTML = `<div class="help">Formato dati non previsto. Contatta il supporto.</div>`;
}
function buildTableFromArray(arr) {
  const keys = Array.from(new Set(arr.flatMap((o) => Object.keys(o || {}))));
  const thead = `<thead><tr>${keys.map((k) => `<th>${escapeHtml(k)}</th>`).join("")}</tr></thead>`;
  const rows = arr.map((o) => `<tr>${keys.map((k) => `<td>${escapeHtml(formatCell(o?.[k]))}</td>`).join("")}</tr>`).join("");
  return `<div style="overflow:auto"><table>${thead}<tbody>${rows}</tbody></table></div>`;
}
function buildRoomsTable(arr) {
  const header = "<thead><tr><th>Nome Sala</th><th>Capienza Max</th><th>Orario Disponibile</th><th>Giorni Operativi</th><th></th></tr></thead>";
  const body = arr.map((r) => {
    const nome = escapeHtml(r.nome ?? "—");
    const cap = r.capienza != null ? Number(r.capienza).toLocaleString("it-IT") : "—";
    const ore = escapeHtml(r.disponibilita_ore ?? "—");
    const giorni = escapeHtml(r.disponibilita_giorni ?? "—");
    return `<tr><td>${nome}</td><td>${cap}</td><td>${ore}</td><td>${giorni}</td><td style="text-align:right"><button class="btn primary btn-prenota" data-room="${escapeHtml(r.nome)}">Prenota Ora</button></td></tr>`;
  }).join("");
  return `<div style="overflow:auto"><table>${header}<tbody>${body}</tbody></table></div>`;
}
function formatCell(v) { if (v === null || v === undefined) return ""; if (typeof v === "object") return JSON.stringify(v); return String(v); }
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

/* ─────────────────────────── Default & normalizzazioni ─────────────────────────── */
function setDefaultAvailabilityInputs() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  $("#rooms-data").value = `${yyyy}-${mm}-${dd}`;
  $("#rooms-inizio").value = "09:00";
  $("#rooms-fine").value = "11:00";
  $("#rooms-capienza").value = 30;
}
function toWholeHour(v) {
  if (!v) return v;
  const h = String(v).split(":")[0];
  const hh = String(h).padStart(2, "0");
  return `${hh}:00`;
}
["#rooms-inizio", "#rooms-fine"].forEach((sel) => {
  const el = document.querySelector(sel);
  if (!el) return;
  el.addEventListener("change", () => { el.value = toWholeHour(el.value); updateTimeMinConstraint(); });
  el.addEventListener("blur", () => { el.value = toWholeHour(el.value); updateTimeMinConstraint(); });
});
$("#rooms-data")?.addEventListener("change", () => updateTimeMinConstraint(true));

/* ─────────────────────────── Checkout ─────────────────────────── */
const chkCode = $("#chk-code");
const btnCheckout = $("#btn-checkout");
const spinnerChk = $("#spinner-chk");
const alertChk = $("#alert-chk");
btnCheckout?.addEventListener("click", async () => {
  if (!isSessionActive()) return forceLogoutWithMessage("Sessione scaduta. Effettua di nuovo l'accesso.");
  bumpSession();

  clearAlert(alertChk);
  const code = (chkCode?.value || "").trim();
  if (!code) return setAlert(alertChk, "error", "Inserisci il codice prenotazione.");
  setLoading(spinnerChk, true);
  const token = localStorage.getItem("ps_token") || undefined;
  const path = ENDPOINTS.checkout + "/" + encodeURIComponent(code);
  let status = null, data = null, done = false;
  for (const m of ["PUT", "POST", "GET"]) {
    try {
      const res = await fetch(API_BASE + path, { method: m, headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) } });
      status = res.status; try { data = await res.json(); } catch { data = {}; }
      if (status === 405) continue; done = true; break;
    } catch {}
  }
  setLoading(spinnerChk, false);
  if (!done) return setAlert(alertChk, "error", "Il server non è raggiungibile.");
  const msg = (data && (data.message || data.detail || data.error)) || "Operazione completata.";
  if (status === 200) setAlert(alertChk, "success", msg);
  else if (status === 208) setAlert(alertChk, "info", msg);
  else if (status === 404) setAlert(alertChk, "error", msg);
  else if (status >= 500) setAlert(alertChk, "error", msg);
  else setAlert(alertChk, "info", msg);
});
chkCode?.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); btnCheckout?.click(); } });

/* ─────────────────────────── Delete prenotazione ─────────────────────────── */
const delCode = $("#del-code");
const btnDelete = $("#btn-delete");
const spinnerDel = $("#spinner-del");
const alertDel = $("#alert-del");
btnDelete?.addEventListener("click", async () => {
  if (!isSessionActive()) return forceLogoutWithMessage("Sessione scaduta. Effettua di nuovo l'accesso.");
  bumpSession();

  clearAlert(alertDel);
  const code = (delCode?.value || "").trim();
  if (!code) return setAlert(alertDel, "error", "Inserisci il codice prenotazione.");
  setLoading(spinnerDel, true);
  const token = localStorage.getItem("ps_token") || undefined;
  const path = ENDPOINTS.cancel + "/" + encodeURIComponent(code);
  try {
    const res = await fetch(API_BASE + path, { method: "DELETE", headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) } });
    let data; try { data = await res.json(); } catch { data = {}; }
    const status = res.status;
    const msg = (data && (data.message || data.detail || data.error)) || "Operazione completata.";
    if (status === 200) setAlert(alertDel, "success", msg);
    else if (status === 208) setAlert(alertDel, "info", msg);
    else if (status === 404) setAlert(alertDel, "error", msg);
    else if (status >= 500) setAlert(alertDel, "error", msg);
    else setAlert(alertDel, "info", msg);
  } catch {
    setAlert(alertDel, "error", "Il server non è raggiungibile.");
  } finally {
    setLoading(spinnerDel, false);
  }
});
delCode?.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); btnDelete?.click(); } });

/* ─────────────────────────── Prenota dal risultato ─────────────────────────── */
resultsSale.addEventListener("click", async (e) => {
  if (!isSessionActive()) return forceLogoutWithMessage("Sessione scaduta. Effettua di nuovo l'accesso.");
  bumpSession();

  const btn = e.target.closest(".btn-prenota");
  if (!btn) return;
  clearAlert(alertSale);

  updateTimeMinConstraint();
  const dateStr = $("#rooms-data").value;
  const next = getNextSlotDate();
  const now = new Date();
  if (isTodayDateStr(dateStr) && next.getDate() !== now.getDate()) {
    return setAlert(alertSale, "error", "Per oggi non è più possibile prenotare: seleziona una data successiva.");
  }

  const nom_sala = btn.dataset.room;
  const giorno = $("#rooms-data").value;
  const inizio = $("#rooms-inizio").value;
  const fine = $("#rooms-fine").value;
  const fascia_oraria = `${toWholeHour(inizio)} - ${toWholeHour(fine)}`;
  const partecipanti_previsti = parseInt($("#rooms-partecipanti")?.value || "");
  const cf_utente = ($("#cf-utente")?.value || localStorage.getItem("ps_cf") || "").trim();
  if (!cf_utente) return setAlert(alertSale, "error", "Inserisci il CF utente per procedere con la prenotazione.");
  if (!partecipanti_previsti || partecipanti_previsti < 1) return setAlert(alertSale, "error", "Inserisci il numero di partecipanti.");

  setLoading(spinnerSale, true);
  try {
    const token = localStorage.getItem("ps_token") || undefined;
    const body = { cf_utente, nom_sala, giorno, fascia_oraria, partecipanti_previsti };
    const res = await apiPost(ENDPOINTS.prenota, body, token);
    setAlert(alertSale, "success", res?.message || `Sala ${nom_sala} prenotata con successo!`);
  } catch (err) {
    setAlert(alertSale, "error", err?.data?.detail || err?.data?.message || "Errore durante la prenotazione.");
  } finally {
    setLoading(spinnerSale, false);
  }
});

/* ─────────────────────────── Logout & auto-login ─────────────────────────── */
$("#btn-logout").addEventListener("click", () => {
  clearSession();
  pageTest.style.display = "none";
  viewAuth.style.display = "grid";
  BODY.classList.add("auth-active");
  switchTab("login");
  const aLogin = $("#alert-login");
  setAlert(aLogin, "info", "Sei uscito.");
});

document.addEventListener("DOMContentLoaded", () => {
  // ✅ Se ricarichi, resta dentro se la sessione è valida (email presente + expiry non scaduto)
  initSessionIfAny();
  const email = localStorage.getItem("ps_email");
  if (email && isSessionActive()) {
    startSessionHeartbeat();
    const token = localStorage.getItem("ps_token") || undefined;
    showTestPage({ email }, token);
  } else {
    if (!isSessionActive()) localStorage.removeItem(SESSION_KEY);
  }
});
