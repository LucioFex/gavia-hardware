# Materiales y conceptos

`gavia-materiales-y-conceptos.pdf` explica qué es cada cosa del dron flotador, de qué está hecha y
cómo se fabrica, para leer antes de comprar, pedir o armar algo. Se actualiza en cada sesión.

La fuente es `index.html`. Para regenerar el PDF, con Work Sans instalada y desde esta carpeta:

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --no-pdf-header-footer --print-to-pdf="%CD%\gavia-materiales-y-conceptos.pdf" "file:///%CD:\=/%/index.html"
```

Para sumar un concepto, agregá un par `<dt>` y `<dd>` en la sección que corresponda.
