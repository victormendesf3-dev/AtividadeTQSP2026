def calcular_desconto(valor: float) -> float:
    """Aplica 10% de desconto para compras a partir de R$ 100,00."""
    if valor < 0:
        raise ValueError("Valor não pode ser negativo")
    if valor >= 100:
        return round(valor * 0.9, 2)
    return round(valor, 2)


def calcular_frete(valor_pedido: float, distancia_km: float) -> float:
    """Calcula frete grátis a partir de R$ 200,00 ou R$ 10 + R$ 1,50/km."""
    if valor_pedido < 0:
        raise ValueError("Valor do pedido não pode ser negativo")
    if distancia_km < 0:
        raise ValueError("Distância não pode ser negativa")
    if valor_pedido >= 200:
        return 0.0
    return round(10.0 + distancia_km * 1.5, 2)
