// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Fecha: 2026-11-24
// Utilidades comunes de la terminal: formatos (los del artículo), rampa de color, lienzos y matemática 3D.
(function () {
  "use strict";
  const FC = (window.FC = {});
  FC.C = { tinta: "#E8EEFC", tinta2: "#A9B6D3", tinta3: "#7483A6", borde: "#1C2744", azul: "#4F8CFF", turquesa: "#22D3EE",
           verde: "#34D399", coral: "#FB7185", oro: "#FBBF24", violeta: "#A78BFA" };
  FC.MONO = '"JetBrains Mono", Consolas, monospace';
  FC.SANS = '"Plus Jakarta Sans", "Segoe UI", sans-serif';
  FC.quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Punto decimal y espacio de miles, como en el artículo; null = sin dato
  FC.num = function (x, dec) {
    if (x === null || x === undefined || !isFinite(x)) return "—";
    const [e, d] = Math.abs(x).toFixed(dec || 0).split(".");
    return (x < 0 ? "−" : "") + e.replace(/\B(?=(\d{3})+(?!\d))/g, " ") + (d ? "." + d : "");
  };
  FC.soles = function (x) {
    if (x === null || x === undefined) return "—";
    return Math.abs(x) < 1e6 && x !== 0 ? "S/ " + FC.num(x / 1e3, 1) + " mil" : "S/ " + FC.num(x / 1e6, 2) + " M";
  };
  FC.signo = (x, dec, u) => (x === null || x === undefined ? "—" : (x > 0 ? "+" : "") + FC.num(x, dec) + " " + u);

  // Rampa secuencial propia: de noche a amanecer (más alto = más claro)
  FC.RAMPA = [[23, 26, 74], [37, 71, 208], [14, 148, 214], [16, 185, 150], [132, 204, 60], [251, 191, 36], [255, 244, 204]];
  FC.color = function (t, a) {
    const f = Math.min(1, Math.max(0, t)) * 6, i = Math.min(5, Math.floor(f)), k = f - i;
    const c = FC.RAMPA[i].map((v, j) => Math.round(v + (FC.RAMPA[i + 1][j] - v) * k));
    return "rgba(" + c.join(",") + "," + (a === undefined ? 1 : a) + ")";
  };
  FC.rgba = (hex, a) => "rgba(" + [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)).join(",") + "," + a + ")";
  FC.rgb01 = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255);

  FC.calidad = 1;   // baja sola en equipos lentos (principal.js)
  // Ajusta un lienzo a la densidad de la pantalla; devuelve su tamaño en píxeles CSS
  FC.medir = function (cv, es3d) {
    const d = Math.min(2, window.devicePixelRatio || 1) * FC.calidad, r = es3d ? d : Math.max(1, d), w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== Math.round(w * r) || cv.height !== Math.round(h * r)) { cv.width = Math.round(w * r); cv.height = Math.round(h * r); }
    return { w, h, r };
  };
  FC.caja = function (g, x, y, w, h, r) {
    g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
  };
  // Recuadro de lectura junto a un punto; líneas: [texto, color]
  FC.globo = function (g, x, y, lineas, W, H) {
    g.font = "600 11.5px " + FC.MONO;
    const w = Math.max(...lineas.map((l) => g.measureText(l[0]).width)) + 20, h = lineas.length * 17 + 12;
    let px = x + 14, py = y - h - 12;
    if (px + w > W - 4) px = x - w - 14;
    if (px < 4) px = 4;
    if (py < 4) py = Math.min(H - h - 4, y + 14);
    FC.caja(g, px, py, w, h, 8); g.fillStyle = "rgba(6,9,19,.94)"; g.fill(); g.strokeStyle = "rgba(79,140,255,.6)"; g.lineWidth = 1; g.stroke();
    g.textAlign = "left"; g.textBaseline = "middle";
    lineas.forEach((l, i) => { g.fillStyle = l[1] || FC.C.tinta; g.fillText(l[0], px + 10, py + 15 + i * 17); });
  };

  // ---- matrices 4×4 por columnas (convención de WebGL)
  FC.perspectiva = function (fov, asp, n, f) {
    const t = 1 / Math.tan(fov / 2);
    return [t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) / (n - f), -1, 0, 0, (2 * f * n) / (n - f), 0];
  };
  const resta = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const cruz = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const punto = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  FC.norma = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  FC.mirar = function (ojo, fin, arriba) {
    const z = FC.norma(resta(ojo, fin)), x = FC.norma(cruz(arriba, z)), y = cruz(z, x);
    return [x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0, -punto(x, ojo), -punto(y, ojo), -punto(z, ojo), 1];
  };
  FC.mul = function (a, b) {
    const o = new Array(16);
    for (let c = 0; c < 4; c++) for (let f = 0; f < 4; f++) { let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + f] * b[c * 4 + k]; o[c * 4 + f] = s; }
    return o;
  };
  FC.suave = (t) => { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); };
})();
