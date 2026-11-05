# Taller 02 - Analizador léxico MiniUIP

Universidad Interamericana de Panamá  
Materia: Compiladores  
Estudiante: Euris Rodríguez  
Cédula: 8-1013-2315  
Profesor: Ricardo Wong

## Archivos

- `lexer.py`: reglas, análisis léxico y ejecución por consola.
- `test_lexer.py`: diez pruebas de la guía y una prueba de la extensión.
- `ejemplo.min`: código de entrada válido.
- `ejemplo_error.min`: código con el carácter `@` en la segunda línea.
- `ejemplo_potencia.min`: entrada para comprobar el operador `**`.
- `evidencias/`: capturas E01 a E06.

## Ejecución

Python 3.10 o superior. No requiere instalar paquetes.

Desde la carpeta del proyecto, ejecutar:

```powershell
py --version
py lexer.py
py lexer.py ejemplo_error.min
py -m unittest -v
py lexer.py ejemplo_potencia.min
```

En Windows también puede usarse `python` en lugar de `py`.

Resultados del ejemplo principal: 27 tokens. El archivo de error debe indicar línea 2, columna 10. La suite contiene 11 pruebas y debe finalizar con `OK`. El ejemplo de potencia identifica `**` como un solo operador.

## Cambio realizado

Se añadió el operador `**` antes de `*` en la expresión regular `OPERADOR`. Así, `2 ** 3` se divide en tres tokens: `NUMERO`, `OPERADOR` y `NUMERO`. La prueba `test_extension_operador_potencia` verifica el lexema y su ubicación.

En la prueba de posición se incluyeron dos espacios al principio de la segunda línea, para que el identificador empiece en columna 3, como indica la guía. No fue necesario modificar el cálculo de posiciones del analizador.

## Preguntas de reflexión

**¿Por qué enteroide no es una palabra reservada?**  
Se reconocen como reservadas únicamente las palabras que coinciden exactamente con una de las entradas de `PALABRAS_RESERVADAS`. `enteroide` no está en ese conjunto.

**¿Por qué el analizador no comprueba si edad fue declarada?**  
El Lexer solo reconoce secuencias de caracteres. Comprobar declaraciones corresponde al análisis semántico.

**¿Qué ocurre si > se evalúa antes que >=?**  
La expresión regular podría dividir `>=` en dos operadores. Por eso se reconocen primero los operadores compuestos.

**¿En qué se diferencia un error léxico de uno sintáctico?**  
Un símbolo como `@` fuera de una cadena no pertenece al vocabulario del lenguaje. La ausencia de `;` afecta la estructura de la instrucción, que debe revisar el analizador sintáctico.

**¿Qué se necesita para admitir comentarios multilínea?**  
Una regla para `/* ... */`, el conteo de saltos de línea dentro del comentario y un diagnóstico cuando no tenga cierre.
