import MetaTrader5 as mt5


mt5.symbol_select("IVVB11", True)  # Exemplo
info = mt5.symbol_select("IVVB11")
if info is None:
    print("Ainda não foi encontrado")
else:
    print("Sim, foi encontrado")
