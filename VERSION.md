# Historial de versiones

## Versión 5

Los archivos llamados exactamente `NOMINA-<COEG_NUMERO>` se distribuyen en la carpeta `T` de **todos** los `FOLIO` (columna B) que tengan ese mismo `COEG_NUMERO` (columna C). Por ejemplo, si `7085` aparece en diez folios, `NOMINA-7085.pdf` queda en las diez carpetas `T` correspondientes. La nómina se copia en los destinos necesarios y el original se mueve al último destino, de modo que deja de estar en la carpeta de origen.

Esta regla aplica únicamente a archivos `NOMINA-*`. Los archivos COEG normales mantienen su destino en `CE` del primer folio asociado.

## Versión 4

Durante el ordenamiento por `COEG_NUMERO` (columna C), los archivos llamados exactamente `NOMINA-<COEG_NUMERO>` se detectan de forma prioritaria y se **mueven** a `T` del primer `FOLIO` (columna B) asociado al COEG. Por ejemplo, `NOMINA-7085.pdf` se mueve a la carpeta `T` del primer folio que contiene el COEG `7085`.

Los demás archivos COEG conservan el comportamiento anterior y se copian o mueven a `CE` según la acción seleccionada. Las nóminas sin un COEG válido se omiten y se informan en el resumen.

## Versión 3

Clasifica respaldos por `ID` (columna A) hacia `T` de cada `FOLIO` (columna B). Excluye documentos cuyo `TIPO_DOCUMENTO` (columna G) contenga las palabras “Convenio” y “Becados”, con o sin la palabra “de”.

Si un ID válido aparece en varios folios, al copiar se deja una copia en cada carpeta `T` relacionada. Para evitar pérdida de respaldos, esos IDs no se mueven.

## Versión 2

Clasifica cada archivo por `COEG_NUMERO` (columna C) y lo copia o mueve a `CE` de la primera carpeta `FOLIO` (columna B) donde aparece ese COEG.

Ejemplo: el archivo `7005.pdf` va a `1/CE`; `7008.pdf` va a `274/CE`. Las repeticiones posteriores del mismo COEG no generan copias adicionales.

## Versión 1

Estado inicial: crea carpetas por `FOLIO`, con subcarpetas `CE` y `T`, y permite ordenar archivos por coincidencia de folio en el nombre.
