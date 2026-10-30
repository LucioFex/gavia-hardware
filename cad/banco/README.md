# Banco de empuje de un ducto

Primera etapa del prototipo: un solo motor con su hélice de 8 pulgadas adentro de un ducto como
los del aro, para medir empuje, corriente y cuánto se pierde con las rejillas. La lista de
compras está en `../../bom/lista-de-materiales.md`.

## Qué se mide

Cinco configuraciones con el mismo motor y la misma hélice, cada una con un barrido de acelerador
del 30 al 100 %:

| | Configuración | Qué sale |
|---|---|---|
| a | Hélice libre, sin ducto | Empuje base, contra la tabla del fabricante |
| b | Ducto de canto vivo | Ganancia del ducto = b/a |
| c | Canto vivo con las dos rejillas | Pérdida de las rejillas = c/b |
| d | Ducto con labio redondeado | Ganancia del ducto con labio = d/a |
| e | Labio con las dos rejillas | Pérdida de las rejillas con labio = e/d |

Los resultados reemplazan `kg_por_motor`, `k_ducto` y `k_rejilla` en `../blender/gavia_aro.py`.
Si el empuje/peso que sale da 2 o más, se sigue con ese motor.

## Archivos

| Archivo | Qué es |
|---|---|
| `rejilla_banco.py` | Genera la rejilla en 2D a partir de los parámetros de `../blender/gavia_aro.py` |
| `rejilla_banco.svg`, `rejilla_banco.dxf` | La rejilla para corte láser, en mm. Hacen falta dos |

```
python rejilla_banco.py
```

## Medidas

- Rejilla: disco de 212,6 mm en acrílico de 6 mm, flejes de 2 mm, ranura de 5 mm, cinco nervios
  de 2,6 mm y un aro de 4 mm. Entra en el ducto con 0,3 mm de juego por lado. Las ranuras más
  chicas que 15 mm² contra el aro quedan llenas.
- Ducto: tira de policarbonato de 1 mm de 90 por 693 mm, enrollada a 213,2 mm de diámetro
  interior, con 20 mm de solape pegado. Deja 5 mm de holgura en la punta de la hélice, como el aro.
- Labio (configuraciones d y e): manguera de unos 20 mm cortada a lo largo y calzada en el borde
  de entrada.

## Armado

El motor va en una planchuela de aluminio que cruza el ducto a la altura de la hélice, atornillada
a dos planchuelas verticales por fuera del ducto que bajan a la placa apoyada en la celda de carga.
La hélice sopla hacia arriba. El ducto y las rejillas van del lado que pesa la celda, porque si no
la ganancia del ducto y la pérdida de las rejillas no se ven en la medida.

## Seguridad

Una hélice de 8 pulgadas en 6S corta. El banco va atornillado a una mesa pesada, nadie se para en
el plano de la hélice, el ESP32 corta solo a los 10 s de cada paso, y la batería se carga y se
guarda en bolsa ignífuga.
