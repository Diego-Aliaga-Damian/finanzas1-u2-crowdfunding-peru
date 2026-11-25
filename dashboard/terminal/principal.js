// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Fecha: 2026-11-24
// Arranque de la terminal: recibe los datos de Streamlit, coordina el replay, las superficies y el relato guiado.
(function () {
  "use strict";
  const FC = window.FC, $ = (x) => document.getElementById(x);
  let d = null, sup, replay, flujo, consola, pos = 0, corre = !FC.quieto, vel = 2.6, mesVisto = -1, supId = null, relato = null, ultimo = 0, visible = true, finDe = 0;
  const avisados = new Set();

  // ---- protocolo de componentes de Streamlit
  const enviar = (type, datos) => window.parent.postMessage(Object.assign({ isStreamlitMessage: true, type }, datos), "*");
  const medir = () => { if (!document.fullscreenElement) enviar("streamlit:setFrameHeight", { height: Math.ceil($("t").getBoundingClientRect().height) + 2 }); };
  window.addEventListener("message", (e) => { if (e.data && e.data.type === "streamlit:render" && !d) iniciar(e.data.args.datos); });

  function iniciar(datos) {
    d = datos; $("espera").remove(); $("t").hidden = false;
    $("rango").textContent = d.etiquetas[0] + " → " + d.etiquetas[d.etiquetas.length - 1]; $("sha").textContent = "SHA-256 " + d.sha.slice(0, 10) + "…"; $("sha").title = "Huella de la base procesada: " + d.sha;
    const leyenda = $("leyenda"); d.plataformas.forEach((p) => { const s = document.createElement("span"), i = document.createElement("i"); i.style.background = p.color; s.append(i, p.nombre); leyenda.append(s); });
    const cinta = $("cinta"); for (let k = 0; k < 2; k++) d.cinta.forEach((c) => { const s = document.createElement("span"), b = document.createElement("b"), e = document.createElement("em"); b.textContent = c.v; e.textContent = c.d === null ? "" : (c.d > 0 ? "▲ " : c.d < 0 ? "▼ " : "= ") + FC.num(Math.abs(c.d), Math.abs(c.d) < 1 ? 2 : 1) + " " + c.u; s.append(c.t, b, e); cinta.append(s); });
    sup = new FC.Superficie($("gl"), $("capa")); sup.mesTexto = (p) => { const M = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]; return M[+p.slice(5) - 1] + " " + p.slice(0, 4); };
    replay = new FC.Replay($("c-replay"), d, (i) => { pausar(); ir(i); }); flujo = new FC.Flujo($("c-flujo"), d); consola = new FC.Consola($("consola"), d.log);
    d.superficies.forEach((s) => { const b = document.createElement("button"); b.textContent = s.boton; b.dataset.s = s.id; b.onclick = () => elegir(s.id); $("tabs").append(b); });
    $("linea").max = d.meses.length - 1; elegir("costo"); ir(FC.quieto ? d.meses.length - 1 : d.meses.indexOf("2024-01")); for (let k = 0; k < 16; k++) consola.paso(99);
    $("play").onclick = () => (corre ? pausar() : seguir()); $("atras").onclick = () => { pausar(); ir(Math.floor(pos) - 1); }; $("adelante").onclick = () => { pausar(); ir(Math.floor(pos) + 1); };
    $("linea").oninput = (e) => { pausar(); ir(+e.target.value); };
    $("vel").onclick = (e) => { if (!e.target.dataset.v) return; vel = +e.target.dataset.v; [...$("vel").children].forEach((b) => b.classList.toggle("on", b === e.target)); };
    $("zmas").onclick = () => sup.acercar(1.12); $("zmen").onclick = () => sup.acercar(1 / 1.12); $("relato").onclick = () => (relato ? cerrarRelato() : contar());
    $("pantalla").onclick = pantalla;
    document.addEventListener("fullscreenchange", () => { const f = !!document.fullscreenElement; document.body.classList.toggle("lleno", f); $("pantalla").textContent = f ? "✕ Salir" : "⛶ Pantalla completa"; setTimeout(medir, 80); });
    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" && e.key.startsWith("Arrow")) return;
      const k = { " ": () => (corre ? pausar() : seguir()), ArrowLeft: () => { pausar(); ir(Math.floor(pos) - 1); }, ArrowRight: () => { pausar(); ir(Math.floor(pos) + 1); }, f: pantalla, r: () => (relato ? cerrarRelato() : contar()), 1: () => elegir(d.superficies[0].id), 2: () => elegir(d.superficies[1].id), 3: () => elegir(d.superficies[2].id) }[e.key.length === 1 ? e.key.toLowerCase() : e.key];
      if (k && !(e.key === " " && e.target.tagName === "BUTTON")) { e.preventDefault(); k(); }
    });
    if (!corre) $("play").textContent = "▶";
    new ResizeObserver(medir).observe($("t"));
    new IntersectionObserver((v) => { visible = v[0].isIntersecting; }).observe($("t"));
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(medir);
    medir(); requestAnimationFrame(cuadro);
  }

  function pantalla() { if (document.fullscreenElement) document.exitFullscreen(); else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(() => avisar("Pantalla completa", "Tu navegador no la permite aquí.", 4)); }
  function pausar() { corre = false; $("play").textContent = "▶"; if (relato) cerrarRelato(); }
  function seguir() { if (pos >= d.meses.length - 1.01) { pos = 0; avisados.clear(); } corre = true; $("play").textContent = "❚❚"; }
  function ir(i) { pos = Math.max(0, Math.min(d.meses.length - 1, i)); }
  function elegir(id) {
    supId = id; const s = d.superficies.find((x) => x.id === id); sup.fijar(s);
    $("s-tit").textContent = s.titulo; $("s-ins").textContent = s.insignia; $("s-ins").className = "ins" + (s.insignia.startsWith("Observado") ? " obs" : ""); $("s-for").textContent = s.formula; $("s-ex").textContent = s.explica;
    [...$("tabs").children].forEach((b) => b.classList.toggle("on", b.dataset.s === id)); mesVisto = -1; medir();
  }

  // ---- avisos y relato guiado
  let temporizador = null;
  function avisar(titulo, texto, seg) {
    const a = $("aviso"); a.children[0].textContent = titulo; a.children[1].textContent = texto; a.classList.add("on"); clearTimeout(temporizador);
    const b = a.children[2]; b.style.transition = "none"; b.style.transform = "scaleX(1)"; void b.offsetWidth; b.style.transition = "transform " + seg + "s linear"; b.style.transform = "scaleX(0)";
    temporizador = setTimeout(() => a.classList.remove("on"), seg * 1000);
  }
  function contar() { corre = true; relato = { k: 0, fase: "viaja", reloj: 0 }; pos = 0; avisados.clear(); $("play").textContent = "❚❚"; $("relato").textContent = "■ Detener la historia"; elegir(d.hitos[0].sup); }
  function cerrarRelato() { relato = null; $("relato").textContent = "▶ Contar la historia"; $("aviso").classList.remove("on"); }
  function avanzar(dt) {
    const fin = d.meses.length - 1;
    if (relato) {
      const h = d.hitos[relato.k], meta = d.meses.indexOf(h.mes);
      if (relato.fase === "viaja") {
        pos = Math.min(meta, pos + dt * Math.max(3, (meta - pos) * 1.1 + 2));
        if (pos >= meta) { relato.fase = "cuenta"; relato.reloj = 7.5; if (supId !== h.sup) elegir(h.sup); avisar(relato.k + 1 + "/" + d.hitos.length + " · " + h.titulo, d.etiquetas[meta] + ": " + h.texto, 7.5); }
      } else if ((relato.reloj -= dt) <= 0) { if (++relato.k >= d.hitos.length) { cerrarRelato(); pausar(); } else relato.fase = "viaja"; }
      return;
    }
    if (!corre) return;
    if (pos >= fin) { if ((finDe += dt) > 6) { finDe = 0; pos = 0; avisados.clear(); } return; }
    pos = Math.min(fin, pos + dt * vel);
    const i = Math.floor(pos); d.hitos.forEach((h) => { if (d.meses.indexOf(h.mes) === i && !avisados.has(h.mes)) { avisados.add(h.mes); avisar(h.titulo, d.etiquetas[i] + ": " + h.texto, 5.5); } });
  }

  function alCambiarMes(i) {
    FC.tablero(d, i); $("reloj").textContent = d.etiquetas[i]; $("linea").value = i; $("linea").setAttribute("aria-valuetext", d.etiquetas[i]); sup.etiqueta = d.etiquetas[i];
    sup.lineas = d.tasas.map((t) => ({ color: t.color, tramo: t.tramo, tea: t.v[i], nombre: t.nombre }));
    const c = $("s-series"); c.replaceChildren();
    if (supId === "costo") sup.lineas.filter((l) => l.tramo).forEach((l) => { const e = document.createElement("div"), k = document.createElement("i"), b = document.createElement("b"); k.style.background = l.color; b.textContent = FC.num(l.tea, 2) + " %"; e.append(k, l.nombre + " ", b); c.append(e); });
  }

  function cuadro(ms) {
    requestAnimationFrame(cuadro);
    const real = (ms - ultimo) / 1000 || 0, dt = Math.min(0.1, real); ultimo = ms;
    if (!visible || document.hidden) return;
    const t0 = performance.now();
    avanzar(Math.min(0.5, real)); const i = Math.floor(pos); if (i !== mesVisto) { mesVisto = i; alCambiarMes(i); }
    sup.corte = supId === "tasas" ? pos + d.desfase_tasas : pos;
    consola.paso(dt); replay.dibujar(pos); flujo.dibujar(i, dt); sup.dibujar(ms / 1000, dt);
    FC.ms = (FC.ms || 8) * 0.95 + (performance.now() - t0) * 0.05;      // costo medio por cuadro
    if (FC.ms > 24 && FC.calidad > 0.6) { FC.calidad -= 0.2; FC.ms = 12; }
  }

  enviar("streamlit:componentReady", { apiVersion: 1 });
})();
