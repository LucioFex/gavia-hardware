# gavia-hardware

Parte de Gavia, un dron salvavidas autónomo con IA.

Modelos 3D, lista de materiales e instrucciones de armado del dron salvavidas autónomo: cápsula
liberadora, protectores y frame.

> Prototipo experimental en desarrollo. No es un equipo de rescate certificado y no reemplaza a
> un guardavidas.

## Qué hay acá

| Carpeta | Contenido |
|---|---|
| `cad/` | Archivos fuente editables (Blender, CAD) |
| `stl/` | Piezas listas para imprimir en 3D |
| `bom/` | Lista de materiales |
| `docs/` | Instrucciones de armado y notas de impresión |

## Las piezas

El dron es un cuadricóptero de 5 pulgadas, lo más chico posible que pueda cargar el flotador con el
viento de la costa. Las piezas propias del proyecto son:

- Cápsula liberadora. Es un "huevo" de plástico liso, sin ganchos ni partes salientes con las que
  alguien se pueda lastimar. Adentro tiene un pasador que mueve un servo. Cuando el pasador sale, cae
  el flotador junto con su soga, así la persona en el agua nunca queda atada al dron.
- Eslabón débil. Es el respaldo por si el servo falla: si alguien tira de la soga, la unión se
  corta.
- Protectores de hélice, para volar cerca de gente.
- Frame impreso en PETG o nylon con fibra de carbono. El plan B es un frame comercial de fibra
  de carbono.
- Carcasa estanca de la botonera del guardavidas.

El flotador es un tubo que se infla solo al tocar el agua, con un cartucho de CO₂ de 16 g. Las
pruebas de la demo se hacen con un flotador de espuma.

## Estado

En diseño. Todavía no hay modelos publicados.

## Repos del proyecto

- [gavia-vision](https://github.com/LucioFex/gavia-vision): detección y lógica de decisión
- [gavia-firmware](https://github.com/LucioFex/gavia-firmware): botonera ESP32 y configuración de ArduPilot
- [gavia-hardware](https://github.com/LucioFex/gavia-hardware): modelos 3D y lista de materiales (este repo)

## Licencia

[CERN-OHL-P-2.0](LICENSE), una licencia permisiva de hardware abierto. Copyright 2026 Luciano
Esteban y Elías Espinosa.

## Autores

- Luciano Esteban ([@LucioFex](https://github.com/LucioFex))
- Elías Espinosa
