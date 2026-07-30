# Historial de versiones

## Versión 3

Clasifica respaldos por `ID` (columna A) hacia `T` de cada `FOLIO` (columna B). Excluye documentos cuyo `TIPO_DOCUMENTO` (columna G) contenga las palabras “Convenio” y “Becados”, con o sin la palabra “de”.

Si un ID válido aparece en varios folios, al copiar se deja una copia en cada carpeta `T` relacionada. Para evitar pérdida de respaldos, esos IDs no se mueven.

## Versión 2

Clasifica cada archivo por `COEG_NUMERO` (columna C) y lo copia o mueve a `CE` de la primera carpeta `FOLIO` (columna B) donde aparece ese COEG.

Ejemplo: el archivo `7005.pdf` va a `1/CE`; `7008.pdf` va a `274/CE`. Las repeticiones posteriores del mismo COEG no generan copias adicionales.

## Versión 1

Estado inicial: crea carpetas por `FOLIO`, con subcarpetas `CE` y `T`, y permite ordenar archivos por coincidencia de folio en el nombre.
