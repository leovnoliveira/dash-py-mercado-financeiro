import MetaTrader5 as mt5

if not mt5.initialize():
    print("Falha ao inicializar MetaTrader5, erro:", mt5.last_error())
else:
    print("MetaTrader5 inicializado com sucesso!")

# Testa se consegue acessar informações da conta
account_info = mt5.account_info()
if account_info is None:
    print("Erro ao acessar informações da conta:", mt5.last_error())
else:
    print("Conta conectada com sucesso:", account_info)
