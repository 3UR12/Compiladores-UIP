"""Analizador léxico del lenguaje educativo MiniUIP.

Python 3.10 o superior. No requiere librerías externas.
Uso: py lexer.py [archivo.min]
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys


PALABRAS_RESERVADAS = {
    "entero", "decimal", "cadena", "si", "sino",
    "mientras", "imprimir", "verdadero", "falso",
}

# Los operadores compuestos van antes que los de un carácter.
REGLAS = [
    ("COMENTARIO", r"//[^\n]*"),
    ("CADENA", r'"(?:\\["\\nrt]|[^"\\\n])*"'),
    ("NUMERO", r"\d+(?:\.\d+)?"),
    ("OPERADOR", r"==|!=|<=|>=|&&|\|\||\*\*|[+\-*/%=<>!]"),
    ("DELIMITADOR", r"[(){};,]"),
    ("IDENTIFICADOR", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("SALTO", r"\n"),
    ("ESPACIO", r"[ \t\r]+"),
    ("ERROR", r"."),
]

PATRON = re.compile("|".join(
    f"(?P<{nombre}>{expresion})" for nombre, expresion in REGLAS
))


@dataclass(frozen=True)
class Token:
    tipo: str
    lexema: str
    linea: int
    columna: int


class ErrorLexico(ValueError):
    """Error al encontrar un carácter no reconocido."""


def analizar(codigo: str) -> list[Token]:
    """Devuelve los tokens del código o informa el primer error léxico."""
    tokens: list[Token] = []
    linea, columna = 1, 1

    for coincidencia in PATRON.finditer(codigo):
        tipo = coincidencia.lastgroup
        lexema = coincidencia.group()

        if tipo == "SALTO":
            linea += 1
            columna = 1
            continue

        if tipo in {"ESPACIO", "COMENTARIO"}:
            columna += len(lexema)
            continue

        if tipo == "ERROR":
            raise ErrorLexico(
                f"Carácter no reconocido {lexema!r} en línea {linea}, columna {columna}"
            )

        if tipo == "IDENTIFICADOR" and lexema in PALABRAS_RESERVADAS:
            tipo = "RESERVADA"

        tokens.append(Token(tipo, lexema, linea, columna))
        columna += len(lexema)

    return tokens


def main() -> int:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ejemplo.min")

    try:
        codigo = ruta.read_text(encoding="utf-8")
        tokens = analizar(codigo)
    except (OSError, UnicodeError, ErrorLexico) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Archivo analizado: {ruta.name}")
    print(f"{'LÍNEA':<8}{'COLUMNA':<10}{'TIPO':<17}LEXEMA")
    print("-" * 59)
    for token in tokens:
        print(f"{token.linea:<8}{token.columna:<10}{token.tipo:<17}{token.lexema}")
    print(f"Total de tokens: {len(tokens)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
