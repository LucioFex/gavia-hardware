# Lista de materiales del prototipo

Compras por fase del plan "medir antes de construir": herramientas, banco de un ducto
(`cad/banco/`), maqueta de flotación, corte por agua, vuelo atado e IA a bordo. Reemplaza la lista
del dron de 5″, que quedó vieja cuando el dron pasó a ser el flotador.

Precios de MercadoLibre Argentina consultados el 30/10/26, pasados a dólares con el MEP de $1.568
([DolarHoy](https://dolarhoy.com/)). Lo que viene de China no incluye impuestos. Cambian rápido:
revisalos antes de comprar.


## Antes de comprar

- Límite de aduana. Las publicaciones que vienen de China avisan que se pueden recibir hasta 5
  envíos internacionales por año, sumando todas las plataformas. La fase 1 usa 3 (motores, ESC y
  cargador) y la 4a tiene varios más. Conviene juntar lo importado en pocas compras, idealmente del
  mismo vendedor, y preferir lo local. Cómo cuenta ML el límite (por compra o por paquete) está a
  validar.
- Motores. Ningún vendedor es tienda oficial. Preguntar por mensaje si son Hobbywing originales y
  cuántos trae el pack. El banco lo confirma: si el empuje medido se parece a la tabla, son buenos.
- Batería. Preguntarle al vendedor el peso y el conector antes de comprar. Pesa más que la de
  3000 mAh que supone el modelo: al recibirla se pesa y se actualiza `masa_bateria_kg`.

## Fase 0: herramientas (unos USD 127)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Soldador | Estación T12 G Tools 72 W | 95.101 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5129242865) |
| Estaño | Mechanic 63/37, 0,8 mm, 60 g, con flux | 10.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3765784628) |
| Multímetro | Uni-T UT89XD | 37.900 | [ML](https://www.mercadolibre.com.ar/x/p/MLA22611320) |
| Cable | Silicona 12 AWG, 2 m rojo y 2 m negro (confirmar largo) | 29.900 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3256538588) |
| Termocontraíble | Kit de 560 piezas | 15.200 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5069989514) |
| Anteojos | Libus 900555, x3 | 10.340 | [ML](https://www.mercadolibre.com.ar/x/p/MLA24368245) |
| | Subtotal | 198.941 | |

## Fase 1: banco de un ducto (unos USD 602)

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Motores | Hobbywing XRotor 2812 900KV, pack de 4 | 127.997 | China | [ML](https://www.mercadolibre.com.ar/hobbywing-xrotor-2812-900kv-motor-brushless-fpv-4-unidades/up/MLAU5301615561) |
| Hélices | Gemfan 8046-3, un par | 49.501 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU2977712694) |
| ESC | EMAX BLHeli 60A, 2 a 6S | 53.168 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Batería | Pulse 6S 5200 mAh 80C | 270.000 | Local (CABA) | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5705660626) |
| Cargador | ToolkitRC M7 200 W | 135.687 | China | [ML](https://www.mercadolibre.com.ar/x/p/MLA2064780308) |
| Fuente | 24 V 10 A para el cargador | 32.299 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU152378872) |
| Medidor | Wattímetro 150 A (viene sin fichas) | 79.000 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3010886186) |
| Fichas | XT60, macho y hembra | 9.284 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3284321661) |
| Celda | 5 kg con HX711 | 10.700 | Local | [ML](https://www.mercadolibre.com.ar/x/p/MLA62544558) |
| Placa | ESP32 USB-C | 15.990 | Local | [ML](https://www.mercadolibre.com.ar/nodemcu-esp32-wifi-bluetooth-42-iot-wroom-esp32s-usb-c/p/MLA2038887439) |
| Bolsa | Ignífuga para LiPo, 29 x 23 cm | 37.991 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3258038031) |
| Ducto | Policarbonato 1 mm, 1,2 x 1,2 m | 47.033 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU279911287) |
| Rejillas | Acrílico 6 mm, 40 x 30 cm | 35.757 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU4083789410) |
| Base | Fenólico 18 mm, 1/8 de placa | 17.000 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU4040449224) |
| Prensas | Sargento Wadfow 300 mm, x2 | 22.800 | Local | [ML](https://www.mercadolibre.com.ar/x/p/MLA2086927338) |
| | Subtotal | 944.207 | | |

Sin cotizar: corte láser (precio a convenir, por ejemplo
[este servicio en Almirante Brown](https://servicio.mercadolibre.com.ar/MLA-3214912144-servicio-corte-laser-co2-mdf-acrilico-madera-goma-grabados-_JM)),
planchuela de aluminio, bulones, manguera para el labio y un adaptador si la batería no trae XT60
(el XT90 a XT60 sale [$9.889](https://www.mercadolibre.com.ar/x/up/MLAU133881372)).

## Fase 2: maqueta de flotación (unos USD 88)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Espuma | EPS 1 x 1 m, 50 mm, 30 kg/m³, x2 (Almirante Brown) | 66.400 | [ML](https://www.mercadolibre.com.ar/x/p/MLA2126643882) |
| Pegamento | Novolastic para telgopor, x2 | 21.091 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU280100227) |
| Dinamómetro | Balanza colgante digital 50 kg | 20.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU4045801615) |
| Lastre | Cressi forrado 1 kg, x2 | 30.478 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU297562071) |
| | Subtotal | 138.469 | |

Sin cotizar: el corte con hilo caliente. Opciones a consultar:
[Telgopor Quilmes](https://www.instagram.com/telgoporquilmes/),
[Deletrearte](https://deletrearte.com.ar/Servicios/) y
[RotulArte](https://rotularte.com.ar/producto/corte-cnc-por-hora-servicio-para-grafica-y-carteleria/)
(CABA, CNC desde $61.440 la hora, hilo caliente a convenir). Y la entrada a la pileta.

## Fase 3: corte por agua (unos USD 70)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Sensor | Módulo LM393 con sonda de agua | 5.604 | [ML](https://www.mercadolibre.com.ar/x/p/MLA2071007363) |
| Comparador | LM393 suelto | 4.064 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU304182418) |
| Latch | CD4013 | 3.899 | [ML](https://www.mercadolibre.com.ar/x/p/MLA63345726) |
| Relé | Módulo biestable 5 V | 7.490 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU227966400) |
| Reset | Reed switch NA, x6 | 5.895 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3856250498) |
| Imán | Neodimio 10 x 3 mm, x5 | 4.790 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU136862942) |
| MOSFET | IRLZ44N, x2 | 12.398 | [ML](https://www.mercadolibre.com.ar/transistor-mosfet-irlz44n-49a-55v-irlz44-ir-arduino-nubbeo/up/MLAU4368014937) |
| Optoacoplador | PC817, x5 | 4.900 | [ML](https://www.mercadolibre.com.ar/circuito-integrado-optoacoplador-pc817-pack-x-5/p/MLA2118452318) |
| Resistencias | Kit de 600 | 13.708 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU140612356) |
| Capacitores | Kit de 600 cerámicos | 22.999 | [ML](https://www.mercadolibre.com.ar/x/p/MLA63226507) |
| Protoboard | 830 puntos con 120 cables | 10.990 | [ML](https://www.mercadolibre.com.ar/kit-protoboard-830-puntos-120-cables-jumper-dupont-mm-mh-hh/up/MLAU5641877707) |
| Electrodos | Varilla roscada inoxidable 316, 1/4" x 1 m | 13.750 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3820171820) |
| | Subtotal | 110.487 | |

## Fase 4a: vuelo atado (unos USD 754)

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Controladora | Matek H743-WING V3 ([ArduPilot](https://ardupilot.org/copter/docs/common-matekh743-wing.html)) | 275.210 | China | [ML](https://www.mercadolibre.com.ar/controlador-de-vuelo-inav-de-ala-fija-matek-h743-wing-v3/p/MLA2122662864) |
| ESC | EMAX BLHeli 60A, x3 más (máximo 3 por compra) | 159.504 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Distribución | Matek FCHUB-12S V2, con sensor de 440 A | 66.392 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2080086204) |
| GPS | MicoAir M10G-5883 | 69.906 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2085469012) |
| Radio | Radiomaster Pocket ELRS | 201.977 | Internacional | [ML](https://www.mercadolibre.com.ar/p/MLA2075906042) |
| Receptor | Radiomaster RP3 ELRS 2,4 GHz | 86.355 | Internacional | [ML](https://www.mercadolibre.com.ar/p/MLA2099353396) |
| Estructura | Tubo de carbono 13 x 10 x 1000 mm | 96.000 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU4047653302) |
| Buzzer | Activo 5 V, x5 | 6.519 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3532054677) |
| Fichas | XT90, 2 pares | 22.063 | Local | [ML](https://www.mercadolibre.com.ar/conector-xt90-xt90-fichas-2-macho-2-hembra-40-amp-lipo/up/MLAU3278059021) |
| Hélices | 8″, 8 unidades, según lo que diga el banco. Opción: Gemfan F8041-2, x4 pares | 198.005 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3918163590) |
| | Subtotal | 1.181.931 | | |

La telemetría va por el mismo enlace ELRS, sin radio aparte
([ExpressLRS](https://www.expresslrs.org/software/mavlink/)). Alternativa más barata de controladora:
MicoAir743 a $127.216 ([ML](https://www.mercadolibre.com.ar/p/MLA2039430017),
[ArduPilot](https://ardupilot.org/copter/docs/common-MicoAir743.html)). Sin cotizar: la espuma del
cuerpo, los liners y rejillas impresos, un posible segundo tubo de carbono y las dos 18650 de la radio.

## Fase 4b: IA a bordo (unos USD 370)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Computadora | Raspberry Pi 5 8 GB | 431.308 | [ML](https://www.mercadolibre.com.ar/p/MLA32625223) |
| Cámara | Raspberry Pi AI Camera (IMX500, IA en el sensor) | 134.527 | [ML](https://www.mercadolibre.com.ar/p/MLA47068778) |
| Luz | Tira LED WS2812B 1 m | 14.724 | [ML](https://www.mercadolibre.com.ar/p/MLA47128873) |
| | Subtotal | 580.559 | |

Sin cotizar: un BEC de 5 V 5 A para la Raspberry. El peso de la computadora y la cámara no figura
en las publicaciones y hay que medirlo, porque suma a los 3,4 kg.

## Total

Unos $3.154.593, cerca de USD 2.012, sin los ítems sin cotizar ni impuestos. Las fases 0 a 3, que
alcanzan para validar el diseño sin construir el dron, suman unos USD 887.
