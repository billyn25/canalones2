# Datos e imágenes

## Municipios y centroides

Archivo de origen: https://github.com/ManuelCebreiro/spanish-cities-info/blob/main/src/data/cities.json

Consulta: 5 de noviembre de 2026. Se conserva el subconjunto de las provincias 01, 09, 20, 24, 39, 40 y 48. Según la documentación del proveedor, los nombres y códigos se reconcilian con la relación del INE a 1 de enero de 2026; las coordenadas son centroides geométricos del dataset `georef-spain-municipio` de Opendatasoft, con base IGN, bajo CC BY 4.0. No son posiciones de oficinas ni necesariamente el centro urbano. La descarga directa del fichero anual del INE no pudo verificarse en este entorno; se utilizó el conjunto publicado y documentado por su mantenedor.

- https://github.com/ManuelCebreiro/spanish-cities-info
- https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177031&idp=1254735976614&menu=ultiDatos
- https://public.opendatasoft.com/explore/dataset/georef-spain-municipio/
- https://creativecommons.org/licenses/by/4.0/

Modificaciones: filtrado por provincias y agrupación de cada municipio alrededor del principal más próximo de su provincia. La agrupación se calcula con centroides y no describe rutas por carretera, sedes locales ni disponibilidad confirmada. Se añaden nombres conocidos y alias en algunos principales, conservando los códigos de origen. Las denominaciones de provincia mostradas comercialmente son Vizcaya, Álava y Guipúzcoa.

Licencia del proyecto fuente:

ISC License

Copyright (c) 2026 Manuel Cebreiro

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

## Fotografías

- `assets/tejado.webp`: Adrien Olichon, «Photo of Roof While Raining», Pexels. https://www.pexels.com/photo/photo-of-roof-while-raining-2663254/ . Licencia Pexels: https://www.pexels.com/license/ . Adaptación: reducción de tamaño y conversión a WebP.
- `assets/canalon.webp`: Luke Southern, «A close up of a rain gutter on a roof», Unsplash. https://unsplash.com/photos/a-close-up-of-a-rain-gutter-on-a-roof-ZzZouwiQWV0 . Licencia Unsplash: https://unsplash.com/license . Adaptación: reducción de tamaño y conversión a WebP.

Son fotografías de ambientación; no se atribuyen al titular como trabajos realizados ni se presentan como imágenes de las localidades cubiertas.



## Fotografías de trabajos aportadas el 5 de noviembre de 2026

El usuario facilita diez fotografías y las identifica como trabajos reales del negocio. Archivos publicados: `assets/trabajos/*.webp`. El catálogo y las descripciones figuran en `data/photos.json`. Se generan miniaturas y copias optimizadas en WebP; no se modifica el contenido de las escenas. No se deduce el municipio, la fecha del trabajo ni que una escena documente una reparación terminada. Las fotografías anteriores de Pexels y Unsplash se conservan como recursos heredados, pero ya no se utilizan en las páginas.

## Ampliación de fotografías propias · 6 de noviembre de 2026

Se incorporan nueve fotografías adicionales facilitadas y confirmadas por el usuario como trabajos reales. La galería reúne 19 fotografías; se describen los elementos visibles sin atribuir municipios ni resultados de reparación no documentados. Copias WebP y miniaturas sin alterar las escenas.

## León y fotografías adicionales · 6 de noviembre de 2026

211 municipios de León del mismo dataset; total contrastado con https://www.dipuleon.es/municipios/ayuntamientos-de-la-provincia/ . Se incorporan 12 zonas principales, entre ellas Boñar. El usuario identifica las dos nuevas fotos como trabajos reales de Boñar y otras localidades, sin precisar la ubicación de cada imagen. No se identifica cada foto con una dirección ni se presenta la humedad como una reparación terminada. Galería total: 21 imágenes.
