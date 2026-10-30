# Lista de materiales del prototipo

Compras por fase del plan "medir antes de construir", en la versión simplificada del 30/10/26:
banco con el sensor de agua (`cad/banco/`), cuerpo del aro en telgopor (`cad/cuerpo/`) y vuelo
atado. La IA a bordo queda para después. El paso a paso de cómo pedir y armar cada cosa está en
`docs/roadmap/gavia-roadmap-prototipo.pdf`.

Precios de MercadoLibre Argentina y de [TangoFPV](https://tangofpv.com/) consultados el 30/10/26,
pasados a dólares con el MEP de $1.568 ([DolarHoy](https://dolarhoy.com/)). Lo que viene de China no
incluye impuestos. Cambian rápido: revisalos antes de comprar.

MercadoLibre es la primera opción, por la compra protegida. Se compra afuera solo cuando ahorra mucho
o MercadoLibre no lo tiene: la batería y el receptor salen de TangoFPV (Córdoba). Lo que alguien del
equipo ya tenga (soldador, estaño, multímetro, sargentos, anteojos) no se compra, y eso ahorra
hasta unos $205.000 más.

## Antes de comprar

- Importados repartidos entre los tres. Las publicaciones de China avisan que se pueden recibir
  hasta 5 envíos internacionales por año por persona, sumando todas las plataformas. Si cada uno
  compra con su cuenta, usa su propio cupo, y el paquete llega a nombre y a la dirección de quien
  compra. Sugerencia: en la fase 1, motores (Lucho), ESC del banco y radio (Eli), wattímetro y
  cargador (Augus). En la fase 3, GPS y placa de distribución (Lucho), tres ESC (Eli) y controladora
  (Augus). Cada uno usa 3 de sus 5 envíos. Cómo cuenta MercadoLibre el límite (por compra o por
  paquete) está a validar.
- Motores. Ningún vendedor es tienda oficial. Preguntar por mensaje si son Hobbywing originales y
  cuántos trae el pack. El banco lo confirma: si el empuje medido se parece a la tabla, son buenos.
- Batería. La CNHL 6S 4000 pesa unos 650 g según la tienda y trae EC5, así que todo el proyecto
  usa EC5. Preguntarle a TangoFPV el costo y el tiempo del envío. Al recibirla se pesa y se
  actualiza `masa_bateria_kg` (el modelo supone 480 g).

## Fase 1: banco, con herramientas y sensor de agua (unos USD 665)

### Herramientas

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Soldador | Estación T12 G Tools 72 W | 95.101 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5129242865) |
| Estaño | Mechanic 63/37, 0,8 mm, 60 g, con flux | 10.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3765784628) |
| Multímetro | Uni-T UT33D+ | 20.900 | [ML](https://www.mercadolibre.com.ar/uni-t-multimetro-digital-compacto-ut33d/p/MLA22558626) |
| Cable | Silicona 12 AWG, 2 m rojo y 2 m negro (confirmar largo) | 29.900 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3256538588) |
| Termocontraíble | Kit de 560 piezas | 15.200 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5069989514) |
| Anteojos | Libus 900555, x3 | 10.340 | [ML](https://www.mercadolibre.com.ar/x/p/MLA24368245) |
| Tornillos | Kit Allen M3 y M4, 240 unidades (la celda puede pedir M5, a validar) | 26.999 | [ML](https://articulo.mercadolibre.com.ar/MLA-685085119) |
| | Subtotal | 208.940 | |

### Banco

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Motores | Hobbywing XRotor 2812 900KV, pack de 4 | 127.997 | China | [ML](https://www.mercadolibre.com.ar/hobbywing-xrotor-2812-900kv-motor-brushless-fpv-4-unidades/up/MLAU5301615561) |
| Hélices | Gemfan 8046-3, 3 packs de 2: uno para el banco y dos para el dron. Es la única hélice del proyecto y escasea | 148.503 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU2977712694) |
| ESC | EMAX BLHeli 60A, 2 a 6S | 53.168 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Batería | CNHL 6S 4000 mAh 65C con EC5, unos 650 g | 191.400 | TangoFPV (Córdoba) | [TangoFPV](https://tangofpv.com/producto/bateria-de-lipo-cnhl-4000mah-22-2v-6s-65c-ec5/) |
| Cargador | iMAX B6AC V3 con fuente incluida, 80 W, se enchufa a 220 V. Trae enchufe europeo: va con un adaptador | 111.021 | China | [ML](https://www.mercadolibre.com.ar/up/MLAU5676738851) |
| Adaptador | Enchufe europeo a patas argentinas | 6.756 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3059010977) |
| Medidor | Wattímetro 150 A (viene sin fichas) | 23.918 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2037161975) |
| Fichas | EC5, 4 pares ($5.990 el par) | 23.960 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3333023448) |
| Probador | Probador de LiPo de 1 a 8S con alarma | 5.597 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3325789537) |
| Celda | 10 kg con HX711 (la de 5 kg queda justa con el banco encima) | 16.795 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3419553238) |
| Placa | ESP32 USB-C, x2: una de repuesto que después va a la botonera | 31.980 | Local | [ML](https://www.mercadolibre.com.ar/nodemcu-esp32-wifi-bluetooth-42-iot-wroom-esp32s-usb-c/p/MLA2038887439) |
| Radio | Radiomaster Pocket ELRS. Se adelanta para practicar en un simulador en la PC, por USB | 201.977 | Internacional | [ML](https://www.mercadolibre.com.ar/p/MLA2075906042) |
| Pilas | Samsung 18650 30Q, x2, para la radio ($19.500 c/u) | 39.000 | Local | [ML](https://www.mercadolibre.com.ar/p/MLA16952001) |
| Bolsa | Ignífuga para LiPo, 29 x 23 cm | 37.991 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3258038031) |
| Ducto | Policarbonato 1 mm, 1,2 x 1,2 m. Alcanza para el banco y los cuatro liners del dron | 47.033 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU279911287) |
| Labio | Manguera cristal 3/4" (19 x 25 mm), 5 m. Hacen falta 70 cm: en ferretería sale menos | 25.000 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3268635007) |
| Prensas | Sargento Wadfow 300 mm, x2 | 22.800 | Local | [ML](https://www.mercadolibre.com.ar/x/p/MLA2086927338) |
| | Subtotal | 1.114.896 | | |

### Sensor de agua

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Sensor | Módulo LM393 con sonda de agua | 5.604 | [ML](https://www.mercadolibre.com.ar/x/p/MLA2071007363) |
| Electrodos | Varilla roscada inoxidable 316, 1/4" x 1 m | 13.750 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3820171820) |
| | Subtotal | 19.354 | |

Total de la fase 1: $1.343.190, unos USD 857, más el corte láser.

Falta el precio del corte láser del banco con material incluido (dos planchas de MDF de 5,5 mm y dos
discos de acrílico de 6 mm). Talleres y referencias en "Proveedores y servicios", al final. El
acrílico, el fenólico y las planchuelas de aluminio de la lista anterior ya no hacen falta: todo sale
del láser.

## Fase 2: cuerpo (unos USD 37, más el corte y la pileta)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Corte | Tres capas de EPS de 30 mm y 30 kg/m³ con material incluido (`cad/cuerpo/`) | a cotizar | |
| Pegamento | Novolastic para telgopor, x2 | 21.091 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU280100227) |
| Dinamómetro | Balanza colgante digital 50 kg | 20.500 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU4045801615) |
| Lastre | Unos 3 kg de discos de mancuerna de hierro o bolsas de tuercas, de casa. Si nadie tiene, [Cressi forrado 1 kg](https://www.mercadolibre.com.ar/x/up/MLAU297562071), $30.478 por dos | 0 | |
| Cajas | Caja de paso estanca IP65 Kalop (Unika) 120 x 170 x 75 mm, x2 ($8.011 c/u) | 16.022 | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3893576153) |
| | Subtotal | 57.613 | |

Talleres para el corte y referencias de la pileta en "Proveedores y servicios". Si el taller no pone
el material, son tres [planchas de EPS de 1 x 1 m, 30 mm y 30 kg/m³](https://www.mercadolibre.com.ar/p/MLA70281050),
a $14.187 cada una. En el país no encontramos cajas IP67 de menos de 90 mm de alto que sirvan, por
eso van las IP65 y se prueban 30 minutos a 1 m en la pileta.

## Fase 3: vuelo atado (unos USD 358, más el corte de las rejillas)

Controladora MicoAir743 con cuatro ESC sueltos: si se quema uno se cambia uno ($53.168) y no la
placa entera, y el del banco ya es el cuarto. Se confirma al terminar el banco. En MercadoLibre no
apareció un stack SpeedyBee F405 V4 original (ArduPilot lo soporta,
[docs](https://ardupilot.org/copter/docs/common-speedybeef4-v3.html)), solo uno "Marca Generic"
desde China a [$438.142](https://www.mercadolibre.com.ar/p/MLA2088323725). Si aparece uno de marca,
se puede elegir ese. Plan B de controladora: Matek H743-WING V3
([ArduPilot](https://ardupilot.org/copter/docs/common-matekh743-wing.html)), a
[$275.210](https://www.mercadolibre.com.ar/controlador-de-vuelo-inav-de-ala-fija-matek-h743-wing-v3/p/MLA2122662864).

| Ítem | Producto | ARS | Envío | Link |
|---|---|---|---|---|
| Controladora | MicoAir743, 2 a 6S, 10 salidas de motor y entrada de sensor de corriente ([ArduPilot](https://ardupilot.org/copter/docs/common-MicoAir743.html)) | 127.215 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2039430017) |
| ESC | EMAX BLHeli 60A, x3 más (máximo 3 por compra). El cuarto es el del banco | 159.504 | China | [ML](https://www.mercadolibre.com.ar/x/up/MLAU5508376270) |
| Distribución | Matek FCHUB-12S V2, con sensor de 440 A | 66.392 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2080086204) |
| GPS | MicoAir M10G-5883 | 69.906 | China | [ML](https://www.mercadolibre.com.ar/p/MLA2085469012) |
| Receptor | Radiomaster XR2 Nano ELRS 2,4 GHz | 43.065 | TangoFPV (Córdoba) | [TangoFPV](https://tangofpv.com/producto/radiomaster-xr2-nano-receptor-elrs-2-4ghz/) |
| Estructura | Caño redondo de aluminio de 12,7 x 1 mm, 3 tiras de 1 m ($9.832 c/u), para el cuadrado y los puentes de los motores | 29.496 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU213325382) |
| Buzzer | Activo 5 V, x5 | 6.519 | Local | [ML](https://www.mercadolibre.com.ar/up/MLAU3532054677) |
| Bloqueo | Relé biestable 5 V | 7.490 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU227966400) |
| Reset | Reed switch NA, x6 | 5.895 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU3856250498) |
| Imán | Neodimio 10 x 3 mm, x5 | 4.790 | Local | [ML](https://www.mercadolibre.com.ar/x/up/MLAU136862942) |
| Sellador | Poxipol 10 minutos, 14 ml, para los pasos de cables | 7.449 | Local | [ML](https://articulo.mercadolibre.com.ar/MLA-860672385) |
| Piel | Membrana líquida acrílica Polacrin, 4 L. Es al agua y no ataca el telgopor | 32.900 | Local | [ML](https://www.mercadolibre.com.ar/p/MLA26392325) |
| | Subtotal | 560.621 | | |

La telemetría va por el mismo enlace ELRS, sin radio aparte
([ExpressLRS](https://www.expresslrs.org/software/mavlink/)). El circuito del bloqueo por agua se
define con el umbral medido en la fase 1, así que esas tres piezas pueden cambiar.

El aluminio reemplaza al [tubo de carbono de 13 x 10 mm](https://www.mercadolibre.com.ar/up/MLAU4047653302)
($96.000 el metro) en el primer prototipo. Entra en el canal de 13,5 mm del cuerpo, pesa unos 100 g
por metro contra unos 84 g del carbono y es más blando (aprox., a validar). Si se golpea o se
agujerea mal, se dobla o se cambia por $9.832. Si el dron vibra, se pasa a carbono.

La radio y sus pilas pasaron a la fase 1. La piel de membrana alcanza para la pileta y el campo.
Para el mar: epoxi con tela de vidrio hecho por nosotros
([tela de 200 g](https://www.mercadolibre.com.ar/up/MLAU169656405), $21.978 el m², unos 2 m², y
[resina epoxi](https://articulo.mercadolibre.com.ar/MLA-1670706600), $58.626 el kg, unos $102.582 en
total, a validar que la resina sea de laminado) o un taller de tablas de surf. Nunca resina
poliéster, porque derrite el telgopor. Falta el precio del corte de las ocho rejillas del dron (mismo
archivo del banco): una [plancha de acrílico de 6 mm de 120 x 60](https://articulo.mercadolibre.com.ar/MLA-1919877273),
$116.600, da 10 discos, ocho y dos de repuesto. Los liners salen de la plancha de policarbonato de la
fase 1.

## Botonera (unos USD 54)

| Ítem | Producto | ARS | Link |
|---|---|---|---|
| Caja | Kalop IP65 de 170 x 120 x 75 mm, la misma de los drones (el modelo 3D pasa de 200 a 170 mm) | 8.045 | [ML](https://www.mercadolibre.com.ar/up/MLAU3866774031) |
| Botones | Pulsador de 30 mm tipo arcade, x2 (rojo y gris), $3.749 c/u. No son estancos: van bajo el techo de la torre | 7.498 | [ML](https://www.mercadolibre.com.ar/up/MLAU5020679137) |
| Pantalla | OLED 1,3" SH1106 I2C | 8.400 | [ML](https://www.mercadolibre.com.ar/up/MLAU245352701) |
| LED | Portaled metálico de 5 mm (a validar cuántos trae) | 23.751 | [ML](https://www.mercadolibre.com.ar/up/MLAU289137012) |
| Prensacables | PG7, pack de 20. Los que sobran van a las cajas del dron | 20.677 | [ML](https://articulo.mercadolibre.com.ar/MLA-2126012616) |
| Cable | USB-C de 3 m | 16.790 | [ML](https://articulo.mercadolibre.com.ar/MLA-2012191232) |
| | Subtotal | 85.161 | |

El ESP32 es el de repuesto del banco y el buzzer sale del pack de cinco de la fase 3. La ventana de
acrílico de 2 mm se pide como retazo al taller láser. Para la v2 conviene un pulsador estanco, por
ejemplo un [par de rasantes de 22 mm](https://articulo.mercadolibre.com.ar/MLA-2151149170) a $8.117.

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

Las fases 1 a 3 y la botonera suman unos $2.046.585, cerca de USD 1.305, sin impuestos ni los
servicios (corte láser, corte del telgopor, corte de las rejillas y pileta). Suma cosas que antes no
estaban cotizadas: botonera, piel, pilas, tornillos, manguera y adaptador. Con la misma lista de
antes, la revisión de gastos bajó de unos USD 1.507 a unos USD 1.163, y el primer plan daba unos
USD 2.012 con la IA a bordo incluida.

## Proveedores y servicios

| Qué | Dónde | Referencia | Qué preguntar |
|---|---|---|---|
| Corte láser del banco | Talleres en MercadoLibre: [Almirante Brown](https://servicio.mercadolibre.com.ar/MLA-3214912144-servicio-corte-laser-co2-mdf-acrilico-madera-goma-grabados-_JM), [zona oeste](https://articulo.mercadolibre.com.ar/MLA-3355709130) y [CABA](https://articulo.mercadolibre.com.ar/MLA-1805504129) | [Acrílico de 6 mm de 60 x 40](https://www.mercadolibre.com.ar/up/MLAU4421302558), $52.844 | El mensaje del roadmap, con material incluido |
| Rejillas del dron | El mismo taller | Acrílico de 6 mm de 120 x 60, $116.600, 10 discos | Las 8 juntas y un retazo de 2 mm para la botonera |
| Corte del telgopor | [Telgopor Quilmes](https://www.instagram.com/telgoporquilmes/), [Deletrearte](https://deletrearte.com.ar/Servicios/) y [RotulArte](https://rotularte.com.ar/producto/corte-cnc-por-hora-servicio-para-grafica-y-carteleria/) | CNC desde $61.440 la hora (RotulArte). EPS de 30 mm, $14.187 la plancha | El mensaje del roadmap. Plan B: [cortador de hilo caliente de mano](https://www.mercadolibre.com.ar/up/MLAU1131312175), $51.990, con la plantilla impresa |
| Pileta | Clubes de la zona, por ejemplo Pejerrey Club (Quilmes) | $12.500 la entrada para no socios y $2.500 de revisión médica (sin fecha, a validar). En CABA, Parque Norte cobraba $4.000 a $6.000 el pase diario en enero de 2026 ([Ámbito](https://www.ambito.com/economia/cuanto-sale-llevar-los-chicos-la-pileta-el-verano-2026-n6237449)) | Si es techada o climatizada y si dejan meter el aro con pesas una hora |
| Batería y receptor | [TangoFPV](https://tangofpv.com/) (Córdoba) | $191.400 y $43.065 | Costo y tiempo del envío |
| Piel para el mar | Talleres de tablas de surf (no encontramos uno con web, buscar "shaper" en Instagram o en Mar del Plata) | Hacerlo nosotros: unos $102.582 en materiales | Si laminan con epoxi sobre telgopor y cuánto sale un aro de 80 cm |
| Lo chico | Ferretería del barrio | Manguera, cola vinílica, cinta y tornillos sueltos | |

Para más adelante, la estación todo en uno de la v2 lleva una Raspberry Pi 5 de 8 GB ($431.308) con
el [kit de IA Hailo de 13 TOPS](https://www.mercadolibre.com.ar/p/MLA39649202) ($215.559). No se
compran ahora.

## Qué cambió para gastar menos

Revisión del 30/10/26: ¿hay algo igual de bueno y más barato? ¿Y qué pasa si lo rompemos?

| Qué | Antes | Ahora | Ahorro |
|---|---|---|---|
| Cargador | B6AC local, $219.990 | El mismo modelo (B6AC V3) importado, $111.021 | 108.969 |
| Batería | Pulse 6S 5200 80C, $270.000 | CNHL 6S 4000 65C en TangoFPV, $191.400, unos 650 g | 78.600 |
| Wattímetro | Local, $79.000 | Importado, $23.918 | 55.082 |
| Multímetro | Uni-T UT89XD, $37.900 | Uni-T UT33D+, $20.900 | 17.000 |
| Lastre | Cressi, $45.717 | Pesas de casa | 45.717 |
| Controladora | Matek H743-WING, $275.210 | MicoAir743, $127.215 | 147.995 |
| Receptor | Radiomaster RP3, $86.355 | Radiomaster XR2 en TangoFPV, $43.065 | 43.290 |
| Estructura | Tubo de carbono, $96.000 | Caño de aluminio, 3 m, $29.496 | 66.504 |
| Sumamos | | Probador de LiPo, ESP32 de repuesto y fichas EC5 | −23.484 |
| Total | $2.362.993 | $1.823.320 | 539.673 |

En lo que no se ahorra: las tres parejas de hélices (lo que más se rompe y casi no hay), la bolsa
ignífuga de 29 x 23 (la [más barata](https://www.mercadolibre.com.ar/up/MLAU5056940071) mide
13 x 18,5 cm y la batería no entra), el soldador T12 (uno barato no calienta una ficha de batería) y
la celda de 10 kg. En el roadmap, la página "Si se rompe o se quema algo" dice cómo evitar cada
rotura y cuánto sale reponerla.

## Si algo no está

Lo escaso se compra temprano. Lo que no hay no se persigue hasta que haga falta. Revisado el 30/10/26.

| Pieza | Qué puede pasar | Plan A | Plan B |
|---|---|---|---|
| Batería | En MercadoLibre hay una sola publicación local que sirve. TangoFPV tenía stock | CNHL 6S 4000 65C con EC5, $191.400, en la primera tanda | [Pulse 6S 5200 80C](https://www.mercadolibre.com.ar/x/up/MLAU5705660626), $270.000, o la [Ovonic 6S 5000 130C](https://www.mercadolibre.com.ar/up/MLAU4006221150), $459.124, importada |
| Cargador | El importado tarda unas tres semanas o llega fallado | B6AC V3 importado, $111.021 | [El mismo modelo local](https://www.mercadolibre.com.ar/up/MLAU132422334), $219.990 |
| Wattímetro | Lo mismo | Importado, $23.918 | [Local](https://www.mercadolibre.com.ar/x/up/MLAU3010886186), $79.000 |
| Hélices | Casi no hay de 8 pulgadas tripala de marca y tardan una semana | Los 3 packs de Gemfan 8046 juntos, en la fase 1 | Traer Gemfan o HQ 8x4.5x3 junto con los motores |
| Motores | El vendedor no es tienda oficial | Pack de 4 Hobbywing. La configuración a del banco dice si son originales | Devolverlos con la compra protegida y probar otro vendedor |
| Celda | Hay varias | 10 kg con HX711, $16.795 | [Otra igual](https://www.mercadolibre.com.ar/up/MLAU294756996), $16.479 |
| Controladora | No hay stack SpeedyBee original, solo genéricos | MicoAir743 con ESC sueltos, se confirma después del banco | Matek H743-WING (ver fase 3) |
| Receptor | TangoFPV se queda sin stock | Radiomaster XR2, $43.065 | [RP1](https://www.mercadolibre.com.ar/p/MLA2077209660) o [RP3](https://www.mercadolibre.com.ar/p/MLA2099353396) en MercadoLibre, unos $88.000 |
| Cajas | No hay IP67 de menos de 90 mm de alto | Kalop IP65 de 120 x 170 x 75 mm | Si no pasan la prueba de la pileta, otra caja y se regeneran las capas |
| Talleres | No publican precios | Pedir presupuesto a dos o tres de cada tipo apenas se arranca | Otro taller de la lista |

