// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Fecha: 2026-11-24
// Paneles 2D de la terminal: replay mensual, flujo del dinero, tablero del mes y consola con el registro real.
(function () {
  "use strict";
  const FC = window.FC, C = FC.C;

  // ---------------------------------------------------------------- replay mensual
  class Replay {
    constructor(cv, d, alElegir) {
      this.cv = cv; this.d = d; this.g = cv.getContext("2d"); this.cursor = null;
      this.tope = Math.ceil(Math.max(...d.mensual.monto.map((x) => x || 0), ...d.mensual.media_previa.map((m, i) => (m || 0) + (d.mensual.desv_previa[i] || 0))) / 2e6) * 2e6;
      const mes = (e) => { const b = cv.getBoundingClientRect(); return Math.max(0, Math.min(d.meses.length - 1, Math.floor((e.clientX - b.left - this.x0) / this.paso))); };
      cv.addEventListener("pointermove", (e) => { const b = cv.getBoundingClientRect(); this.cursor = { m: mes(e), y: e.clientY - b.top }; });
      cv.addEventListener("pointerleave", () => { this.cursor = null; });
      cv.addEventListener("click", (e) => alElegir(mes(e)));
    }
    dibujar(pos) {
      const g = this.g, d = this.d, { w, h, r } = FC.medir(this.cv); if (w < 40) return;
      g.setTransform(r, 0, 0, r, 0, 0); g.clearRect(0, 0, w, h);
      const N = d.meses.length, x0 = (this.x0 = 46), x1 = w - 60, y0 = 12, alto2 = 66, y1 = h - alto2 - 34, paso = (this.paso = (x1 - x0) / N), Y = (v) => y1 - ((y1 - y0) * v) / this.tope;
      const hasta = Math.floor(pos); if (hasta !== this.ult) { this.ult = hasta; this.nace = performance.now(); }      // la barra nueva crece y queda completa
      const X = (i) => x0 + paso * (i + 0.5);
      g.font = "500 10.5px " + FC.MONO; g.textBaseline = "middle"; g.textAlign = "right"; g.lineWidth = 1;
      for (let v = 0; v <= this.tope; v += 4e6) { g.strokeStyle = "rgba(28,39,68,.85)"; g.beginPath(); g.moveTo(x0, Y(v)); g.lineTo(x1, Y(v)); g.stroke(); g.fillStyle = C.tinta3; g.fillText(v / 1e6 + " M", x0 - 6, Y(v)); }
      // banda descriptiva de los 12 meses anteriores
      const m = d.mensual; g.beginPath(); let abierto = false; const bajo = [];
      for (let i = 0; i <= hasta; i++) if (m.media_previa[i] !== null) { const s = m.desv_previa[i] || 0; abierto ? g.lineTo(X(i), Y(m.media_previa[i] + s)) : g.moveTo(X(i), Y(m.media_previa[i] + s)); abierto = true; bajo.push([X(i), Y(Math.max(0, m.media_previa[i] - s))]); }
      if (abierto) { bajo.reverse().forEach((p) => g.lineTo(p[0], p[1])); g.closePath(); g.fillStyle = "rgba(34,211,238,.12)"; g.fill();
        g.beginPath(); let k = false; for (let i = 0; i <= hasta; i++) if (m.media_previa[i] !== null) { k ? g.lineTo(X(i), Y(m.media_previa[i])) : g.moveTo(X(i), Y(m.media_previa[i])); k = true; } g.strokeStyle = C.turquesa; g.lineWidth = 1.8; g.stroke(); }
      // reforma
      const xr = x0 + paso * d.reforma; g.setLineDash([3, 4]); g.strokeStyle = "rgba(167,139,250,.75)"; g.lineWidth = 1.2; g.beginPath(); g.moveTo(xr, y0); g.lineTo(xr, h - 20); g.stroke(); g.setLineDash([]);
      g.fillStyle = C.violeta; g.textAlign = "right"; g.fillText("reforma (dic 2025)", xr - 5, y0 + 5);
      // barras apiladas por plataforma
      for (let i = 0; i < N; i++) {
        const crece = i < hasta ? 1 : i === hasta ? (FC.quieto ? 1 : 0.2 + 0.8 * FC.suave((performance.now() - this.nace) / 320)) : 0; if (!crece) continue;
        let y = y1; for (const p of d.plataformas) { const v = (p.monto[i] || 0) * crece; if (!v) continue; const a = Math.max(1.2, y1 - Y(v)); g.fillStyle = i === hasta ? p.color : FC.rgba(p.color, 0.82); g.fillRect(x0 + paso * i + paso * 0.14, y - a, paso * 0.72, a); y -= a; }
      }
      // precio del mes a la derecha, como en un gráfico de mercado
      const val = m.monto[hasta]; if (val) { const y = Y(val); g.setLineDash([2, 3]); g.strokeStyle = C.oro; g.beginPath(); g.moveTo(X(hasta), y); g.lineTo(x1, y); g.stroke(); g.setLineDash([]); FC.caja(g, x1 + 2, y - 9, 56, 18, 4); g.fillStyle = C.oro; g.fill(); g.fillStyle = "#1A1203"; g.font = "700 10.5px " + FC.MONO; g.textAlign = "center"; g.fillText(FC.num(val / 1e6, 2) + " M", x1 + 30, y); }
      // panel inferior: TEA observada (≤360 d)
      const ya = y1 + 20, yb = ya + alto2 - 8, Z = (v) => yb - ((yb - ya) * (v - 25)) / 45; g.font = "500 10px " + FC.MONO; g.textAlign = "right"; g.fillStyle = C.tinta3;
      [30, 50, 70].forEach((v) => { g.strokeStyle = "rgba(28,39,68,.7)"; g.lineWidth = 1; g.beginPath(); g.moveTo(x0, Z(v)); g.lineTo(x1, Z(v)); g.stroke(); g.fillText(v + " %", x0 - 6, Z(v)); });
      d.tasas.filter((t) => t.tramo && t.tramo[1] === 12).forEach((t) => { g.beginPath(); for (let i = 0; i <= hasta; i++) i ? g.lineTo(X(i), Z(t.v[i])) : g.moveTo(X(i), Z(t.v[i])); g.strokeStyle = t.color; g.lineWidth = 1.6; g.stroke(); g.beginPath(); g.arc(X(hasta), Z(t.v[hasta]), 2.6, 0, 7); g.fillStyle = t.color; g.fill(); });
      g.textAlign = "left"; g.fillStyle = C.tinta2; g.fillText("TEA de bancos y cajas ≤360 d (BCRP): referencia, no es el precio del FPF", x0 + 4, ya - 3);
      // años
      g.textAlign = "left"; g.fillStyle = C.tinta2; d.meses.forEach((p, i) => { if (p.endsWith("-01")) { g.fillStyle = C.tinta2; g.fillText(p.slice(0, 4), x0 + paso * i + 2, h - 8); g.strokeStyle = "rgba(28,39,68,.6)"; g.beginPath(); g.moveTo(x0 + paso * i, y0); g.lineTo(x0 + paso * i, h - 16); g.stroke(); } });
      // línea de tiempo
      g.strokeStyle = "rgba(251,191,36,.85)"; g.lineWidth = 1.4; g.beginPath(); g.moveTo(X(hasta), y0); g.lineTo(X(hasta), h - 18); g.stroke();
      if (this.cursor) {
        const i = this.cursor.m; g.strokeStyle = "rgba(232,238,252,.45)"; g.setLineDash([3, 3]); g.lineWidth = 1; g.beginPath(); g.moveTo(X(i), y0); g.lineTo(X(i), h - 18); g.stroke(); g.setLineDash([]);
        const L = [[d.etiquetas[i]]];
        if (m.monto[i]) { L.push(["Total " + FC.soles(m.monto[i]), C.oro]); d.plataformas.forEach((p) => { if (p.monto[i]) L.push([p.nombre + " " + FC.soles(p.monto[i]), p.color]); }); } else L.push(["sin proyectos financiados", C.tinta3]);
        if (m.no_obtenidas[i]) L.push([m.no_obtenidas[i] + " plataforma(s) sin respuesta del portal", C.coral]);
        FC.globo(g, X(i), Math.max(90, this.cursor.y), L, w, h);
      }
    }
  }

  // ---------------------------------------------------------------- flujo del dinero
  class Flujo {
    constructor(cv, d) { this.cv = cv; this.d = d; this.g = cv.getContext("2d"); this.puntos = new Map(); }
    dibujar(mes, dt) {
      const g = this.g, d = this.d, { w, h, r } = FC.medir(this.cv); if (w < 40) return;
      g.setTransform(r, 0, 0, r, 0, 0); g.clearRect(0, 0, w, h);
      const f = d.flujos[mes], xa = 22, xb = w - 22, arriba = 62, abajo = h - 10, total = Object.values(f).reduce((s, v) => s + v.reduce((a, b) => a + b, 0), 0);
      g.textBaseline = "middle"; g.textAlign = "left"; g.font = "700 11px " + FC.SANS; g.fillStyle = C.tinta3; g.fillText("PLATAFORMA", 12, 20); g.textAlign = "right"; g.fillText("QUIÉN LO RECIBE", w - 12, 20);
      g.textAlign = "center"; g.font = "700 12px " + FC.MONO; g.fillStyle = C.oro; g.fillText("12 meses a " + d.etiquetas[mes] + " · " + FC.soles(total), w / 2, 44);
      if (!total) { g.fillStyle = C.tinta3; g.font = "500 12px " + FC.MONO; g.fillText("sin proyectos financiados todavía", w / 2, h / 2); return; }
      const P = d.plataformas, tipos = d.tipos.slice(0, 2), grueso = Math.max(40, abajo - arriba - P.length * 46);
      const color = [C.azul, C.oro], ancho = (v) => Math.max(1.2, grueso * (v / total)), rutas = [];
      const suma = (n) => (f[n] || [0, 0, 0]).slice(0, 2).reduce((a, b) => a + b, 0), porTipo = tipos.map((_, j) => P.reduce((a, p) => a + (f[p.nombre] || [0, 0, 0])[j], 0));
      // cada nodo ocupa lo que mide su franja más el espacio de su rótulo; las posiciones se deslizan al cambiar de mes
      const reparte = (vs) => { const libre = (abajo - arriba - vs.reduce((a, v) => a + Math.max(8, ancho(v)), 0)) / vs.length; let y = arriba; return vs.map((v) => { const a = Math.max(8, ancho(v)); y += libre; const c = y + a / 2; y += a; return c - 2; }); };
      const meta = { p: reparte(P.map((p) => suma(p.nombre))), t: reparte(porTipo) }; if (!this.y || this.y.h !== h) this.y = { p: meta.p.slice(), t: meta.t.slice(), h };
      ["p", "t"].forEach((k) => meta[k].forEach((v, i) => { this.y[k][i] += (v - this.y[k][i]) * Math.min(1, dt * 6); })); const yP = this.y.p, yT = this.y.t;
      P.forEach((p, i) => tipos.forEach((t, j) => { const v = (f[p.nombre] || [0, 0, 0])[j]; if (v > 0) rutas.push({ k: p.nombre + j, p, i, j, v }); }));
      const curva = (q) => { const y0 = yP[q.i], y1 = yT[q.j], mx = (xa + xb) / 2; return (t) => { const u = 1 - t; return [u * u * u * xa + 3 * u * u * t * mx + 3 * u * t * t * mx + t * t * t * xb, u * u * u * y0 + 3 * u * u * t * y0 + 3 * u * t * t * y1 + t * t * t * y1]; }; };
      rutas.sort((a, b) => b.v - a.v).forEach((q) => { const c = curva(q); g.beginPath(); for (let k = 0; k <= 30; k++) { const p = c(k / 30); k ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); } g.lineWidth = ancho(q.v); g.lineCap = "butt"; const gr = g.createLinearGradient(xa, 0, xb, 0); gr.addColorStop(0, FC.rgba(q.p.color, 0.3)); gr.addColorStop(1, FC.rgba(color[q.j], 0.22)); g.strokeStyle = gr; g.stroke(); });
      rutas.forEach((q) => {
        const n = Math.max(1, Math.round(q.v / 5e5)); let L = this.puntos.get(q.k); if (!L) this.puntos.set(q.k, (L = []));
        while (L.length < n) L.push({ t: Math.random(), y: Math.random() * 2 - 1, v: 0.1 + Math.random() * 0.08 }); if (L.length > n) L.length = n;
        const c = curva(q), a = ancho(q.v) / 2; g.fillStyle = q.p.color;
        L.forEach((p) => { if (!FC.quieto) p.t = (p.t + dt * p.v) % 1; const z = c(p.t), o = Math.min(1, Math.min(p.t, 1 - p.t) * 8); g.globalAlpha = 0.95 * o; g.beginPath(); g.arc(z[0], z[1] + p.y * Math.max(0, a - 2), n === 1 ? 2.8 : 1.9, 0, 7); g.fill(); }); g.globalAlpha = 1;
      });
      const nodo = (x, y, v, txt, col, lado) => { const a = Math.max(8, ancho(v)); FC.caja(g, x - 5, y - a / 2, 10, a, 4); g.fillStyle = v ? col : FC.rgba(col, 0.3); g.fill(); g.textAlign = lado; g.font = "700 11.5px " + FC.SANS; g.fillStyle = v ? C.tinta : C.tinta3; const tx = lado === "left" ? x - 8 : x + 8; g.fillText(txt, tx, y - a / 2 - 21); g.font = "600 10.5px " + FC.MONO; g.fillStyle = v ? C.tinta2 : C.tinta3; g.fillText(v ? FC.soles(v) + " · " + FC.num((100 * v) / total, 1) + " %" : "sin monto", tx, y - a / 2 - 8); };
      P.forEach((p, i) => nodo(xa, yP[i], suma(p.nombre), p.nombre, p.color, "left"));
      tipos.forEach((t, j) => nodo(xb, yT[j], porTipo[j], t, color[j], "right"));
    }
  }

  // ---------------------------------------------------------------- tablero del mes
  const SIT = { maximo: ["MÁXIMO HISTÓRICO", "El monto de este mes es el más alto hasta ese momento."],
    sobre: ["SOBRE LO HABITUAL", "El monto supera la franja de los 12 meses anteriores (media + 1 desviación)."],
    dentro: ["DENTRO DE LO HABITUAL", "El monto está dentro de la franja de los 12 meses anteriores."],
    bajo: ["BAJO LO HABITUAL", "El monto está por debajo de la franja de los 12 meses anteriores (media − 1 desviación)."],
    sin_ventana: ["AÚN SIN 12 MESES", "Todavía no hay 12 meses previos con los que comparar."],
    sin_actividad: ["SIN ACTIVIDAD", "No hay proyectos financiados registrados en este mes."] };
  FC.tablero = function (d, i) {
    const m = d.mensual, s = SIT[m.situacion[i]], bco = d.tasas.find((t) => t.id === "tea_bcos_pyme_360"), caj = d.tasas.find((t) => t.id === "tea_cmac_pyme_360"), el = (x) => document.getElementById(x);
    el("e-mes").textContent = d.etiquetas[i]; el("e-sit").textContent = s[0]; el("e-sit").className = "sit " + m.situacion[i]; el("e-ex").textContent = s[1] + " Es una descripción, no una señal de inversión.";
    const filas = [["Monto del mes", m.monto[i] ? FC.soles(m.monto[i]) : "—"], ["Frente al año anterior", m.interanual_pct[i] === null ? "—" : FC.signo(m.interanual_pct[i], 1, "%"), m.interanual_pct[i]],
      ["Acumulado 12 meses", FC.soles(m.acumulado_12m[i])], ["Publicados / financiados", m.publicados[i] === null ? "—" : FC.num(m.publicados[i]) + " / " + FC.num(m.financiados[i])],
      ["Colocación 12 meses", m.colocacion_12m_pct[i] === null ? "—" : FC.num(m.colocacion_12m_pct[i], 1) + " %"], ["Parte de la líder (12 m)", m.lider_12m_pct[i] === null ? "—" : FC.num(m.lider_12m_pct[i], 1) + " %"],
      ["IHH (12 m)", FC.num(m.ihh_12m[i])], ["TEA bancos pyme ≤360 d", FC.num(bco.v[i], 2) + " %"], ["TEA cajas mun. pyme ≤360 d", FC.num(caj.v[i], 2) + " %"],
      ["Sin respuesta del portal", m.no_obtenidas[i] ? m.no_obtenidas[i] + " de 6" : "0 de 6"]];
    const dl = el("e-filas"); if (!dl.children.length) filas.forEach(() => { dl.append(document.createElement("dt"), document.createElement("dd")); });
    filas.forEach((f, k) => { dl.children[2 * k].textContent = f[0]; const dd = dl.children[2 * k + 1]; dd.textContent = f[1]; dd.className = f[2] === undefined || f[2] === null ? "" : f[2] > 0 ? "up" : "dn"; });
  };

  // ---------------------------------------------------------------- consola
  FC.Consola = class {
    constructor(cont, log) { this.cont = cont; this.log = log; this.i = 0; this.espera = 0;
      document.getElementById("c-ex").textContent = "Muestra de " + log.lineas.length + " de las " + FC.num(log.total) + " líneas del registro (" + FC.num(log.http200) + " respuestas HTTP 200). El número L es la línea del archivo: se puede comprobar."; }
    paso(dt) {
      this.espera -= dt; if (this.espera > 0 || !this.log.lineas.length) return;
      if (this.i >= this.log.lineas.length) { this.i = 0; this.espera = 2.5; this._linea(null); return; }
      const l = this.log.lineas[this.i++]; this._linea(l); this.espera = FC.quieto ? 3 : /HTTP/.test(l.texto) ? 0.32 : 0.55;
    }
    _linea(l) {
      const e = document.createElement("div"), s = (t, x) => { const n = document.createElement(t); n.textContent = x; return n; };
      this.cont.querySelectorAll(".cur").forEach((x) => x.classList.remove("cur")); e.className = "cur";
      if (!l) e.append(s("u", "— fin de la muestra; se repite desde la primera línea —"));
      else { e.append(s("u", "L" + l.n + " " + l.hora.slice(5) + " "), s("q", l.script.slice(0, 2) === "01" ? "api " : "web ")); const m = /^(HTTP 200|.*?\bOK\b)(.*)$/.exec(l.texto); if (m) e.append(s("s", m[1]), document.createTextNode(m[2])); else e.append(document.createTextNode(l.texto)); if (l.nivel !== "INFO") e.classList.add("w"); }
      this.cont.append(e); while (this.cont.children.length > 34) this.cont.firstChild.remove();
    }
  };
  FC.Replay = Replay; FC.Flujo = Flujo;
})();
