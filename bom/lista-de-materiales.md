# Lista de materiales del prototipo

Compras por fase del plan "medir antes de construir", en la versión simplificada del 30/10/26:
banco con el sensor de agua (`cad/banco/`), cuerpo del aro en telgopor (`cad/cuerpo/`) y vuelo
atado. La IA a bordo queda para después. El paso a paso de cómo pedir y armar cada cosa está en
`docs/roadmap/gavia-roadmap-prototipo.pdf`.

Precios de MercadoLibre Argentina consultados el 30/10/26, pasados a dólares con el MEP de $1.568
([DolarHoy](https://dolarhoy.com/)). Lo que viene de China no incluye impuestos. Cambian rápido:
revisalos antes de comprar.

## Antes de comprar

- Importados repartidos entre los tres. Las publicaciones de China avisan que se pueden recibir
  hasta 5 envíos internacionales por año por persona, sumando todas las plataformas. Si cada uno
  compra con su cuenta, usa su propio cupo, y el paquete llega a nombre y a la dirección de quien
  compra. Sugerencia: motores (Lucho) y ESC del banco (Eli) en la fase 1, controladora y ESC del dron
  (Augus), GPS (Lucho) y radio con receptor (Eli) en la fase 3. Cómo cuenta MercadoLibre el límite
  (por compra o por paquete) está a validar.
- Motores. Ningún vendedor es tienda oficial. Preguntar por mensaje si son Hobbywing originales y
  cuántos trae el pack. El banco lo confirma: si el empuje medido se parece a la tabla, son buenos.
- Batería. Preguntarle al vendedor el peso y la ficha (XT60 o XT90) antes de comprar. Todo el
  proyecto usa la ficha que traiga la batería. Pesa más que la de 3000 mAh que supone el modelo: al
  recibirla se pesa y se actualiza `masa_bateria_kg`.

## Fase 1: banco, con herramientas y sensor de agua (unos USD 816)

### Herramientas

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Soldador | Estación T12 G Tools 72 W | 95.101 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5129242865) |
| Estaño | Mechanic 63/37, 0,8 mm, 60 g, con flux | 10.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3765784628) |
| Multímetro | Uni-T UT89XD | 37.900 | [ML](https://www.mercadolibre.com.ar/x/p/MLA22611320) |
| Cable | Silicona 12 AWG, 2 m rojo y 2 m negro (confirmar largo) | 29.900 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3256538588) |
| Termocontraíble | Kit de 560 piezas | 15.200 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5069989514) |
| Anteojos | Libus 900555, x3 | 10.340 | [ML](https://www.mercadolibre.com.ar/x/p/MLA24368245) |
| | Subtotal | 198.941 | |

### Banco

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Motores | Hobbywing XRotor 2812 900KV, pack de 4 | 127.997 | China | [ML](https://www.mercadolibre.com.ar/hobbywing-xrotor-2812-900kv-motor-brushless-fpv-4-unidades/up/MLAU5301615561) |
| Hélices | Gemfan 8046-3, 3 packs de 2: uno para el banco y dos para el dron. Es la única hélice del proyecto y escasea | 148.503 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU2977712694) |
| ESC | EMAX BLHeli 60A, 2 a 6S | 53.168 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Batería | Pulse 6S 5200 mAh 80C | 270.000 | Local (CABA) | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5705660626) |
| Cargador | iMAX B6AC con fuente incluida, 80 W, se enchufa a 220 V | 219.990 | Local (Río Cuarto) | [ML](https://www.mercadolibre.com.ar/up/MLAU132422334) |
| Medidor | Wattímetro 150 A (viene sin fichas) | 79.000 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3010886186) |
| Fichas | XT90, 2 pares (o XT60 si la batería trae XT60) | 22.063 | Local | [ML](https://www.mercadolibre.com.ar/conector-xt90-xt90-fichas-2-macho-2-hembra-40-amp-lipo/up/MLAU3278059021) |
| Celda | 10 kg con HX711 (la de 5 kg queda justa con el banco encima) | 16.795 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3419553238) |
| Placa | ESP32 USB-C | 15.990 | Local | [ML](https://www.mercadolibre.com.ar/nodemcu-esp32-wifi-bluetooth-42-iot-wroom-esp32s-usb-c/p/MLA2038887439) |
| Bolsa | Ignífuga para LiPo, 29 x 23 cm | 37.991 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3258038031) |
| Ducto | Policarbonato 1 mm, 1,2 x 1,2 m. Alcanza para el banco y los cuatro liners del dron | 47.033 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU279911287) |
| Prensas | Sargento Wadfow 300 mm, x2 | 22.800 | Local | [ML](https://www.mercadolibre.com.ar/x/p/MLA2086927338) |
| | Subtotal | 1.061.330 | | |

### Sensor de agua

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Sensor | Módulo LM393 con sonda de agua | 5.604 | [ML](https://www.mercadolibre.com.ar/x/p/MLA2071007363) |
| Electrodos | Varilla roscada inoxidable 316, 1/4" x 1 m | 13.750 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3820171820) |
| | Subtotal | 19.354 | |

Total de la fase 1: $1.279.625, unos USD 816.

Sin cotizar: el corte láser del banco con material incluido (dos planchas de MDF de 5,5 mm y dos discos de
acrílico de 6 mm, por ejemplo
[este servicio en Almirante Brown](https://servicio.mercadolibre.com.ar/MLA-3214912144-servicio-corte-laser-co2-mdf-acrilico-madera-goma-grabados-_JM)),
la manguera para el labio y los tornillos. El acrílico, el fenólico y las planchuelas de aluminio de
la lista anterior ya no hacen falta: todo sale del láser.

## Fase 2: cuerpo (unos USD 66)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Corte | Tres capas de EPS de 30 mm y 30 kg/m³ con material incluido (`cad/cuerpo/`) | a cotizar | |
| Pegamento | Novolastic para telgopor, x2 | 21.091 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU280100227) |
| Dinamómetro | Balanza colgante digital 50 kg | 20.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU4045801615) |
| Lastre | Cressi forrado 1 kg, x3 (la publicación da $30.478 por dos) | 45.717 (aprox.) | [ML](https://www.mercadolibre.com.ar/x/up/MLAU297562071) |
| Cajas | Caja de paso estanca IP65 Kalop (Unika) 120 x 170 x 75 mm, x2 ($8.011 c/u) | 16.022 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3893576153) |
| | Subtotal | 103.330 | |

Talleres para consultar el corte:
[Telgopor Quilmes](https://www.instagram.com/telgoporquilmes/),
[Deletrearte](https://deletrearte.com.ar/Servicios/) y
[RotulArte](https://rotularte.com.ar/producto/corte-cnc-por-hora-servicio-para-grafica-y-carteleria/)
(CABA, CNC desde $61.440 la hora, hilo caliente a convenir). Si el taller no pone el material, hacen
falta tres planchas de EPS de 1 x 1 m de 30 mm. Sin cotizar: la entrada a la pileta. En el país no
encontramos cajas IP67 de menos de 90 mm de alto que sirvan, por eso van las IP65 y se prueban 30
minutos a 1 m en la pileta.

## Fase 3: vuelo atado (unos USD 625, con el plan B)

La controladora y los ESC se eligen al terminar el banco: un stack con ESC 4 en 1 de 6S y 55 A o
más por canal, con soporte oficial de ArduPilot, comprado junto. En MercadoLibre no apareció un
SpeedyBee F405 V4 original (ArduPilot lo soporta,
[docs](https://ardupilot.org/copter/docs/common-speedybeef4-v3.html)), solo uno "Marca Generic"
desde China a [$438.142](https://www.mercadolibre.com.ar/p/MLA2088323725). Si no aparece uno de
marca confirmada, va el plan B de la tabla.

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Controladora (plan B) | Matek H743-WING V3 ([ArduPilot](https://ardupilot.org/copter/docs/common-matekh743-wing.html)) | 275.210 | China | [ML](https://www.mercadolibre.com.ar/controlador-de-vuelo-inav-de-ala-fija-matek-h743-wing-v3/p/MLA2122662864) |
| ESC (plan B) | EMAX BLHeli 60A, x3 más (máximo 3 por compra) | 159.504 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Distribución (plan B) | Matek FCHUB-12S V2, con sensor de 440 A | 66.392 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2080086204) |
| GPS | MicoAir M10G-5883 | 69.906 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2085469012) |
| Radio | Radiomaster Pocket ELRS | 201.977 | Internacional | [ML](https://www.mercadolibre.com.ar/p/MLA2075906042) |
| Receptor | Radiomaster RP3 ELRS 2,4 GHz | 86.355 | Internacional | [ML](https://www.mercadolibre.com.ar/p/MLA2099353396) |
| Estructura | Tubo de carbono 13 x 10 x 1000 mm | 96.000 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU4047653302) |
| Buzzer | Activo 5 V, x5 | 6.519 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3532054677) |
| Bloqueo | Relé biestable 5 V | 7.490 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU227966400) |
| Reset | Reed switch NA, x6 | 5.895 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3856250498) |
| Imán | Neodimio 10 x 3 mm, x5 | 4.790 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU136862942) |
| | Subtotal | 980.038 | | |

La telemetría va por el mismo enlace ELRS, sin radio aparte
([ExpressLRS](https://www.expresslrs.org/software/mavlink/)). Alternativa más barata de controladora:
MicoAir743 a $127.216 ([ML](https://www.mercadolibre.com.ar/p/MLA2039430017),
[ArduPilot](https://ardupilot.org/copter/docs/common-MicoAir743.html)). El circuito del bloqueo por
agua se define con el umbral medido en la fase 1, así que esas tres piezas pueden cambiar.

Sin cotizar: las ocho rejillas del dron (mismo archivo de láser que el banco, en acrílico de 6 mm),
la piel (laminado epoxi sobre EPS en un taller de tablas de surf, o membrana acrílica a pincel, nunca
resina poliéster porque derrite el telgopor), un posible segundo tubo de carbono, las dos 18650 de
la radio y la botonera (lista en `cad/blender/botonera_piezas.md`). Los liners salen de la plancha
de policarbonato de la fase 1.

## Después: IA a bordo (unos USD 370)

Queda fuera del primer prototipo y se encara después del primer vuelo atado.

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Computadora | Raspberry Pi 5 8 GB | 431.308 | [ML](https://www.mercadolibre.com.ar/p/MLA32625223) |
| Cámara | Raspberry Pi AI Camera (IMX500, IA en el sensor) | 134.527 | [ML](https://www.mercadolibre.com.ar/p/MLA47068778) |
| Luz | Tira LED WS2812B 1 m | 14.724 | [ML](https://www.mercadolibre.com.ar/p/MLA47128873) |
| | Subtotal | 580.559 | |

Sin cotizar: un BEC de 5 V 5 A para la Raspberry. El peso de la computadora y la cámara no figura
en las publicaciones y hay que medirlo, porque suma a los 3,4 kg.

## Total

Las fases 1 a 3 suman unos $2.362.993, cerca de USD 1.507, sin impuestos ni lo que falta cotizar.
El plan anterior daba unos USD 2.012 con la IA a bordo incluida.

## Si algo no está

Lo escaso se compra temprano. Lo que no hay no se persigue hasta que haga falta. Revisado el 30/10/26.

| Pieza | Qué puede pasar | Plan A | Plan B |
|---|---|---|---|
| Batería | Una sola publicación local que sirve (5 disponibles) | Pulse 6S 5200 80C, en la primera tanda | [Ovonic 6S 5000 130C con XT90](https://www.mercadolibre.com.ar/up/MLAU4006221150), $459.124, importada |
| Hélices | Casi no hay de 8 pulgadas tripala de marca y tardan una semana | Los 3 packs de Gemfan 8046 juntos, en la fase 1 | Traer Gemfan o HQ 8x4.5x3 junto con los motores |
| Motores | El vendedor no es tienda oficial | Pack de 4 Hobbywing. La configuración a del banco dice si son originales | Devolverlos con la compra protegida y probar otro vendedor |
| Celda | Hay varias | 10 kg con HX711, $16.795 | [Otra igual](https://www.mercadolibre.com.ar/up/MLAU294756996), $16.479 |
| Controladora | No hay stack SpeedyBee original, solo genéricos | Se elige después del banco | Matek H743-WING (ver fase 3) |
| Cajas | No hay IP67 de menos de 90 mm de alto | Kalop IP65 de 120 x 170 x 75 mm | Si no pasan la prueba de la pileta, otra caja y se regeneran las capas |
| Talleres | No publican precios | Pedir presupuesto a dos o tres de cada tipo apenas se arranca | Otro taller de la lista |

