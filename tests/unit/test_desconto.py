import pytest

from src.desconto import calcular_desconto, calcular_frete


def test_aplica_10_por_cento_acima_de_100():
    # Arrange
    valor = 200.0

    # Act
    resultado = calcular_desconto(valor)

    # Assert
    assert resultado == 180.0


# ---------------------------------------------------------------------------
# calcular_desconto - Análise de Valor Limite / Classes de Equivalência
# Classes: [0, 100) sem desconto | [100, +inf) com 10% | (-inf, 0) inválida
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor, esperado",
    [
        (0, 0.0),           # limite inferior válido
        (99.99, 99.99),     # imediatamente abaixo do limite de desconto
        (100.0, 90.0),      # exatamente no limite: já recebe desconto
        (200.0, 180.0),     # classe com desconto
    ],
)
def test_calcular_desconto_valores_de_borda(valor, esperado):
    # Arrange (valores vêm do parametrize)

    # Act
    resultado = calcular_desconto(valor)

    # Assert
    assert resultado == esperado


@pytest.mark.parametrize("valor", [-0.01, -1, -100.0])
def test_calcular_desconto_valor_negativo_lanca_erro(valor):
    # Arrange (valor negativo vem do parametrize)

    # Act / Assert
    with pytest.raises(ValueError, match="Valor não pode ser negativo"):
        calcular_desconto(valor)


# ---------------------------------------------------------------------------
# calcular_frete
# Classes: valor >= 200 frete grátis | valor < 200 -> 10 + 1,50/km
#          valor negativo ou distância negativa -> ValueError
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor_pedido, distancia_km",
    [
        (200.0, 0),       # exatamente no limite do frete grátis
        (200.0, 50),      # limite, distância não importa
        (500.0, 100),     # classe frete grátis
    ],
)
def test_calcular_frete_gratis_a_partir_de_200(valor_pedido, distancia_km):
    # Arrange (valores vêm do parametrize)

    # Act
    resultado = calcular_frete(valor_pedido, distancia_km)

    # Assert
    assert resultado == 0.0


@pytest.mark.parametrize(
    "valor_pedido, distancia_km, esperado",
    [
        (0, 0, 10.0),           # limite inferior: só a taxa fixa
        (199.99, 0, 10.0),      # imediatamente abaixo do frete grátis
        (199.99, 10, 25.0),     # 10 + 10 * 1,50
        (100.0, 3.5, 15.25),    # distância fracionada
    ],
)
def test_calcular_frete_abaixo_de_200_cobra_por_distancia(
    valor_pedido, distancia_km, esperado
):
    # Arrange (valores vêm do parametrize)

    # Act
    resultado = calcular_frete(valor_pedido, distancia_km)

    # Assert
    assert resultado == esperado


def test_calcular_frete_valor_pedido_negativo_lanca_erro():
    # Arrange
    valor_pedido = -0.01
    distancia_km = 10

    # Act / Assert
    with pytest.raises(ValueError, match="Valor do pedido não pode ser negativo"):
        calcular_frete(valor_pedido, distancia_km)


def test_calcular_frete_distancia_negativa_lanca_erro():
    # Arrange
    valor_pedido = 100.0
    distancia_km = -0.1

    # Act / Assert
    with pytest.raises(ValueError, match="Distância não pode ser negativa"):
        calcular_frete(valor_pedido, distancia_km)
