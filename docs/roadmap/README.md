# Roadmap del prototipo

`gavia-roadmap-prototipo.pdf` es la guía paso a paso para armar el prototipo en tres fases (banco,
cuerpo y vuelo atado): qué conseguir, qué poner en el buscador de MercadoLibre, qué archivo mandar
a cada taller con el mensaje para copiar, cómo se arma y cuándo se pasa a la fase siguiente. Está
pensado para armarlo sin experiencia previa en drones ni en electrónica. Se actualiza en cada
sesión.

La fuente es `index.html`. Para regenerar el PDF, con Work Sans instalada y desde esta carpeta:

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --no-pdf-header-footer --print-to-pdf="%CD%\gavia-roadmap-prototipo.pdf" "file:///%CD:\=/%/index.html"
```

Las imágenes de `img/` son ilustrativas, generadas con Gemini para que el equipo se vea en cada
momento del trabajo. No son fotos de pruebas y pueden tener detalles que no coinciden con el
diseño. Lo que vale para armar son los dibujos con medidas de `cad/banco/` y `cad/cuerpo/`, y la
lista con precios y links de `bom/lista-de-materiales.md`.
