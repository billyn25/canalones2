# Fuentes · Tejados y Canalones

Web estática para `https://limpiezacanalonestejadosurgente.com`. Contacto: +34 641 49 05 36.

## Construir y comprobar

Se necesita Python 3.10 o posterior. Sin paquetes externos ni claves.

```sh
python3 build.py
python3 scripts/check_site.py
```

`dist/` es el directorio que se publica. Contiene 76 páginas HTML: inicio, seis provincias, 60 municipios principales, cuatro servicios, una galería de trabajos, dos guías y dos páginas legales. El sitemap contiene las 74 páginas comerciales/editoriales. Las páginas legales llevan `noindex,follow` y siguen accesibles desde el pie.

## Netlify

Importar este repositorio, rama `main`. `netlify.toml` ya configura el build y `dist/`. Añadir `limpiezacanalonestejadosurgente.com` como dominio principal en Netlify y aplicar los registros DNS que indique su panel. Añadir también `www` como alias si se desea y redirigirlo al dominio principal. No se ha configurado DNS desde este repositorio.

La URL canónica se define en `config.json`; no cambia por el host de cada petición. Si se cambia el dominio, actualizar ese dato y reconstruir. `SITE_URL` permite sobrescribirlo explícitamente. Las ramas y deploy previews de Netlify se generan con `INDEXABLE=false`; producción es indexable. La vista previa privada de ChatGPT no sustituye el despliegue público en el dominio.

Tras conectar dominio: comprobar HTTPS, redirección del alias, código 200 de las páginas y código 404 para una ruta inexistente. En Search Console comprobar la propiedad del dominio, enviar `/sitemap.xml`, inspeccionar inicio y una provincia y revisar Acciones manuales y Problemas de seguridad. La configuración técnica no garantiza rastreo, indexación ni posiciones.

## Cobertura territorial

934 municipios: Vizcaya 113, Álava 51, Guipúzcoa 88, Burgos 371, Segovia 209, Cantabria 102. Se conservan los nombres y códigos de la fuente; algunos municipios disponen además de un nombre comercial conocido y alias de búsqueda. No es un nomenclátor de todas las aldeas, barrios o entidades menores: estas se atienden dentro de su municipio, previa consulta.

Cada municipio está asignado una sola vez a una página principal de su provincia según la cercanía entre centroides, usando coordenadas como orientación, no como distancias por carretera ni rutas de trabajo confirmadas. Cada principal incluye contenido propio y su lista de cobertura. Los pequeños enlazan a anclas reales en esa lista, sin crear páginas nuevas. El buscador comprende los 934 municipios. Las provincias y listas de cobertura están en el HTML y pueden leerse sin JavaScript.

Fuentes, licencia y limitaciones de los datos en `data/SOURCES.md`. No se asignan oficinas a cada localidad, ni se inventan trabajos, reseñas o cifras de experiencia.

## Consultas

El formulario construye el mensaje en el navegador y abre WhatsApp al pulsar el botón. No envía datos a una base de datos de la web ni almacena formularios en el dispositivo. El visitante revisa y envía desde WhatsApp. Teléfono y enlace directo funcionan sin JavaScript.

## Actualizar contenido

- `config.json`: marca, dominio, teléfono y datos legales.
- `data/hubs.json`: páginas principales y contenido específico.
- `data/municipalities.json`: listado municipal y centroides.
- `data/services.json`: contenidos de servicios.
- `assets/`: CSS, JavaScript, favicon y fotografías optimizadas.
- `build.py`: plantillas, páginas, sitemap, robots y configuración de salida.

El nombre completo del titular solo se imprime en aviso legal y privacidad; no aparece en el pie ni como persona en el JSON-LD. No añadir una ficha de negocio o una dirección ficticia por municipio.

### Protección de publicación

Producción en Netlify fija `INDEXABLE=true`. Si el entorno de producción intenta publicar con `INDEXABLE=false` o con una URL canónica distinta del dominio definido en `config.json`, el build falla antes de escribir la salida. Las páginas de provincia describen solo esa provincia en `Service.areaServed`; los principales incluyen los municipios de su lista visible. El informe `SEO-REVISION.md` distingue las comprobaciones del código de lo que todavía debe verificarse en el dominio público y Search Console.


## Fotografías de trabajos

`data/photos.json` describe las 19 fotografías aportadas por el titular. Se publican como trabajos y revisiones propios, con descripciones de los elementos visibles, sin asignar una localidad, fecha de ejecución, intervención completada o un antes/después que no se haya confirmado. Las imágenes figuran en inicio, servicios, provincias y principales; `/trabajos/` reúne las 19. Los originales aportados no se retocan: se generan copias WebP y miniaturas para la web. Los enlaces a fotografías funcionan sin JavaScript; la ampliación en diálogo añade cierre, navegación con botones y teclado y recuperación del foco.
