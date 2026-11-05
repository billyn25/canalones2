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
