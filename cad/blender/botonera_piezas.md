# Botonera del guardavidas: piezas

Lista de piezas del modelo `gavia_botonera.py`. Todas se compran hechas, no hace falta impresora
3D. Las medidas son de piezas comerciales típicas (aprox., a validar con la pieza en mano). Precios de
MercadoLibre del 30/10/26: unos $85.161 en total.

![La botonera](../../docs/renders/gavia_botonera_1_tres_cuartos.jpg)

| Pieza | Qué comprar | Medida usada en el modelo | Precio |
|---|---|---|---|
| Caja | [Kalop IP65 de 170 x 120 x 75 mm](https://www.mercadolibre.com.ar/up/MLAU3866774031), la misma de los drones | El modelo usa 200 x 120 x 75 mm y pasa a 170 mm (pendiente) | $8.045 |
| Botón INCIDENTE REAL | [Pulsador de 30 mm tipo arcade](https://www.mercadolibre.com.ar/up/MLAU5020679137), rojo | agujero de 30 mm | $3.749 |
| Botón FALSO POSITIVO | El mismo, gris o blanco | agujero de 30 mm | $3.749 |
| Aro protector | El bisel del pulsador arcade hace de aro | 44 mm de diámetro, 9 mm de alto | incluido |
| Pantalla | [OLED 1,3" SH1106 I2C](https://www.mercadolibre.com.ar/up/MLAU245352701) | ventana de 40 x 24 mm | $8.400 |
| Placa | ESP32 USB-C, el de repuesto del banco | | ya comprado en la fase 1 |
| LED de estado | [Portaled metálico de 5 mm](https://www.mercadolibre.com.ar/up/MLAU289137012) (a validar cuántos trae) | agujero de 8 mm | $23.751 |
| Buzzer | Uno del pack de cinco de la fase 3 | agujero de 4 mm | ya comprado |
| Prensacable | [PG7, pack de 20](https://articulo.mercadolibre.com.ar/MLA-2126012616); los que sobran van a las cajas del dron | agujero de unos 12,5 mm | $20.677 |
| Cable | [USB-C de 3 m](https://articulo.mercadolibre.com.ar/MLA-2012191232) | 4 mm de diámetro | $16.790 |
| Ventana | Acrílico transparente de 2 mm, un retazo que se pide al taller láser | 44 x 28 mm, pegado por dentro | con el corte |
| Fijación | Tornillos para madera de 4 mm, de ferretería | dos, por las orejas | |

Los pulsadores arcade no son estancos: en la v1 la botonera va bajo el techo de la torre. Para la v2
conviene un pulsador estanco, por ejemplo un
[par de rasantes de 22 mm](https://articulo.mercadolibre.com.ar/MLA-2151149170) a $8.117.

## Cómo se arma

1. Se marcan y se hacen los agujeros en la tapa: dos de 30 mm para los botones, la ventana de
   40 x 24 mm, uno de 8 mm para el LED y uno de 4 mm para el buzzer. Una mecha copa de 30 mm
   resuelve los botones.
2. Se pega el acrílico por dentro de la ventana con silicona neutra y la pantalla detrás.
3. Se montan los botones con su aro protector y se cablean al ESP32 junto con la pantalla, el LED
   y el buzzer.
4. El cable USB-C entra por el prensacable del costado. Alimenta la botonera y lleva los mensajes a
   la laptop, así que no hay pila adentro.
5. Los rótulos INCIDENTE REAL, FALSO POSITIVO y la palabra Gavia van grabados y rellenos con tinta
   carbón. Si no hay grabado a mano, sirve una etiqueta de vinilo de corte.
6. Se atornilla al poste del puesto por las dos orejas, con el prensacable hacia abajo o al
   costado, para que el agua no entre por ahí.

## Dudas abiertas

- El rojo y el gris de los botones, y si el aro protector va en carbón, se definen con Elías.
- Si la caja comercial viene en gris claro y no en crema, se pinta la tapa o se le pone una placa
  de acrílico crema cortada en láser con los agujeros y los rótulos.
- Los pulsadores de 30 mm con contacto atornillado suelen pedir de 40 a 50 mm de fondo detrás de la
  tapa (aprox., a validar). La caja de 75 mm alcanza.
