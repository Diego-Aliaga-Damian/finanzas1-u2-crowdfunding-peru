// Portal de entrega, versión amigable (Diego Sebastián Aliaga Damián, 2024200481M).
// Escritorio con los productos y recorrido guiado; todo sale de window.PORTAL (datos.js).
(function () {
  "use strict";
  const P = window.PORTAL;
  if (!P) return;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const C = P.cifras, V = P.verificacion;
  const valor = (k) => (k in C ? C[k] : k in V ? String(V[k]) : "");

  // ------------------------------------------------------------------- valores, descargas y tema
  $$("[data-cifra]").forEach((e) => { e.textContent = valor(e.dataset.cifra); });
  const descarga = (stem) => P.descargas[stem];
  $$("[data-descarga]").forEach((e) => {
    const d = descarga(e.dataset.descarga);
    e.href = d.url; e.setAttribute("download", d.nombre);
    e.insertAdjacentHTML("beforeend", ` <small>${d.mb} MB</small>`);
  });
  $("#tema").addEventListener("click", () => {
    const raiz = document.documentElement;
    const actual = raiz.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    raiz.dataset.theme = actual === "dark" ? "light" : "dark";
    try { localStorage.setItem("escritorio-tema", raiz.dataset.theme); } catch (e) { /* solo esta visita */ }
  });
  const aviso = $("#aviso");
  let tAviso;
  const avisar = (t) => { aviso.textContent = t; aviso.classList.add("ver"); clearTimeout(tAviso); tAviso = setTimeout(() => aviso.classList.remove("ver"), 1800); };

  // ------------------------------------------------------------------- gráfico del monto mensual
  const grafico = ({ ancho = 600, alto = 220, ejes = true, nota = true } = {}) => {
    const s = P.serie, arriba = nota ? 46 : 30, abajo = ejes ? 24 : 8, max = Math.max(...s.map((d) => d.m)) * 1.06;
    const x = (i) => 8 + (i / (s.length - 1)) * (ancho - 16), y = (v) => alto - abajo - (v / max) * (alto - arriba - abajo);
    const linea = s.map((d, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(d.m).toFixed(1)}`).join("");
    const area = `${linea}L${x(s.length - 1)},${alto - abajo}L${x(0)},${alto - abajo}Z`;
    const anios = s.map((d, i) => ({ d, i })).filter(({ d }) => d.p.endsWith("-01"));
    const reforma = s.findIndex((d) => d.p === "2025-12");
    return `<svg viewBox="0 0 ${ancho} ${alto}" role="img" aria-label="Monto financiado por mes, de ${s[0].p} a ${s[s.length - 1].p}, en millones de soles">
      <defs><linearGradient id="g-area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b8cff" stop-opacity=".45"/><stop offset="1" stop-color="#5b8cff" stop-opacity="0"/></linearGradient></defs>
      ${ejes ? anios.map(({ d, i }) => `<line x1="${x(i)}" x2="${x(i)}" y1="${arriba - 8}" y2="${alto - abajo}" stroke="currentColor" stroke-opacity=".12" stroke-dasharray="3 4"/><text class="eje" x="${x(i)}" y="${alto - 6}" text-anchor="middle">${d.p.slice(0, 4)}</text>`).join("") : ""}
      ${reforma > 0 && ejes ? `<line x1="${x(reforma)}" x2="${x(reforma)}" y1="${arriba - 14}" y2="${alto - abajo}" stroke="#e8664a" stroke-width="2"/><text class="etq" x="${x(reforma) - 6}" y="${arriba - 18}" text-anchor="end">Cambio de la norma</text>` : ""}
      <path d="${area}" fill="url(#g-area)"/>
      <path d="${linea}" fill="none" stroke="#5b8cff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>`;
  };
  $("#laptop-grafico").innerHTML = grafico({ ancho: 300, alto: 160, ejes: false, nota: true }) +
    `<span class="cifra-pantalla">S/ ${C.monto2025} M<small>financiados en 2025</small></span>`;

  // ------------------------------------------------------------------- ficha (ventana)
  const ficha = $("#ficha"), fVisual = $("#ficha-visual");
  let lista = [], pos = 0, focoPrevio = null, actual = null;
  const boton = (b) => b.href
    ? `<a class="boton ${b.principal ? "boton-principal" : "boton-suave"}" href="${esc(b.href)}" ${b.descargar ? `download="${esc(b.descargar)}"` : 'target="_blank" rel="noopener"'}>${esc(b.texto)}${b.mb ? ` <small>${b.mb} MB</small>` : ""}</a>`
    : `<button class="boton ${b.principal ? "boton-principal" : "boton-suave"}" type="button" data-ir="${esc(b.ir)}">${esc(b.texto)}</button>`;
  const pdf = (stem, texto, principal = true) => { const d = descarga(stem); return { texto, href: d.url, descargar: d.nombre, mb: d.mb, principal }; };
  const pintarLamina = () => {
    const it = lista[pos];
    fVisual.innerHTML = `<img class="lamina" src="${esc(it.src)}" alt="${esc(it.alt || "")}">` + (lista.length > 1
      ? `<div class="ficha-pasos"><button class="redondo" type="button" data-mover="-1" aria-label="Anterior">←</button><span>${pos + 1} de ${lista.length}</span><button class="redondo" type="button" data-mover="1" aria-label="Siguiente">→</button></div>` : "");
    if (it.titulo) $("#ficha-titulo").textContent = it.titulo;
    if (it.cuerpo) $("#ficha-cuerpo").innerHTML = it.cuerpo;
    if (it.botones) $("#ficha-botones").innerHTML = it.botones.map(boton).join("");
    if (lista[pos + 1]) new Image().src = lista[pos + 1].src;
  };
  const mover = (d) => { if (lista.length > 1) { pos = (pos + d + lista.length) % lista.length; pintarLamina(); } };
  const abrir = (clave) => {
    const f = FICHAS[clave]();
    actual = clave; focoPrevio = document.activeElement;
    $("#ficha-cejilla").textContent = f.cejilla;
    $("#ficha-titulo").textContent = f.titulo;
    $("#ficha-cuerpo").innerHTML = f.cuerpo;
    $("#ficha-botones").innerHTML = (f.botones || []).map(boton).join("");
    lista = f.laminas || []; pos = 0;
    if (lista.length) pintarLamina(); else fVisual.innerHTML = f.visual || "";
    ficha.hidden = false; document.body.style.overflow = "hidden";
    $("#ficha-cerrar").focus();
  };
  const cerrar = () => { ficha.hidden = true; document.body.style.overflow = ""; fVisual.innerHTML = ""; actual = null; if (focoPrevio) focoPrevio.focus(); };
  $("#ficha-cerrar").addEventListener("click", cerrar);
  ficha.addEventListener("click", (ev) => {
    if (ev.target === ficha) return cerrar();
    const m = ev.target.closest("[data-mover]"); if (m) return mover(+m.dataset.mover);
    const ir = ev.target.closest("[data-ir]"); if (ir) { cerrar(); abrir(ir.dataset.ir); }
  });
  addEventListener("keydown", (ev) => {
    if (ficha.hidden) return;
    if (ev.key === "Escape") cerrar();
    else if (ev.key === "ArrowRight") mover(1);
    else if (ev.key === "ArrowLeft") mover(-1);
  });
  let x0 = null;
  fVisual.addEventListener("touchstart", (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
  fVisual.addEventListener("touchend", (ev) => { if (x0 === null) return; const dx = ev.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) mover(dx < 0 ? 1 : -1); });

  const paginas = (carpeta, pref, n, nombre) => Array.from({ length: n }, (_, k) => ({ src: `img/${carpeta}/${pref}${String(k + 1).padStart(2, "0")}.webp`, alt: `${nombre}, página ${k + 1}` }));
  const FICHAS = {
    articulo: () => ({
      cejilla: "Mi artículo", titulo: "Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026",
      cuerpo: `<p>Tiene formato de revista a dos columnas, con normas APA 7 y ${P.paginas.articulo} páginas. Incluye el resumen en español e inglés, los antecedentes, el método, los resultados con pruebas econométricas, la discusión y las conclusiones.</p><p>Usa las flechas para hojearlo.</p>`,
      laminas: paginas("articulo", "p", P.paginas.articulo, "Artículo"),
      botones: [pdf("Aliaga_Damian_articulo_FPF_Peru", "PDF (LaTeX)"), pdf("Aliaga_Damian_articulo_FPF_Peru_typst", "PDF (Typst)", false)],
    }),
    beamer: () => ({
      cejilla: "Beamer", titulo: "Diez diapositivas para la exposición",
      cuerpo: "<p>Del problema a las conclusiones, con una demostración en vivo de cómo se extraen los datos de la SMV en tres minutos. Hay una versión para proyectar y otra para imprimir una copia por compañero.</p>",
      laminas: paginas("beamer", "d", P.paginas.beamer, "Diapositiva"),
      botones: [pdf("Aliaga_Damian_beamer", "Para proyectar"), pdf("Aliaga_Damian_beamer_para_imprimir", "Para imprimir", false)],
    }),
    poster: () => ({
      cejilla: "Póster A0", titulo: "El artículo en una sola lámina",
      cuerpo: "<p>Muestra el contexto, el problema, el objetivo, la metodología, los resultados, las conclusiones y un código QR que lleva al repositorio.</p>",
      laminas: [{ src: "img/poster_articulo.webp", alt: "Póster del artículo en tamaño A0" }],
      botones: [pdf("Aliaga_Damian_poster_articulo", "Descargar el PDF")],
    }),
    posteres: () => ({
      cejilla: "Estado del arte", titulo: "20 pósteres, uno por cada artículo",
      cuerpo: "",
      laminas: P.articulos.map((a) => ({
        src: a.img, alt: `Póster ${a.n}: ${a.titulo_es}`, titulo: `${a.n}. ${a.titulo_es}`,
        cuerpo: `<p><b>${esc(a.autores)} (${a.anio})</b> · <i>${esc(a.revista)}</i> · ${a.cuartil}</p><p>${esc(a.titulo)}</p>`,
        botones: [{ texto: "PDF del póster", href: a.poster, descargar: a.poster.split("/").pop(), principal: true },
          { texto: "Ver el artículo original", href: `https://doi.org/${a.doi}` }],
      })),
    }),
    datos: () => ({
      cejilla: "Datos y código", titulo: "Todo se puede repetir desde cero",
      cuerpo: `<p>La base tiene <b>${C.filasPanel}</b> observaciones y <b>${C.columnasPanel}</b> variables, de ${C.fechaInicio} a ${C.fechaCorte}. Los ${V.crudos} archivos originales se guardaron sin editar.</p>
        <div class="lista-enlaces">
          ${["datos_procesados_2024200481M", "datos_procesados_2024200481M_empresas"].map((k, i) => { const d = descarga(k); return `<a href="${d.url}" download="${d.nombre}"><span class="em ${i ? "em-violeta" : "em-verde"}">⬇</span><span>${i ? "Base de empresas supervisadas" : "Base procesada"} (CSV)<small>${d.mb} MB · huella SHA-256 abajo</small></span></a>`; }).join("")}
          <a href="${P.repositorio}/tree/main/codigo" target="_blank" rel="noopener"><span class="em em-azul">&lt;/&gt;</span><span>Los scripts en Python<small>extracción, limpieza, análisis y auditoría</small></span></a>
          <a href="${P.repositorio}/tree/main/datos_crudos" target="_blank" rel="noopener"><span class="em em-ambar">🗂</span><span>Datos crudos<small>las respuestas originales de cada fuente</small></span></a>
          <a href="${P.repositorio}/blob/main/diccionario_variables.md" target="_blank" rel="noopener"><span class="em em-coral">📖</span><span>Diccionario de variables<small>qué significa cada columna</small></span></a>
          <button type="button" data-copiar="${V.sha_base}"><span class="em em-verde">🔐</span><span>Copiar la huella SHA-256 de la base<small class="huella">${V.sha_base}</small></span></button>
        </div>`,
      visual: `<div class="paso-visual" style="width:100%"><span class="objeto carpeta" style="position:relative;left:auto;top:auto;--r:-3deg"><span class="carpeta-pestana"></span><span class="carpeta-cuerpo"><b>Datos y código</b><small>${C.filasPanel} observaciones · ${V.crudos} archivos</small></span></span></div>`,
    }),
    dashboard: () => ({
      cejilla: "Dashboard", titulo: "Para explorar los datos por tu cuenta",
      cuerpo: "<p>Tiene doce páginas interactivas, con filtros por periodo y plataforma, un centro de mando en 3D, la comparación con el crédito tradicional y las pruebas econométricas. Si tarda en abrir, es porque se estaba “despertando”: espera unos segundos.</p>",
      visual: `<div class="grafico-paso" style="transform:none"><p class="grafico-titulo">Monto financiado cada mes (S/ millones)</p>${grafico()}</div>`,
      botones: [{ texto: "Abrir el dashboard", href: P.dashboard, principal: true }],
    }),
    guia: () => ({
      cejilla: "Guía del proyecto", titulo: "Todo explicado paso a paso",
      cuerpo: "<p>Explica de dónde salen los datos, qué hace cada programa, cómo se calculó cada resultado y cómo se comprobó. Está pensada para alguien que ve el proyecto por primera vez.</p>",
      visual: `<div class="paso-visual" style="width:100%"><span class="objeto cuaderno" style="position:relative;left:auto;top:auto;--r:4deg"><span class="espiral"></span><b>Guía del proyecto</b><small>paso a paso</small></span></div>`,
      botones: [pdf("Guia_completa_del_proyecto", "Descargar la guía")],
    }),
  };
  $$("[data-abrir]").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.abrir)));
  document.addEventListener("click", (ev) => {
    const c = ev.target.closest("[data-copiar]");
    if (!c) return;
    navigator.clipboard?.writeText(c.dataset.copiar).then(() => avisar("Huella copiada"), () => avisar("No se pudo copiar"));
  });

  // ------------------------------------------------------------------- recorrido guiado
  const li = (em, color, titulo, texto) => `<li><span class="em em-${color}" aria-hidden="true">${em}</span><div><b>${titulo}</b><span>${texto}</span></div></li>`;
  const PASOS = [
    { nombre: "La pregunta", titulo: "¿Por qué estudiar el crowdfunding?",
      texto: "El financiamiento participativo financiero (FPF) conecta, mediante una plataforma, a quienes necesitan dinero con personas que se lo prestan o invierten. En el Perú lo supervisa la SMV desde 2021.",
      lista: [li("💳", "coral", "El crédito tradicional es caro", `La tasa anual de los bancos a las pymes subió de ${C.teaBcosPyme2022} % en 2022 a ${C.teaBcosPyme2026} % en 2026.`),
        li("🔎", "azul", "Faltaban datos oficiales", "Solo circulaban cifras anuales sueltas en la prensa."),
        li("🎯", "verde", "Mi objetivo", "Describir la oferta de FPF de 2022 a 2026 y compararla con el crédito tradicional.")],
      boton: { texto: "Leer el artículo", ir: "articulo", principal: true },
      visual: () => `<div class="papel" style="width:min(62%,250px)"><img src="img/articulo/p01.webp" alt="Portada del artículo"></div><span class="nota nota-amarilla" style="--r:6deg;right:8%;top:10%">La pregunta<br>de todo</span>` },
    { nombre: "Los datos", titulo: "Busqué los datos en las fuentes oficiales",
      texto: "Nadie los copió a mano: unos programas en Python los descargaron, los revisaron y los ordenaron.",
      lista: [li("🏦", "azul", "BCRP y SMV por API", "10 series de tasas e inflación, y los estados financieros de las plataformas."),
        li("🕸️", "violeta", "Portal de la SMV, por scraping", `Proyectos y montos de ${C.plataformasAutorizadas} plataformas, mes a mes: ${C.solicitudesHTTP} consultas.`),
        li("📊", "verde", "Una base lista para analizar", `${C.filasPanel} observaciones y ${C.columnasPanel} variables, de ${C.fechaInicio} a ${C.fechaCorte}.`)],
      boton: { texto: "Ver los datos", ir: "datos", principal: true },
      visual: () => `<span class="objeto carpeta" style="position:relative;left:auto;top:auto;--r:-4deg"><span class="carpeta-pestana"></span><span class="carpeta-cuerpo"><b>Datos y código</b><small>${C.filasPanel} observaciones</small></span></span><span class="nota nota-verde" style="--r:5deg;right:7%;bottom:12%">Fuentes<br>oficiales ✓</span>` },
    { nombre: "Lo que encontré", titulo: "Creció mucho, pero en muy pocas manos",
      texto: "Estos son los resultados principales, dichos en simple.",
      lista: [li("📈", "verde", "Creció rápido", `De S/ ${C.monto2022} millones en 2022 a S/ ${C.monto2025} millones en 2025.`),
        li("🏆", "ambar", "Una plataforma domina", `${C.nombreLider} reúne el ${C.participacionLider} % de todo lo financiado.`),
        li("🔗", "azul", "No se mueve con las tasas del banco", `Con ${C.muSeriesObs} meses no hay evidencia de una relación estable con las tasas de bancos y cajas.`),
        li("📜", "coral", "La norma de 2025", "No se encontró evidencia de que haya impulsado el monto: ya venía creciendo.")],
      boton: { texto: "Explorar en el dashboard", href: P.dashboard, principal: true },
      visual: () => `<div class="grafico-paso"><p class="grafico-titulo">Monto financiado cada mes (S/ millones)</p>${grafico()}</div>` },
    { nombre: "Lo que preparé", titulo: "Todo lo que entrego",
      texto: "El artículo es el centro, y alrededor hay productos para presentarlo, revisarlo y repetirlo. Toca cualquiera para verlo.",
      lista: [li("📄", "azul", "Para leer", "El artículo en dos versiones (LaTeX y Typst) y la guía del proyecto."),
        li("🎤", "coral", "Para exponer", "El Beamer, el póster A0 y los 20 pósteres del estado del arte."),
        li("🧰", "verde", "Para revisar", "Los datos, el código y el dashboard interactivo.")],
      boton: { texto: "Descargar el artículo", stem: "Aliaga_Damian_articulo_FPF_Peru" },
      visual: () => `<div class="mosaico">${[["articulo", "📄", "Artículo", "azul"], ["beamer", "🎤", "Beamer", "coral"], ["poster", "🖼️", "Póster A0", "verde"],
        ["posteres", "🗂️", "20 pósteres", "violeta"], ["datos", "🧮", "Datos", "ambar"], ["dashboard", "💻", "Dashboard", "azul"]]
        .map(([k, em, t, c]) => `<button type="button" class="em-${c}" data-abrir-paso="${k}"><span class="em">${em}</span>${t}</button>`).join("")}</div>` },
    { nombre: "¿Es confiable?", titulo: "Cualquiera puede comprobarlo",
      texto: "Los resultados no dependen de confiar en mí: el proyecto trae cómo verificarlos.",
      lista: [li("🧪", "verde", `${V.pruebas} pruebas automáticas`, "Revisan la extracción, la limpieza, el análisis y el dashboard."),
        li("🔍", "azul", `${V.controles} controles de auditoría`, "Comparan los datos entregados con las fuentes, en vivo."),
        li("🔐", "violeta", "Huella SHA-256", "Confirma que la base no se modificó después del análisis."),
        li("💻", "ambar", "Código abierto", "Todo está en GitHub para repetirlo desde cero.")],
      boton: { texto: "Ver el código en GitHub", href: P.repositorio, principal: true },
      visual: () => `<div class="sello-grande"><b>${V.pruebas}</b><span>pruebas<br>aprobadas</span></div><span class="nota nota-rosa" style="--r:-6deg;left:8%;bottom:12%">¡Todo en verde!</span>` },
  ];
  const lista_pasos = $("#pasos"), caja = $("#paso");
  let paso = 0;
  lista_pasos.innerHTML = PASOS.map((p, i) => `<li role="presentation"><button type="button" role="tab" id="tab-${i}" aria-controls="paso" aria-selected="false"><span class="num">${i + 1}</span><span class="nom">${p.nombre}</span></button></li>`).join("");
  const mostrarPaso = (i, enfocar) => {
    paso = Math.max(0, Math.min(PASOS.length - 1, i));
    const p = PASOS[paso];
    $$("button", lista_pasos).forEach((b, k) => { b.setAttribute("aria-selected", k === paso); b.classList.toggle("hecho", k < paso); b.tabIndex = k === paso ? 0 : -1; });
    const bt = p.boton.stem ? (() => { const d = descarga(p.boton.stem); return `<a class="boton boton-principal" href="${d.url}" download="${d.nombre}">${p.boton.texto} <small>${d.mb} MB</small></a>`; })() : boton(p.boton);
    caja.setAttribute("aria-labelledby", `tab-${paso}`);
    caja.innerHTML = `<div class="paso-texto"><p class="cejilla">Paso ${paso + 1}</p><h3>${p.titulo}</h3><p>${p.texto}</p><ul class="datos-paso">${p.lista.join("")}</ul>${bt}</div><div class="paso-visual">${p.visual()}</div>`;
    caja.style.animation = "none"; void caja.offsetWidth; caja.style.animation = "";
    $("#cuenta").textContent = `${paso + 1} de ${PASOS.length}`;
    $("#anterior").style.visibility = paso === 0 ? "hidden" : "visible";
    $("#siguiente").textContent = paso === PASOS.length - 1 ? "Volver a empezar ↺" : "Siguiente →";
    if (enfocar) $$("button", lista_pasos)[paso].focus();
  };
  $$("button", lista_pasos).forEach((b, i) => b.addEventListener("click", () => mostrarPaso(i)));
  lista_pasos.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowRight") { ev.preventDefault(); mostrarPaso(paso + 1, true); }
    if (ev.key === "ArrowLeft") { ev.preventDefault(); mostrarPaso(paso - 1, true); }
  });
  $("#anterior").addEventListener("click", () => mostrarPaso(paso - 1));
  $("#siguiente").addEventListener("click", () => mostrarPaso(paso === PASOS.length - 1 ? 0 : paso + 1));
  caja.addEventListener("click", (ev) => {
    const a = ev.target.closest("[data-abrir-paso]"); if (a) return abrir(a.dataset.abrirPaso);
    const ir = ev.target.closest("[data-ir]"); if (ir) abrir(ir.dataset.ir);
  });
  mostrarPaso(0);
})();
