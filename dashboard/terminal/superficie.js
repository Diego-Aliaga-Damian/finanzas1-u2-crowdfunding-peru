// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Fecha: 2026-11-24
// Motor 3D propio en WebGL2, sin librerías. Dibuja tres formas, según lo que son los datos:
//   malla  = función continua de dos variables (costo del crédito según TEA y plazo)
//   cintas = una serie por categoría en el tiempo (las categorías no se unen entre sí)
//   barras = una columna por mes observado (los meses sin dato no se dibujan)
// Si el navegador no tiene WebGL2, la misma escena se dibuja en alambre con el lienzo 2D.
(function () {
  "use strict";
  const FC = window.FC;
  const AX = 1.75, AY = 1.05, AZ = 0.86;   // semiancho, semifondo y alto de la caja

  const VERT = `#version 300 es
  in vec3 aPos; in vec3 aNor; in vec3 aDat;             // aDat = (u, v, valor 0-1); en barras u = índice del mes
  uniform mat4 uMVP; uniform float uGrow; uniform float uCorte; uniform int uModo;
  out vec3 vNor; out vec3 vDat; out vec3 vPos;
  void main(){
    float g = clamp(uGrow * 1.9 - length(aPos.xy) * .5, 0., 1.); g = g * g * (3. - 2. * g);
    vec3 p = aPos; p.z *= g;
    if (uModo == 2) p.z *= clamp(uCorte + 1. - aDat.x, 0., 1.);
    if (uModo == 3) p.z = .001;
    vNor = aNor; vDat = aDat; vPos = p; gl_Position = uMVP * vec4(p, 1.);
  }`;
  const FRAG = `#version 300 es
  precision highp float; precision highp int;
  in vec3 vNor; in vec3 vDat; in vec3 vPos; out vec4 sal;
  uniform vec3 uRampa[7]; uniform vec2 uMalla; uniform float uBarrido, uCorte, uGrow; uniform int uModo; uniform vec3 uOjo; uniform vec4 uTinta;
  vec3 rampa(float t){ float f = clamp(t, 0., 1.) * 6.; int i = min(int(floor(f)), 5); return mix(uRampa[i], uRampa[i + 1], f - float(i)); }
  float linea(float k, float g){ float c = abs(fract(k - .5) - .5) / max(fwidth(k), 1e-5); return 1. - min(c / g, 1.); }
  void main(){
    if (uModo == 5) { sal = uTinta; return; }
    if (uModo == 3) {                                    // proyección de curvas de nivel en el piso
      float n = linea(vDat.z * 12., 1.1) ; sal = vec4(rampa(vDat.z) * .9 + .1, n * .6 * uGrow); if (sal.a < .02) discard; return;
    }
    if ((uModo == 1 || uModo == 4) && vDat.x > uCorte) discard;
    if (uModo == 2 && vDat.x > uCorte + .99) discard;     // los meses futuros del replay no se adelantan
    vec3 col = rampa(vDat.z);
    if (uModo == 4) { float a = smoothstep(0., 1., vPos.z / max(vDat.y, .001)); sal = vec4(col, mix(.03, .42, a) * uGrow); return; }
    vec3 N = normalize(vNor), V = normalize(uOjo - vPos), L = normalize(vec3(-.45, -.55, 1.));
    if (dot(N, V) < 0.) N = -N;
    float dif = .58 + .46 * max(dot(N, L), 0.), esp = pow(max(dot(reflect(-L, N), V), 0.), 26.) * .22, borde = pow(1. - max(dot(N, V), 0.), 3.) * .22;
    vec3 c = col * dif + esp + col * borde;
    if (uModo == 0) {
      vec2 g = vDat.xy * uMalla;
      c = mix(c, c * 1.55 + .06, max(linea(g.x, 1.), linea(g.y, 1.)) * .34);
      c = mix(c, vec3(1.), linea(vDat.z * 12., 1.2) * .20);
      float b = exp(-pow((vDat.x - uBarrido) * 26., 2.)); c += vec3(.75, .9, 1.) * b * .55;
    }
    if (uModo == 1) { c = mix(c, vec3(1.), exp(-pow((vDat.x - uCorte) * 90., 2.)) * .85); c = mix(c, c * 1.35 + .05, smoothstep(.75, 1., abs(vDat.y * 2. - 1.)) * .6); }
    if (uModo == 2) { float h = 1. - clamp(abs(vDat.x - floor(uCorte)) , 0., 1.); c += vec3(.35, .30, .18) * h; c = mix(c, c * .62, smoothstep(.25, 0., vPos.z) * .6); }
    sal = vec4(c, 1.);
  }`;

  class Superficie {
    constructor(lienzo, capa) {
      this.gl = lienzo; this.capa = capa; this.ctx = capa.getContext("2d");
      this.yaw0 = -0.55; this.pitch0 = 0.43; this.yaw = this.yaw0; this.pitch = this.pitch0; this.zoom = 1;
      this.crece = 0; this.cursor = null; this.corte = 0; this.lineas = []; this.t = 0;
      const g = (this.g = lienzo.getContext("webgl2", { antialias: true, alpha: true, premultipliedAlpha: false }));
      if (g) this._programa();
      this._eventos();
    }

    _programa() {
      const g = this.g, sh = (t, s) => { const x = g.createShader(t); g.shaderSource(x, s); g.compileShader(x);
        if (!g.getShaderParameter(x, g.COMPILE_STATUS)) throw new Error(g.getShaderInfoLog(x)); return x; };
      try {
        const p = (this.p = g.createProgram());
        g.attachShader(p, sh(g.VERTEX_SHADER, VERT)); g.attachShader(p, sh(g.FRAGMENT_SHADER, FRAG)); g.linkProgram(p);
        if (!g.getProgramParameter(p, g.LINK_STATUS)) throw new Error(g.getProgramInfoLog(p));
      } catch (e) { console.warn("WebGL no disponible:", e.message); this.g = null; return; }
      this.u = {}; ["uMVP", "uGrow", "uCorte", "uModo", "uRampa", "uMalla", "uBarrido", "uOjo", "uTinta"].forEach((n) => (this.u[n] = g.getUniformLocation(this.p, n)));
      this.lugar = { aPos: g.getAttribLocation(this.p, "aPos"), aNor: g.getAttribLocation(this.p, "aNor"), aDat: g.getAttribLocation(this.p, "aDat") };
      this.mallas = {}; this.bufLineas = this._vao();
    }

    _vao() {
      const g = this.g, v = g.createVertexArray(), b = g.createBuffer();
      g.bindVertexArray(v); g.bindBuffer(g.ARRAY_BUFFER, b);
      [["aPos", 0], ["aNor", 12], ["aDat", 24]].forEach(([n, o]) => { if (this.lugar[n] >= 0) { g.enableVertexAttribArray(this.lugar[n]); g.vertexAttribPointer(this.lugar[n], 3, g.FLOAT, false, 36, o); } });
      g.bindVertexArray(null);
      return { v, b, n: 0 };
    }
    _cargar(m, datos) {
      const g = this.g; g.bindBuffer(g.ARRAY_BUFFER, m.b); g.bufferData(g.ARRAY_BUFFER, new Float32Array(datos), g.DYNAMIC_DRAW); m.n = datos.length / 9; return m;
    }

    // ------------------------------------------------------------------ geometría
    fijar(s) {
      this.s = s; this.crece = FC.quieto ? 1 : 0; this.puntos = []; this.cursor = null;
      const vx = s.ejeX.valores, vy = s.ejeY.valores, margen = s.tipo === "malla" ? 0 : 0.55;
      const x0 = vx[0] - (s.tipo === "barras" ? 0.6 : 0), x1 = vx[vx.length - 1] + (s.tipo === "barras" ? 0.6 : 0), y0 = vy[0] - margen, y1 = vy[vy.length - 1] + margen;
      this.px = (v) => -AX + (2 * AX * (v - x0)) / (x1 - x0);
      this.py = (v) => -AY + (2 * AY * (v - y0)) / (y1 - y0);
      this.pz = (v) => (AZ * v) / s.ejeZ.max;
      this.max = Math.max(...s.z.flat().filter((v) => v !== null)); this.min = Math.min(...s.z.flat().filter((v) => v !== null));
      this.norm = (v) => (s.tipo === "malla" ? (v - this.min) / (this.max - this.min) : Math.max(0, v) / this.max);
      s.z.forEach((f, j) => f.forEach((v, i) => { if (v !== null && (s.tipo !== "barras" || v > 0)) this.puntos.push({ i, j, v, p: [this.px(vx[i]), this.py(vy[j]), this.pz(v)] }); }));
      if (!this.g) return;
      const d = { malla: () => this._malla(), cintas: () => this._cintas(), barras: () => this._barras() }[s.tipo]();
      const m = (this.mallas[s.id] = this.mallas[s.id] || { a: this._vao(), b: this._vao() });
      this._cargar(m.a, d.a); this._cargar(m.b, d.b);
    }

    _malla() {
      const s = this.s, vx = s.ejeX.valores, vy = s.ejeY.valores, nx = vx.length, ny = vy.length, P = [], N = [];
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) P.push([this.px(vx[i]), this.py(vy[j]), this.pz(s.z[j][i])]);
      const en = (j, i) => P[Math.min(ny - 1, Math.max(0, j)) * nx + Math.min(nx - 1, Math.max(0, i))];
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const a = en(j, i + 1), b = en(j, i - 1), c = en(j + 1, i), e = en(j - 1, i);
        const dx = (a[2] - b[2]) / (a[0] - b[0]), dy = (c[2] - e[2]) / (c[1] - e[1]); N.push(FC.norma([-dx, -dy, 1]));
      }
      const o = [], v = (j, i) => { const k = j * nx + i; o.push(...P[k], ...N[k], i / (nx - 1), j / (ny - 1), this.norm(s.z[j][i])); };
      for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) { v(j, i); v(j, i + 1); v(j + 1, i + 1); v(j, i); v(j + 1, i + 1); v(j + 1, i); }
      return { a: o, b: [] };
    }

    _cintas() {
      const s = this.s, vx = s.ejeX.valores, vy = s.ejeY.valores, a = [], b = [], W = (0.33 * 2 * AY) / (vy.length + 0.1);
      s.z.forEach((f, j) => {
        const y = this.py(vy[j]);
        for (let i = 0; i < f.length - 1; i++) {
          if (f[i] === null || f[i + 1] === null) continue;
          const xa = this.px(vx[i]), xb = this.px(vx[i + 1]), za = this.pz(f[i]), zb = this.pz(f[i + 1]), n = FC.norma([-(zb - za) / (xb - xa), 0, 1]);
          const ua = i / (f.length - 1), ub = (i + 1) / (f.length - 1), na = this.norm(f[i]), nb = this.norm(f[i + 1]);
          const t = (x, yy, z, u, v, c) => a.push(x, yy, z, ...n, u, v, c);
          t(xa, y - W, za, ua, 0, na); t(xb, y - W, zb, ub, 0, nb); t(xb, y + W, zb, ub, 1, nb);
          t(xa, y - W, za, ua, 0, na); t(xb, y + W, zb, ub, 1, nb); t(xa, y + W, za, ua, 1, na);
          [-W, W].forEach((k) => {                        // cortinas hasta el piso (aDat.y = altura de la cinta)
            const q = (x, z, u, h, c) => b.push(x, y + k, z, 0, 1, 0, u, h, c);
            q(xa, 0, ua, za, na); q(xb, 0, ub, zb, nb); q(xb, zb, ub, zb, nb); q(xa, 0, ua, za, na); q(xb, zb, ub, zb, nb); q(xa, za, ua, za, na);
          });
        }
      });
      return { a, b };
    }

    _barras() {
      const s = this.s, vx = s.ejeX.valores, vy = s.ejeY.valores, a = [], dx = (0.36 * 2 * AX) / (vx.length + 0.2), dy = (0.33 * 2 * AY) / (vy.length + 0.1);
      s.z.forEach((f, j) => f.forEach((v, i) => {
        if (v === null || v <= 0) return;
        const x = this.px(vx[i]), y = this.py(vy[j]), z = this.pz(v), k = s.indice[j][i], c = this.norm(v);
        const cara = (p, n) => [0, 1, 2, 0, 2, 3].forEach((q) => a.push(...p[q], ...n, k, 0, p[q][2] > 0 ? c : c * 0.55));
        const A = [x - dx, y - dy], B = [x + dx, y - dy], C = [x + dx, y + dy], D = [x - dx, y + dy], z0 = (q) => [...q, 0], z1 = (q) => [...q, z];
        cara([z1(A), z1(B), z1(C), z1(D)], [0, 0, 1]); cara([z0(A), z0(B), z1(B), z1(A)], [0, -1, 0]); cara([z0(B), z0(C), z1(C), z1(B)], [1, 0, 0]);
        cara([z0(C), z0(D), z1(D), z1(C)], [0, 1, 0]); cara([z0(D), z0(A), z1(A), z1(D)], [-1, 0, 0]);
      }));
      return { a, b: [] };
    }

    // ------------------------------------------------------------------ cámara
    _camara(w, h) {
      const vaiven = FC.quieto || this.agarre || this.cursor ? 0 : Math.sin(this.t * 0.32) * 0.16;
      this.vv = (this.vv || 0) + (vaiven - (this.vv || 0)) * 0.05;
      this.w = w; this.h = h;
      const asp = w / h, centro = [0, 0, 0.34], P = FC.perspectiva(0.72, asp, 0.1, 40);
      const ojo = (yaw, l) => [centro[0] + l * Math.sin(yaw) * Math.cos(this.pitch), centro[1] - l * Math.cos(yaw) * Math.cos(this.pitch), centro[2] + l * Math.sin(this.pitch)];
      const ver = (yaw, l) => FC.mul(P, FC.mirar(ojo(yaw, l), centro, [0, 0, 1]));
      // encuadre automático: la distancia con la que la caja y sus rótulos llenan el panel
      const esq = []; [-1, 1].forEach((x) => [-1, 1].forEach((y) => [0, 1].forEach((z) => esq.push([x * AX * (z ? 1 : 1.14), y * AY * (z ? 1 : 1.28), z * AZ]))));
      const caja = (M) => { let a = 9, b = -9, c = 9, d = -9; esq.forEach((p) => { const q = M[3] * p[0] + M[7] * p[1] + M[11] * p[2] + M[15], x = (M[0] * p[0] + M[4] * p[1] + M[8] * p[2] + M[12]) / q, y = (M[1] * p[0] + M[5] * p[1] + M[9] * p[2] + M[13]) / q; a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); }); return [a, b, c, d]; };
      let cerca = 2.2, lejos = 12; for (let k = 0; k < 14; k++) { const l = (cerca + lejos) / 2, q = caja(ver(this.yaw, l)); if (q[1] - q[0] > 1.72 || q[3] - q[2] > 1.84) cerca = l; else lejos = l; }
      const M0 = ver(this.yaw, lejos), q = caja(M0), tx = -(q[0] + q[1]) / 2 + (w > 700 && this.s.tipo !== "barras" ? 0.12 : 0), ty = -(q[2] + q[3]) / 2, l = lejos / this.zoom, yaw = this.yaw + this.vv;
      this.ojo = ojo(yaw, l); this.M = ver(yaw, l);
      for (let k = 0; k < 4; k++) { this.M[k * 4] += tx * this.M[k * 4 + 3]; this.M[k * 4 + 1] += ty * this.M[k * 4 + 3]; }
    }
    proyectar(p) {
      const m = this.M, x = m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12], y = m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13], q = m[3] * p[0] + m[7] * p[1] + m[11] * p[2] + m[15];
      return [((x / q + 1) / 2) * this.w, ((1 - y / q) / 2) * this.h, q];
    }
    // Altura de la malla en un punto cualquiera (interpolación bilineal de la propia malla)
    altura(vx, vy) {
      const s = this.s, X = s.ejeX.valores, Y = s.ejeY.valores, busca = (A, v) => { let k = 0; while (k < A.length - 2 && A[k + 1] < v) k++; return [k, (v - A[k]) / (A[k + 1] - A[k])]; };
      const [i, a] = busca(X, vx), [j, b] = busca(Y, vy), z = s.z;
      return (z[j][i] * (1 - a) + z[j][i + 1] * a) * (1 - b) + (z[j + 1][i] * (1 - a) + z[j + 1][i + 1] * a) * b;
    }

    // ------------------------------------------------------------------ dibujo
    dibujar(t, dt) {
      if (!this.s) return;
      this.t = t; this.crece = Math.min(1, this.crece + dt / 1.5);
      const { w, h, r } = FC.medir(this.capa); FC.medir(this.gl, true);
      if (w < 2 || h < 2) return;
      this._camara(w, h);
      if (this.g) this._gl();
      const c = this.ctx; c.setTransform(r, 0, 0, r, 0, 0); c.clearRect(0, 0, w, h);
      if (!this.g) this._alambre();
      this._ejes(); this._lineasObservadas(); this._marcaMes(); this._colores(); this._lectura();
    }

    _caja() {                                              // rejilla del piso y de las dos paredes del fondo
      const fx = this.ojo[0] > 0 ? -AX : AX, fy = this.ojo[1] > 0 ? -AY : AY, o = [], l = (a, b) => o.push(...a, 0, 0, 1, 0, 0, 0, ...b, 0, 0, 1, 0, 0, 0);
      this.s.ejeZ.marcas.forEach(([v]) => { const z = this.pz(v); l([-AX, fy, z], [AX, fy, z]); l([fx, -AY, z], [fx, AY, z]); });
      this.s.ejeX.marcas.forEach(([v]) => { const x = this.px(v); l([x, -AY, 0], [x, AY, 0]); l([x, fy, 0], [x, fy, AZ]); });
      this.s.ejeY.marcas.forEach(([v]) => { const y = this.py(v); l([-AX, y, 0], [AX, y, 0]); l([fx, y, 0], [fx, y, AZ]); });
      l([-AX, -AY, 0], [AX, -AY, 0]); l([AX, -AY, 0], [AX, AY, 0]); l([AX, AY, 0], [-AX, AY, 0]); l([-AX, AY, 0], [-AX, -AY, 0]);
      return o;
    }

    _gl() {
      const g = this.g, u = this.u, s = this.s, m = this.mallas[s.id], modo = { malla: 0, cintas: 1, barras: 2 }[s.tipo];
      g.viewport(0, 0, this.gl.width, this.gl.height); g.clearColor(0, 0, 0, 0); g.clear(g.COLOR_BUFFER_BIT | g.DEPTH_BUFFER_BIT);
      g.useProgram(this.p); g.enable(g.DEPTH_TEST); g.enable(g.BLEND); g.blendFuncSeparate(g.SRC_ALPHA, g.ONE_MINUS_SRC_ALPHA, g.ONE, g.ONE_MINUS_SRC_ALPHA);
      g.uniformMatrix4fv(u.uMVP, false, this.M); g.uniform1f(u.uGrow, this.crece); g.uniform3fv(u.uRampa, FC.RAMPA.flat().map((v) => v / 255));
      g.uniform2f(u.uMalla, s.ejeX.valores.length - 1, s.ejeY.valores.length - 1); g.uniform3fv(u.uOjo, this.ojo);
      g.uniform1f(u.uBarrido, FC.quieto ? -9 : ((this.t * 0.16) % 1.5) - 0.25);
      g.uniform1f(u.uCorte, s.tipo === "cintas" ? Math.min(1, this.corte / (s.ejeX.valores.length - 1)) + 1e-4 : this.corte);
      const pinta = (malla, md, prim) => { if (!malla.n) return; g.uniform1i(u.uModo, md); g.bindVertexArray(malla.v); g.drawArrays(prim === undefined ? g.TRIANGLES : prim, 0, malla.n); };
      g.uniform4f(u.uTinta, 0.36, 0.48, 0.78, 0.3); pinta(this._cargar(this.bufLineas, this._caja()), 5, g.LINES);
      if (modo === 0) { g.depthMask(false); pinta(m.a, 3); g.depthMask(true); }
      pinta(m.a, modo);
      if (m.b.n) { g.depthMask(false); pinta(m.b, 4); g.depthMask(true); }
      g.bindVertexArray(null);
    }

    _alambre() {                                           // alternativa sin WebGL: las mismas filas como líneas
      const c = this.ctx, s = this.s, vx = s.ejeX.valores, vy = s.ejeY.valores;
      s.z.forEach((f, j) => { for (let i = 0; i < f.length - 1; i++) { if (f[i] === null || f[i + 1] === null) continue;
        const a = this.proyectar([this.px(vx[i]), this.py(vy[j]), this.pz(f[i])]), b = this.proyectar([this.px(vx[i + 1]), this.py(vy[j]), this.pz(f[i + 1])]);
        c.strokeStyle = FC.color(this.norm(f[i])); c.lineWidth = 1.5; c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke(); } });
    }

    _ejes() {
      const c = this.ctx, s = this.s, sx = this.ojo[0] > 0 ? 1 : -1, sy = this.ojo[1] > 0 ? 1 : -1, centro = this.proyectar([0, 0, 0]);
      c.font = "500 11px " + FC.MONO; c.textBaseline = "middle";
      const rotulo = (p, txt, dx, dy, color, peso) => { const q = this.proyectar(p), vx = q[0] - centro[0]; c.fillStyle = color || FC.C.tinta2; c.font = (peso || "500 11px ") + FC.MONO;
        c.textAlign = dx === undefined ? (vx > 30 ? "left" : vx < -30 ? "right" : "center") : "center"; c.fillText(txt, q[0] + (dx || 0), q[1] + (dy || 0)); };
      const salto = this.w < 520 ? 2 : 1;
      s.ejeX.marcas.forEach(([v, t], k) => { if (k % salto === 0) rotulo([this.px(v), sy * AY * 1.09, 0], t, 0, 6); });
      s.ejeY.marcas.forEach(([v, t]) => rotulo([sx * AX * 1.05, this.py(v), 0], t, undefined, 3));
      s.ejeZ.marcas.forEach(([v, t]) => { const q = this.proyectar([-sx * AX * 1.03, sy * AY * 1.03, this.pz(v)]); c.fillStyle = FC.C.tinta2; c.font = "500 11px " + FC.MONO; c.textAlign = -sx * Math.cos(this.yaw) > 0 === q[0] > this.w / 2 ? (q[0] > this.w / 2 ? "left" : "right") : (q[0] > this.w / 2 ? "left" : "right"); c.fillText(t, q[0] + (q[0] > this.w / 2 ? 4 : -4), q[1]); });
      rotulo([0, sy * AY * 1.4, 0], s.ejeX.titulo, 0, 10, FC.C.tinta3, "700 11px ");
      if (s.ejeY.titulo) { const q = this.proyectar([sx * AX * 1.2, 0, 0]); c.fillStyle = FC.C.tinta3; c.font = "700 11px " + FC.MONO; c.textAlign = q[0] > this.w / 2 ? "left" : "right"; c.fillText(s.ejeY.titulo, q[0], q[1] + 20); }
    }

    _lineasObservadas() {                                  // TEA observada del mes sobre la malla de costo
      if (this.s.tipo !== "malla" || !this.lineas.length) return;
      const c = this.ctx, X = this.s.ejeX.valores, a = FC.suave((this.crece - 0.7) / 0.3);
      if (a <= 0) return;
      this.lineas.forEach((l) => {
        if (!l.tramo || l.tea === null || l.tea < X[0] || l.tea > X[X.length - 1]) return;
        const pts = []; for (let k = 0; k <= 24; k++) { const n = l.tramo[0] + ((l.tramo[1] - l.tramo[0]) * k) / 24; pts.push(this.proyectar([this.px(l.tea), this.py(n), this.pz(this.altura(l.tea, n)) + 0.012])); }
        [[6, 0.22], [2.2, 1]].forEach(([g, o]) => { c.beginPath(); pts.forEach((p, k) => (k ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]))); c.strokeStyle = FC.rgba(l.color, o * a); c.lineWidth = g; c.lineCap = "round"; c.stroke(); });
        const f = pts[pts.length - 1]; c.beginPath(); c.arc(f[0], f[1], 4, 0, 7); c.fillStyle = FC.rgba(l.color, a); c.fill(); c.lineWidth = 1.5; c.strokeStyle = "rgba(6,9,19," + a + ")"; c.stroke();
      });
    }

    _marcaMes() {                                          // rótulo del mes actual del replay
      const s = this.s, c = this.ctx; if (s.tipo === "malla" || !this.etiqueta) return;
      let p = null, txt = this.etiqueta;
      if (s.tipo === "barras") { const k = Math.floor(this.corte); s.indice.forEach((f, j) => f.forEach((v, i) => { if (v === k && s.z[j][i]) p = [this.px(i), this.py(j), this.pz(s.z[j][i])]; if (v === k && s.z[j][i]) txt = this.etiqueta + " · S/ " + FC.num(s.z[j][i], 2) + " M"; })); }
      else { const x = this.px(Math.min(this.corte, s.ejeX.valores.length - 1)); p = [x, -AY * (this.ojo[1] > 0 ? -1 : 1), 0]; }
      if (!p) return;
      const a = this.proyectar(p), b = [a[0], Math.max(52, a[1] - (s.tipo === "barras" ? 34 : 0))];
      if (s.tipo === "cintas") { const l = this.proyectar([p[0], AY, 0]), m = this.proyectar([p[0], -AY, 0]); c.setLineDash([4, 4]); c.strokeStyle = "rgba(251,191,36,.8)"; c.lineWidth = 1.3; c.beginPath(); c.moveTo(l[0], l[1]); c.lineTo(m[0], m[1]); c.stroke(); c.setLineDash([]); b[1] += 34; }
      else { c.strokeStyle = "rgba(251,191,36,.9)"; c.lineWidth = 1.3; c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke(); }
      c.font = "700 11.5px " + FC.MONO; const w = c.measureText(txt).width + 16; FC.caja(c, b[0] - w / 2, b[1] - 20, w, 20, 5); c.fillStyle = "rgba(251,191,36,.95)"; c.fill();
      c.fillStyle = "#1A1203"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(txt, b[0], b[1] - 9.5);
    }

    _colores() {                                           // barra de color a la derecha
      if (this.w < 560) return;
      const c = this.ctx, x = this.w - 26, y0 = 46, h = this.h - 120, s = this.s;
      const gr = c.createLinearGradient(0, y0 + h, 0, y0); for (let k = 0; k <= 6; k++) gr.addColorStop(k / 6, FC.color(k / 6));
      FC.caja(c, x, y0, 9, h, 4); c.fillStyle = gr; c.fill();
      c.font = "500 10.5px " + FC.MONO; c.fillStyle = FC.C.tinta2; c.textAlign = "right"; c.textBaseline = "middle";
      const base = s.tipo === "malla" ? this.min : 0;
      s.ejeZ.marcas.forEach(([v, t]) => { const k = (v - base) / (this.max - base); if (k >= -0.02 && k <= 1.01) c.fillText(t, x - 5, y0 + h * (1 - Math.max(0, k))); });
      if (this.cursor) { const y = y0 + h * (1 - this.norm(this.cursor.v)); c.fillStyle = "#fff"; c.beginPath(); c.moveTo(x + 10, y); c.lineTo(x + 17, y - 5); c.lineTo(x + 17, y + 5); c.fill(); }
    }

    _lectura() {
      const p = this.cursor; if (!p) return;
      const c = this.ctx, q = this.proyectar(p.p), f = this.proyectar([p.p[0], p.p[1], 0]), s = this.s;
      c.setLineDash([3, 4]); c.strokeStyle = "rgba(232,238,252,.6)"; c.lineWidth = 1; c.beginPath(); c.moveTo(q[0], q[1]); c.lineTo(f[0], f[1]); c.stroke(); c.setLineDash([]);
      c.beginPath(); c.arc(q[0], q[1], 5, 0, 7); c.fillStyle = "#fff"; c.fill(); c.strokeStyle = FC.C.azul; c.lineWidth = 2; c.stroke();
      let L;
      if (s.tipo === "malla") L = [["TEA " + FC.num(s.ejeX.valores[p.i], 2) + " % · " + s.ejeY.valores[p.j] + " meses"], ["Por cada S/ 100 pagas S/ " + FC.num(p.v, 2) + " de interés", FC.C.oro], ["cálculo, no es una tasa del FPF", FC.C.tinta3]];
      else if (s.tipo === "cintas") L = [[s.ejeY.marcas[p.j][1]], [this.mesTexto(s.meses[p.i]) + " · TEA " + FC.num(p.v, 2) + " %", FC.C.oro], ["observado · BCRP", FC.C.verde]];
      else L = [[this.mesTexto(s.ejeY.marcas[p.j][1] + "-" + String(p.i + 1).padStart(2, "0"))], ["S/ " + FC.num(p.v, 2) + " M financiados", FC.C.oro], ["observado · SMV (cota inferior)", FC.C.verde]];
      FC.globo(c, q[0], q[1], L, this.w, this.h);
    }

    // ------------------------------------------------------------------ interacción
    _buscar(mx, my) {
      let m = null, d0 = 20 * 20;
      for (const p of this.puntos || []) {
        if (this.s.tipo === "barras" && this.s.indice[p.j][p.i] > this.corte) continue;
        if (this.s.tipo === "cintas" && p.i > this.corte) continue;
        const q = this.proyectar(p.p), d = (q[0] - mx) ** 2 + (q[1] - my) ** 2 + q[2] * 14;
        if (d < d0) { d0 = d; m = p; }
      }
      return m;
    }
    _eventos() {
      const e = this.capa, pos = (v) => { const b = e.getBoundingClientRect(); return [v.clientX - b.left, v.clientY - b.top]; };
      e.addEventListener("pointerdown", (v) => { this.agarre = [...pos(v), this.yaw, this.pitch]; e.classList.add("gira"); e.setPointerCapture(v.pointerId); });
      e.addEventListener("pointermove", (v) => {
        const [x, y] = pos(v);
        if (this.agarre) { this.yaw = Math.max(-1.35, Math.min(1.35, this.agarre[2] - (x - this.agarre[0]) * 0.007)); this.pitch = Math.max(0.12, Math.min(1.35, this.agarre[3] + (y - this.agarre[1]) * 0.006)); this.cursor = null; }
        else if (this.M) this.cursor = this._buscar(x, y);
      });
      const suelta = () => { this.agarre = null; e.classList.remove("gira"); };
      e.addEventListener("pointerup", suelta); e.addEventListener("pointercancel", suelta);
      e.addEventListener("pointerleave", () => { this.cursor = null; });
      e.addEventListener("dblclick", () => { this.yaw = this.yaw0; this.pitch = this.pitch0; this.zoom = 1; });
    }
    acercar(k) { this.zoom = Math.max(0.7, Math.min(1.9, this.zoom * k)); }
  }
  FC.Superficie = Superficie;
})();
