import unittest
from lexer import analizar, ErrorLexico


class PruebasAnalizadorLexico(unittest.TestCase):
    def test_palabras_reservadas(self):
        tokens = analizar("entero edad = 21;")
        self.assertEqual(
            [t.tipo for t in tokens],
            ["RESERVADA", "IDENTIFICADOR", "OPERADOR", "NUMERO", "DELIMITADOR"],
        )

    def test_numero_decimal(self):
        self.assertEqual(analizar("92.5")[0].lexema, "92.5")

    def test_operador_dos_caracteres(self):
        self.assertEqual(analizar("x >= 18")[1].lexema, ">=")

    def test_ubicacion_linea_y_columna(self):
        # Dos espacios antes de 'imprimir': comienza en columna 3.
        token = analizar("entero x;\n  imprimir(x);")[3]
        self.assertEqual((token.linea, token.columna, token.lexema), (2, 3, "imprimir"))

    def test_comentarios_no_generan_tokens(self):
        self.assertEqual(len(analizar("// comentario\nentero x;")), 3)

    def test_cadena_texto(self):
        self.assertEqual(analizar('imprimir("Hola");')[2].tipo, "CADENA")

    def test_simbolo_invalido(self):
        with self.assertRaisesRegex(ErrorLexico, "línea 2, columna 10"):
            analizar("entero x;\nimprimir(@x);")

    def test_entrada_vacia(self):
        self.assertEqual(analizar(""), [])

    def test_identificador_no_reservado(self):
        self.assertEqual(analizar("enteroide")[0].tipo, "IDENTIFICADOR")

    def test_cadena_sin_cerrar(self):
        with self.assertRaises(ErrorLexico):
            analizar('imprimir("incompleta);')

    def test_extension_operador_potencia(self):
        tokens = analizar("2 ** 3")
        self.assertEqual([t.tipo for t in tokens], ["NUMERO", "OPERADOR", "NUMERO"])
        self.assertEqual(tokens[1].lexema, "**")
        self.assertEqual((tokens[1].linea, tokens[1].columna), (1, 3))


if __name__ == "__main__":
    unittest.main()
