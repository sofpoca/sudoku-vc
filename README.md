# Sudoku de Nubes

Un juego de Sudoku para escritorio, hecho con Python y pygame-ce, con una interfaz
en tonos pastel inspirada en la paleta de referencia.

## Requisitos

- Python 3.10 o superior
- pygame-ce 2.5 o superior

## Ejecutar

```powershell
py -m pip install -r requirements.txt
py main.py
```

Elige **Fácil**, **Intermedio** o **Difícil** para comenzar. Cada tablero se
genera con una solución única.

## Controles

- Haz clic en una casilla y escribe `1`–`9` para colocar un número.
- `Supr` o `Retroceso` borra una casilla editable.
- `N` activa o desactiva las notas; vuelve a pulsar un número para quitarlo.
- `H` o el botón **Dame una pista** revela la solución de la casilla seleccionada.
- Las flechas mueven la selección; `R` crea un tablero nuevo y `Esc` vuelve al menú.
- También puedes usar el teclado numérico para ingresar valores.

Las pistas originales no se pueden cambiar. Los errores se señalan en el tablero
y se cuentan; el juego celebra la victoria al completar correctamente la cuadrícula.

## Pruebas

```powershell
py -m unittest discover -s tests -v
```
