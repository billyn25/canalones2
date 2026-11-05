# Revisión previa a publicación

Dominio previsto: https://limpiezacanalonestejadosurgente.es

## Cambios realizados

- Se sustituye una cobertura parcial por los 934 municipios de seis provincias, con una sola asignación por municipio.
- 38 principales con introducción, criterio de revisión, información necesaria y pregunta propios. Los municipios pequeños se integran en esas zonas; no se generan 934 landings.
- Limpieza de tejados y limpieza de canalones aparecen por separado en título/descripción y apartados de las páginas municipales. Cada servicio tiene además una ficha propia con su alcance.
- Reparación de goteras y canalones/bajantes se distinguen de la limpieza. Sin precios, certificaciones, experiencia, reseñas o plazos inventados.
- Nombre completo del titular solo en páginas legales. Pie nuevo con marca, contacto, servicios y enlaces territoriales.
- URL canónica absoluta por página, dominio único configurable, Open Graph, favicon y rutas estables con barra final.
- Se diferencia Burgos provincia de Burgos municipio y Segovia provincia de Segovia municipio en los títulos.
- Datos estructurados de negocio con una única dirección, WebSite, WebPage, Service y BreadcrumbList. Sin AggregateRating ni oficinas ficticias.
- HTML estático para contenido y enlaces; cobertura disponible sin JavaScript; búsqueda auxiliar de los 934 municipios con destino existente.
- Sitemap limitado a páginas indexables; robots permite rastreo. Legales fuera del sitemap. 404 propia, sin redirección de cualquier ruta al inicio.
- Imágenes locales WebP con dimensiones, carga diferida fuera de la cabecera y textos alternativos descriptivos. Sin analítica, mapas ni fuentes externas.
- La consulta solo prepara un mensaje de WhatsApp; no crea solicitudes en un servidor.

## Comprobaciones automáticas

`python3 scripts/check_site.py` verifica páginas, enlaces, fragmentos, canónicas, títulos y descripciones únicos, un H1, datos JSON-LD parseables, proveedor de Service y orden de breadcrumbs, ausencia de huérfanas, coincidencia del sitemap, 934 municipios sin omisiones y nombre personal fuera del pie y de las páginas comerciales. Es un control técnico del contenido generado, no una certificación de Google ni una prueba de todas las reglas de Schema.org.

## Lo que sigue dependiendo de datos externos

No se ha diagnosticado la caída de la web anterior. Para atribuir una causa hacen falta su dominio, fechas de la caída, rendimiento e indexación de Search Console y comprobación de acciones manuales/seguridad. No se puede deducir una penalización solo por una pérdida de posiciones.

Esta nueva web no dispone todavía de trabajos locales documentados, fotos propias, referencias verificables ni información confirmada sobre medios, seguros o condiciones comerciales. No se han inventado. Esos materiales pueden aportar más valor que añadir nuevas variantes de texto. La agrupación de municipios no garantiza visibilidad para cada nombre.

Antes de anunciar la web pública deben conectarse dominio y alojamiento, comprobar HTTPS/host principal y estados HTTP reales. Revisa también los datos legales con el titular; no se ha facilitado NIF ni correo electrónico para completarlos.

## Referencias

- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

Evitar contenido masivo sin valor es un criterio de elaboración; no existe un umbral de similitud que garantice posicionamiento ni una forma de asegurar que Google no desindexe una web.

## Segunda auditoría — 5 de noviembre de 2026

Alcance: código de `main` en GitHub (punto de partida `e94f0e4e5ebfe705b7059ff8289a5c3d6dd3a75b`), HTML generado y documentación oficial de Google y Schema.org. No se pudo verificar el dominio público desde este entorno: tanto el servicio de búsqueda como la conexión HTTP fallaron. El error local fue un timeout del proxy; no demuestra que el dominio esté caído, sin DNS o penalizado. No se ha accedido a Search Console.

### Hallazgos corregidos

1. **Cobertura de Service demasiado amplia en provincias.** Las fichas provinciales heredaban las seis provincias, aunque la página trataba de una sola. Ahora cada provincia marca solo su territorio y cada principal marca exactamente los municipios de su lista visible. Se enlaza WebPage con su servicio principal.
2. **Posible publicación accidental sin indexación.** Antes, `INDEXABLE=false` podía generar toda la web con `noindex` y un sitemap vacío sin que el chequeo lo rechazase. Ahora producción declara `INDEXABLE=true`; el build cancela la publicación si detecta producción con `noindex` global o dominio canónico distinto del configurado. Las vistas previas siguen fuera del índice.
3. **Coherencia de dirección visible y datos estructurados.** La dirección facilitada y confirmada por el titular aparece ahora en el pie, además de las páginas legales, coincidiendo con el JSON-LD. El nombre completo sigue únicamente en las páginas legales.

### Comprobaciones realizadas

- 53 páginas HTML; 51 comerciales/editoriales indexables y dos legales fuera del sitemap.
- Los 934 municipios están asignados una sola vez; enlaces y anclas existen.
- Sin enlaces internos rotos ni páginas huérfanas en el HTML generado.
- Títulos y descripciones únicos, una canónica y un H1 por página.
- Sin valoraciones falsas, plazos 24 horas inventados, oficinas ficticias por localidad, contenido oculto para buscadores o diferencias por user-agent.
- Los bloques de navegación, formulario, servicios y algunas explicaciones se comparten entre páginas; no se ha usado una puntuación de similitud como supuesto umbral de Google.
- Build de producción indexable: comprobado; producción con noindex global: rechazada; producción con host canónico equivocado: rechazada; deploy preview sin indexación: comprobado. Las pruebas se ejecutaron en copias temporales para conservar intacta la salida de producción.

### Riesgos y límites que permanecen

- Las páginas locales aportan consejos de consulta distintos y cobertura territorial; no hay trabajos locales documentados, fotos propias ni testimonios verificables. Los consejos generales adaptados a una localidad no equivalen a prueba de experiencia allí. Añadir documentación real y confirmar condiciones comerciales es el siguiente trabajo editorial útil, antes de multiplicar páginas.
- Esta web no se ha comparado íntegramente con la web anterior. No se ha determinado si son negocios distintos o dos webs del mismo servicio. Si representan el mismo negocio, conviene valorar una presencia principal en vez de clonar ofertas y contenido en varios dominios.
- No se han comprobado estados HTTP reales, DNS, TLS, host principal, reglas de cuenta en Netlify, X-Robots-Tag externos, tiempos de carga de producción ni Core Web Vitals de campo. Las reglas del alojamiento y sus controles de acceso pueden bloquear el sitio aunque el HTML sea correcto.
- Solo Search Console puede confirmar el estado de acciones manuales, seguridad y URLs inspeccionadas de esa propiedad. La auditoría del código no acredita que Google haya rastreado, indexado o descartado una página.
- No se garantiza ausencia futura de penalizaciones ni posiciones. La política de Google se refiere al valor y propósito del contenido, no a un porcentaje de similitud ni a ocultar el uso de herramientas.
