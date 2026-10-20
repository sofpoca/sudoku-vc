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

## Desarrollo con IA: prompts e iteraciones

### Prompt 1: lógica y generación de tableros

**CONTEXTO:** Eres un desarrollador experto en Python y lógica de Sudoku. El
proyecto es un juego de escritorio creado con pygame-ce.

**INSTRUCCIÓN:** Implementa la lógica para generar tableros de Sudoku en los
niveles fácil, intermedio y difícil. Cada tablero debe tener una solución válida
y única. Incluye las operaciones necesarias para colocar y borrar valores,
proteger las pistas iniciales, detectar errores y completar el tablero.

**FORMATO:** Integra la solución en los módulos existentes, separando la lógica
del tablero de la interfaz. Incluye pruebas automatizadas para las reglas
principales.

**RESTRICCIONES:** Usa Python 3.10 o superior y no dependas de servicios externos.
No permitas modificar las pistas iniciales ni aceptar niveles desconocidos como
si fueran válidos.

**Qué se pidió y por qué se refinó:** Se pidió construir la base funcional del
Sudoku. Se precisaron la unicidad de la solución, las reglas del tablero y los
casos inválidos para que “generar un Sudoku” tuviera criterios comprobables.

### Prompt 2: interfaz del juego

**CONTEXTO:** El juego debe ser accesible desde una ventana de escritorio y
mantener una presentación amable, clara y coherente con una paleta de colores
pastel.

**INSTRUCCIÓN:** Crea una interfaz con un menú para elegir la dificultad y una
pantalla de partida que muestre la cuadrícula, el nivel y controles fáciles de
identificar. Resalta la casilla seleccionada y los conflictos, y muestra el
progreso de la partida.

**FORMATO:** Implementa las pantallas y sus elementos con pygame-ce; conserva
los textos de la interfaz en español y añade las instrucciones de uso al README.

**RESTRICCIONES:** Mantén visibles la cuadrícula y los controles en la ventana.
La interfaz debe permitir jugar tanto con el ratón como con el teclado.

**Qué se pidió y por qué se refinó:** Se pidió presentar el juego de forma
usable y atractiva. Se especificaron las pantallas, los elementos y los medios
de interacción para convertir una petición visual general en comportamientos
concretos.

### Prompt 3: controles, ayudas y validación

**CONTEXTO:** La lógica del Sudoku ya permite jugar una partida y la interfaz
cuenta con una cuadrícula seleccionable.

**INSTRUCCIÓN:** Añade notas para las casillas, una pista para revelar el valor
correcto de la casilla seleccionada, un contador de errores y una señal de
victoria al resolver el tablero. Permite iniciar otro tablero y volver al menú.

**FORMATO:** Integra los controles en pantalla y los atajos de teclado. Añade o
ajusta pruebas para comprobar las acciones principales del tablero.

**RESTRICCIONES:** Las pistas originales deben seguir protegidas. Las notas no
deben contar como respuestas y las ayudas deben actuar sobre la casilla
seleccionada.

**Qué se pidió y por qué se refinó:** Se pidió mejorar la experiencia de juego
con ayudas y más controles. Se detalló cómo debía comportarse cada función para
evitar que la mejora visual o de interacción afectara las reglas del Sudoku.

### Iteración y mejora
**Qué se pidió y por qué se refinó:** Se pidió mejorar la experincia del usuario ajustando
iconos y recuadros dentro de la visualizacion del juego, ya que aparecian en desorden.

**Antes**
<img width="430" height="702" alt="Screenshot 2026-10-19 235415" src="https://github.com/user-attachments/assets/eda725c9-71bd-4e27-81f4-8c811cd25ab5" />
**Despues**
<img width="437" height="707" alt="image" src="https://github.com/user-attachments/assets/7d1cbe79-19ae-4a64-a341-0aee7ee02973" />


### Validación y limitaciones

Se ejecutaron las pruebas automatizadas con `py -m unittest discover -s tests -v`.
Las cinco pruebas pasaron; verifican la solución única en los tres niveles,
la validez de la solución, las pistas protegidas, las notas, las pistas de ayuda,
el conteo de errores y el rechazo de niveles desconocidos.

Las pruebas automatizadas comprueban la lógica, pero no automatizan la
presentación ni todos los eventos de pygame. Para revisar manualmente la
interacción, ejecuta el juego y prueba las dificultades, la selección de
casillas, la entrada y el borrado de números, las notas, las pistas y el retorno
al menú.

### Reflexión final

Al desarrollar este juego aprendí a dividir un problema en partes: generación
del tablero, reglas de Sudoku, controles e interfaz. La IA puede acelerar la
creación de una primera versión y ayudar a explorar mejoras, pero sus resultados
deben revisarse y probarse para confirmar que cumplen las reglas del juego. Comprendo el flujo general de una partida
y las operaciones del tablero; aunque hay caracteristicas de la libreria Pygame utilizada que aún desconozco.
