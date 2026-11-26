// Portal de entrega · FinCrowd Perú (Diego Sebastián Aliaga Damián, 2024200481M)
// Lee window.PORTAL (datos.js, generado por herramientas/portal/generar_portal.py) y arma las partes dinámicas.
(function () {
  "use strict";
  const P = window.PORTAL;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const el = (tag, attrs = {}, html = "") => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined || v === false) continue;
      if (k === "class") e.className = v; else e.setAttribute(k, v === true ? "" : v);
    }
    if (html) e.innerHTML = html;
    return e;
  };
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const icono = (id, extra = "") => `<svg class="ic ${extra}"><use href="#${id}"/></svg>`;
  const NBSP = " ";
  const mbTexto = (b) => b >= 1e6 ? `${(b / 1e6).toFixed(1)} MB` : b >= 1e3 ? `${Math.round(b / 1e3)} KB` : `${b} B`;
  if (!P) return;
  document.documentElement.classList.add("js");   // las animaciones de aparición solo se activan si el script corre

  // ------------------------------------------------------------------- valores simples
  const valor = (k) => (k in P.cifras ? P.cifras[k] : k in P.verificacion ? String(P.verificacion[k]) : "");
  $$("[data-cifra]").forEach((e) => { e.textContent = valor(e.dataset.cifra) + (e.dataset.sufijo || ""); });
  $$("[data-paginas]").forEach((e) => { e.textContent = P.paginas[e.dataset.paginas]; });
  $$("[data-hash]").forEach((e) => { e.textContent = P.verificacion[e.dataset.hash]; e.title = P.verificacion[e.dataset.hash]; });
  $$("[data-zip]").forEach((e) => { if (P.zip) e.textContent = e.dataset.zip === "mb" ? `${P.zip.mb} MB` : P.zip.nombre; });
  $$("[data-enlace]").forEach((e) => { e.href = P[e.dataset.enlace]; });
  $$("[data-enlace-texto]").forEach((e) => { e.textContent = P[e.dataset.enlaceTexto]; });
  $$("[data-git]").forEach((e) => { e.href = `${P.repositorio}/${e.dataset.git}`; e.target = "_blank"; e.rel = "noopener"; });
  $$("[data-descarga]").forEach((e) => {
    const d = P.descargas[e.dataset.descarga];
    if (!d) return;
    e.href = d.url; e.setAttribute("download", d.nombre);
    e.insertAdjacentHTML("beforeend", ` <small>${d.mb} MB</small>`);
  });

  // ------------------------------------------------------------------- contadores
  const formatear = (n, dec) => {
    const [ent, frac] = n.toFixed(dec).split(".");
    return ent.replace(/\B(?=(\d{3})+(?!\d))/g, NBSP) + (frac ? "." + frac : "");
  };
  const contar = (e) => {
    const texto = valor(e.dataset.cifra);
    const objetivo = parseFloat(texto.replace(/[\s  ]/g, ""));
    if (!isFinite(objetivo) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const dec = (texto.split(".")[1] || "").length, t0 = performance.now(), dur = 1400;
    const paso = (t) => {
      const x = Math.min(1, (t - t0) / dur), f = 1 - Math.pow(1 - x, 3);
      e.textContent = x < 1 ? formatear(objetivo * f, dec) : texto;
      if (x < 1) requestAnimationFrame(paso);
    };
    requestAnimationFrame(paso);
  };

  // ------------------------------------------------------------------- aparición y menú
  const reveladores = $$(".revelar");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entradas) => entradas.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("visto");
      $$(".contador", en.target).forEach(contar);
      io.unobserve(en.target);
    }), { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveladores.forEach((r) => io.observe(r));
    const enlaces = $$(".menu a");
    const espia = new IntersectionObserver((entradas) => entradas.forEach((en) => {
      if (en.isIntersecting) enlaces.forEach((a) => a.classList.toggle("activo", a.getAttribute("href") === "#" + en.target.id));
    }), { rootMargin: "-45% 0px -50% 0px" });
    $$("main section[id]").forEach((s) => espia.observe(s));
  } else reveladores.forEach((r) => r.classList.add("visto"));
  const barra = $("#barra");
  addEventListener("scroll", () => barra.classList.toggle("con-borde", scrollY > 10), { passive: true });

  // ------------------------------------------------------------------- tema claro / oscuro
  $("#tema").addEventListener("click", () => {
    const raiz = document.documentElement;
    const actual = raiz.dataset.theme || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    const nuevo = actual === "light" ? "dark" : "light";
    raiz.dataset.theme = nuevo;
    try { localStorage.setItem("portal-tema", nuevo); } catch (e) { /* sin almacenamiento: solo esta visita */ }
  });

  // ------------------------------------------------------------------- avisos y copiar
  const aviso = $("#aviso");
  let tAviso;
  const avisar = (t) => { aviso.textContent = t; aviso.classList.add("ver"); clearTimeout(tAviso); tAviso = setTimeout(() => aviso.classList.remove("ver"), 1800); };
  const copiar = async (texto) => {
    try { await navigator.clipboard.writeText(texto); }
    catch (e) {
      const t = el("textarea"); t.value = texto; document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); } catch (e2) { /* sin portapapeles */ }
      t.remove();
    }
    avisar("Copiado");
  };
  $$("[data-copiar]").forEach((b) => b.addEventListener("click", () => {
    const k = b.dataset.copiar;
    copiar(k === "comandos" ? $("#comandos").innerText.trim() : P.verificacion[k]);
    b.innerHTML = icono("i-check"); setTimeout(() => { b.innerHTML = icono("i-copy"); }, 1600);
  }));

  // ------------------------------------------------------------------- explorador de la entrega
  const TIPOS = { pdf: ["i-doc", "t-pdf"], csv: ["i-db", "t-csv"], json: ["i-db", "t-csv"], py: ["i-code", "t-py"],
    tex: ["i-doc", "t-tex"], typ: ["i-doc", "t-tex"], bib: ["i-doc", "t-tex"], sty: ["i-doc", "t-tex"], zip: ["i-zip", "t-zip"],
    png: ["i-img", "t-otro"], webp: ["i-img", "t-otro"], svg: ["i-img", "t-otro"] };
  const tipo = (n) => TIPOS[(n.split(".").pop() || "").toLowerCase()] || ["i-doc", "t-otro"];
  const arbol = $("#arbol");
  const nodos = new Map();
  const pintarNodo = (n, padre, ruta) => {
    const esCarpeta = Array.isArray(n.h);
    const caja = el("div", { class: "nodo", role: "treeitem", "aria-expanded": esCarpeta ? "false" : null });
    const [ic, cl] = esCarpeta ? ["i-folder", "t-carpeta"] : tipo(n.n);
    const meta = esCarpeta ? `${n.c} archivo${n.c === 1 ? "" : "s"} · ${mbTexto(n.s)}` : mbTexto(n.s);
    const fila = el("div", { class: "nodo-fila" + (esCarpeta ? " es-carpeta" : ""), tabindex: esCarpeta ? "0" : null },
      (esCarpeta ? icono("i-chev", "chev") : '<span class="vacio"></span>') + icono(ic, "tipo " + cl) +
      `<span class="nodo-nombre">${esc(n.n)}</span><span class="nodo-meta">${meta}</span>`);
    caja.appendChild(fila);
    const r = ruta ? ruta + "/" + n.n : n.n;
    nodos.set(caja, { n, r });
    if (esCarpeta) {
      const hijos = el("div", { class: "nodo-hijos", role: "group" });
      n.h.forEach((h) => pintarNodo(h, hijos, r));
      caja.appendChild(hijos);
      const alternar = () => { caja.classList.toggle("abierto"); caja.setAttribute("aria-expanded", caja.classList.contains("abierto")); };
      fila.addEventListener("click", alternar);
      fila.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); alternar(); } });
    }
    padre.appendChild(caja);
    return caja;
  };
  if (P.entrega) {
    const raiz = pintarNodo(P.entrega, arbol, "");
    raiz.classList.add("abierto");
    // resumen de las tres carpetas
    P.entrega.h.forEach((h) => {
      const m = /^(N\d)_/.exec(h.n);
      if (!m) return;
      const r = $(`[data-resumen="${m[1]}"]`);
      if (r) r.innerHTML = `<span>${h.c} archivos</span><span>${mbTexto(h.s)}</span>`;
    });
    $$("[data-abrir]").forEach((c) => c.addEventListener("click", () => {
      const clave = c.dataset.abrir;
      $$(".nodo", arbol).forEach((nd) => {
        const d = nodos.get(nd);
        if (d && d.n.n.startsWith(clave + "_")) { nd.classList.add("abierto"); nd.setAttribute("aria-expanded", "true"); }
      });
      $("#explorador").scrollIntoView({ behavior: "smooth", block: "start" });
    }));
  } else {
    arbol.innerHTML = '<p class="sin-resultados">La estructura de la entrega se muestra al generar el portal con la carpeta local.</p>';
  }
  const buscarArchivo = $("#buscar-archivo");
  buscarArchivo.addEventListener("input", () => {
    const q = buscarArchivo.value.trim().toLowerCase();
    const todos = $$(".nodo", arbol);
    if (!q) {
      todos.forEach((nd) => { nd.classList.remove("oculto"); $(".nodo-nombre", nd).innerHTML = esc(nodos.get(nd).n.n); });
      return;
    }
    // de abajo hacia arriba: una carpeta se muestra si ella o algún descendiente coincide
    todos.slice().reverse().forEach((nd) => {
      const d = nodos.get(nd), nombre = d.n.n, i = nombre.toLowerCase().indexOf(q);
      const hijoVisible = $$(":scope > .nodo-hijos > .nodo", nd).some((h) => !h.classList.contains("oculto"));
      const coincide = i >= 0;
      nd.classList.toggle("oculto", !(coincide || hijoVisible));
      if (hijoVisible) { nd.classList.add("abierto"); nd.setAttribute("aria-expanded", "true"); }
      $(".nodo-nombre", nd).innerHTML = coincide
        ? esc(nombre.slice(0, i)) + "<mark>" + esc(nombre.slice(i, i + q.length)) + "</mark>" + esc(nombre.slice(i + q.length))
        : esc(nombre);
    });
  });

  // ------------------------------------------------------------------- visor (galería a pantalla completa)
  const visor = $("#visor"), vImg = $("#visor-img"), vFig = $(".visor-figura"), vTiras = $("#visor-tiras");
  let galeria = [], indice = 0, focoPrevio = null;
  const mostrar = (i) => {
    indice = (i + galeria.length) % galeria.length;
    const it = galeria[indice];
    vFig.classList.remove("ampliado");
    vImg.src = it.src; vImg.alt = it.alt || it.titulo || "";
    $("#visor-titulo").textContent = it.titulo || "";
    $("#visor-pie").innerHTML = it.pie || "";
    $("#visor-cuenta").textContent = galeria.length > 1 ? `${indice + 1} / ${galeria.length}` : "";
    $("#visor-acciones").innerHTML = (it.acciones || []).map((a) =>
      `<a class="boton ${a.principal ? "boton-principal" : "boton-secundario"}" href="${esc(a.href)}" ${a.descargar ? `download="${esc(a.descargar)}"` : 'target="_blank" rel="noopener"'}>${icono(a.icono)}<span>${esc(a.texto)}</span></a>`).join("");
    $$("button", vTiras).forEach((b, k) => b.classList.toggle("activo", k === indice));
    const activa = $$("button", vTiras)[indice];
    if (activa) activa.scrollIntoView({ block: "nearest", inline: "center" });
    $("#visor-ant").hidden = $("#visor-sig").hidden = galeria.length < 2;
    if (galeria[indice + 1]) new Image().src = galeria[indice + 1].src;   // precarga la siguiente
  };
  const abrir = (items, i = 0) => {
    galeria = items; focoPrevio = document.activeElement;
    vTiras.innerHTML = items.length > 1 ? items.map((it, k) => `<button type="button" aria-label="Ir a ${k + 1}"><img src="${esc(it.mini || it.src)}" alt="" loading="lazy"></button>`).join("") : "";
    $$("button", vTiras).forEach((b, k) => b.addEventListener("click", () => mostrar(k)));
    vTiras.hidden = items.length < 2;
    visor.hidden = false; document.body.style.overflow = "hidden";
    mostrar(i);
    $("#visor-cerrar").focus();
  };
  const cerrar = () => { visor.hidden = true; document.body.style.overflow = ""; vImg.removeAttribute("src"); if (focoPrevio) focoPrevio.focus(); };
  $("#visor-cerrar").addEventListener("click", cerrar);
  $("#visor-ant").addEventListener("click", () => mostrar(indice - 1));
  $("#visor-sig").addEventListener("click", () => mostrar(indice + 1));
  vImg.addEventListener("click", () => vFig.classList.toggle("ampliado"));
  visor.addEventListener("click", (ev) => { if (ev.target === visor || ev.target.classList.contains("visor-cuerpo")) cerrar(); });
  addEventListener("keydown", (ev) => {
    if (visor.hidden) return;
    if (ev.key === "Escape") cerrar();
    else if (ev.key === "ArrowRight") mostrar(indice + 1);
    else if (ev.key === "ArrowLeft") mostrar(indice - 1);
  });
  let x0 = null;
  visor.addEventListener("touchstart", (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
  visor.addEventListener("touchend", (ev) => {
    if (x0 === null || vFig.classList.contains("ampliado")) return;
    const dx = ev.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) mostrar(indice + (dx < 0 ? 1 : -1));
  });

  const pdf = (stem, texto, principal = true) => {
    const d = P.descargas[stem];
    return { texto: `${texto} (${d.mb} MB)`, href: d.url, descargar: d.nombre, icono: "i-down", principal };
  };
  const paginasDe = (carpeta, prefijo, n, titulo, acciones) => Array.from({ length: n }, (_, k) => {
    const src = `img/${carpeta}/${prefijo}${String(k + 1).padStart(2, "0")}.webp`;
    return { src, titulo, alt: `${titulo}, página ${k + 1}`, acciones };
  });
  $$("[data-hojear]").forEach((b) => b.addEventListener("click", () => {
    if (b.dataset.hojear === "typst") {
      abrir([{ src: "img/typst/p01.webp", titulo: "Artículo · versión Typst", pie: "Portada de la versión compilada con Typst: mismo diseño, mismas cifras y referencias.",
        acciones: [pdf("Aliaga_Damian_articulo_FPF_Peru_typst", "PDF")] }]);
    } else {
      abrir(paginasDe("articulo", "p", P.paginas.articulo, "Artículo · versión LaTeX", [pdf("Aliaga_Damian_articulo_FPF_Peru", "PDF")]));
    }
  }));
  $$("[data-ampliar]").forEach((b) => b.addEventListener("click", () => abrir([{
    src: "img/poster_articulo.webp", mini: "img/poster_articulo_m.webp", titulo: "Póster del artículo · A0",
    pie: "Toca la imagen para ampliarla y desplázate para leerla.", acciones: [pdf("Aliaga_Damian_poster_articulo", "PDF")],
  }])));

  // ------------------------------------------------------------------- carrusel del Beamer
  const carrusel = $("#carrusel-beamer");
  const diapos = paginasDe("beamer", "d", P.paginas.beamer, "Beamer", [pdf("Aliaga_Damian_beamer", "Proyectar"), pdf("Aliaga_Damian_beamer_para_imprimir", "Imprimir", false)]);
  diapos.forEach((d, k) => {
    const b = el("button", { type: "button", "aria-label": `Ver la diapositiva ${k + 1}` }, `<img src="${d.src}" alt="Diapositiva ${k + 1}" loading="lazy">`);
    b.addEventListener("click", () => abrir(diapos, k));
    carrusel.appendChild(b);
  });
  const cuenta = $("#cuenta-beamer");
  const actual = () => Math.round(carrusel.scrollLeft / (carrusel.clientWidth + 14));
  carrusel.addEventListener("scroll", () => { cuenta.textContent = `${actual() + 1} / ${diapos.length}`; }, { passive: true });
  $$("[data-carrusel]").forEach((b) => b.addEventListener("click", () => {
    const i = Math.max(0, Math.min(diapos.length - 1, actual() + Number(b.dataset.carrusel)));
    carrusel.scrollTo({ left: i * (carrusel.clientWidth + 14), behavior: "smooth" });
  }));

  // ------------------------------------------------------------------- minigráfico del monto mensual
  (() => {
    const caja = $("#minigrafico"), s = P.serie;
    if (!s || !s.length) return;
    const W = 600, H = 190, top = 58, bottom = 26, max = Math.max(...s.map((d) => d.m)) * 1.08;
    const x = (i) => (i / (s.length - 1)) * W, y = (v) => H - bottom - (v / max) * (H - top - bottom);
    const linea = s.map((d, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(d.m).toFixed(1)}`).join("");
    const area = `${linea}L${W},${H - bottom}L0,${H - bottom}Z`;
    const anios = s.map((d, i) => ({ d, i })).filter(({ d }) => d.p.endsWith("-01"));
    caja.innerHTML = `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="Monto financiado mensual, de ${s[0].p} a ${s[s.length - 1].p}">
      <defs><linearGradient id="relleno" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--azul)" stop-opacity=".42"/><stop offset="1" stop-color="var(--azul)" stop-opacity="0"/></linearGradient>
      <linearGradient id="trazo" x1="0" x2="1"><stop offset="0" stop-color="var(--azul)"/><stop offset="1" stop-color="var(--violeta)"/></linearGradient></defs>
      ${anios.map(({ i }) => `<line x1="${x(i)}" x2="${x(i)}" y1="${top - 10}" y2="${H - bottom}" stroke="var(--borde)" stroke-dasharray="3 4" vector-effect="non-scaling-stroke"/>`).join("")}
      <path d="${area}" fill="url(#relleno)"/>
      <path d="${linea}" fill="none" stroke="url(#trazo)" stroke-width="2.4" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
    </svg>
    <p class="minigrafico-dato">Monto financiado por mes<b>S/ ${P.cifras.monto2025} M en 2025</b></p>
    ${anios.map(({ d, i }) => `<span class="eje-x" style="left:${(x(i) / W) * 100}%">${d.p.slice(0, 4)}</span>`).join("")}`;
  })();

  // ------------------------------------------------------------------- estado del arte
  const A = P.articulos;
  const revistas = new Set(A.map((a) => a.revista)).size;
  const q1 = A.filter((a) => a.cuartil === "Q1").length;
  const anios = A.map((a) => +a.anio);
  $("#arte-resumen").innerHTML = [
    `<b>${A.length}</b> artículos`, `<b>${revistas}</b> revistas`, `<b>${q1}</b> en Q1 · <b>${A.length - q1}</b> en Q2`,
    `<b>${Math.min(...anios)}–${Math.max(...anios)}</b>`].map((t) => `<span class="pastilla">${t}</span>`).join("");
  const itemPoster = (a) => ({
    src: a.img, mini: a.mini, titulo: `${a.n} · ${a.autores} (${a.anio})`,
    alt: `Póster del artículo ${a.n}: ${a.titulo_es}`,
    pie: `<b>${esc(a.titulo_es)}</b><br><i>${esc(a.titulo)}</i> · ${esc(a.revista)} · ${a.cuartil}`,
    acciones: [{ texto: "PDF del póster", href: a.poster, icono: "i-down", descargar: a.poster.split("/").pop(), principal: true },
      { texto: "Artículo (DOI)", href: `https://doi.org/${a.doi}`, icono: "i-out" }],
  });
  const rejilla = $("#galeria");
  A.forEach((a, k) => {
    const b = el("button", { class: "tarjeta-poster", type: "button", "data-k": k, "aria-label": `Ver el póster ${a.n}: ${a.titulo_es}` },
      `<span class="miniatura"><img src="${a.mini}" alt="" loading="lazy"><span class="insignia-n">${a.n}</span><span class="insignia-q ${a.cuartil.toLowerCase()}">${a.cuartil}</span></span>
       <span class="cuerpo"><span class="ref">${esc(a.autores)} (${a.anio})</span><span class="tit">${esc(a.titulo_es)}</span><span class="rev">${esc(a.revista)}</span></span>`);
    b.addEventListener("click", () => abrir(visibles().map(itemPoster), visibles().indexOf(a)));
    rejilla.appendChild(b);
  });
  $("#tabla-articulos").innerHTML = `<table><thead><tr><th>N.º</th><th>Referencia</th><th>Revista</th><th>Cuartil</th><th>En la entrega</th><th>DOI</th></tr></thead><tbody>${
    A.map((a, k) => `<tr data-k="${k}"><td>${a.n}</td><td><b>${esc(a.autores)} (${a.anio})</b><span class="tit-en">${esc(a.titulo)}</span></td>
      <td>${esc(a.revista)}</td><td><span class="q ${a.cuartil.toLowerCase()}">${a.cuartil}</span></td>
      <td>${a.version ? esc(a.version) + (a.paginas ? ` · ${a.paginas} págs.` : "") : "—"}</td>
      <td><a href="https://doi.org/${esc(a.doi)}" target="_blank" rel="noopener">${esc(a.doi)}</a></td></tr>`).join("")}</tbody></table>`;
  const buscarArt = $("#buscar-articulo");
  const coincide = (a, q) => !q || [a.autores, a.titulo, a.titulo_es, a.revista, a.anio, a.ambito, a.enfoque, a.n].join(" ").toLowerCase().includes(q);
  const visibles = () => A.filter((a) => coincide(a, buscarArt.value.trim().toLowerCase()));
  buscarArt.addEventListener("input", () => {
    const q = buscarArt.value.trim().toLowerCase();
    $$("[data-k]").forEach((e) => e.classList.toggle("oculto", !coincide(A[+e.dataset.k], q)));
    $("#sin-resultados").classList.toggle("oculto", visibles().length > 0);
  });
  $$("[data-vista]").forEach((b) => b.addEventListener("click", () => {
    $$("[data-vista]").forEach((x) => x.classList.toggle("activo", x === b));
    const tabla = b.dataset.vista === "tabla";
    $("#galeria").classList.toggle("oculto", tabla);
    $("#tabla-articulos").classList.toggle("oculto", !tabla);
  }));

  // ------------------------------------------------------------------- scripts
  $("#scripts").innerHTML = P.scripts.map((s) =>
    `<a class="script revelar visto" href="${P.repositorio}/blob/main/${s.ruta}" target="_blank" rel="noopener">
      <code>${esc(s.ruta.split("/").pop())}</code><b>${esc(s.titulo)}</b><p>${esc(s.texto)}</p>
      <small><span>${formatear(s.lineas, 0)} líneas</span><span>Ver en GitHub ${icono("i-out")}</span></small></a>`).join("");
})();
