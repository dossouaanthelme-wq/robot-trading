import MetaTrader5 as mt5
import time

# Connexion Exness
COMPTE = 298228767
PASSWORD = "TON_MOT_DE_PASSE" 
SERVEUR = "Exness-MT5Trial9"

if not mt5.initialize(login=COMPTE, password=PASSWORD, server=SERVEUR):
    print("Échec de connexion")
    quit()

paires = ["BTCUSDm", "USDJPYm"]

def executer_achat_securise(symbole):
    tick = mt5.symbol_info_tick(symbole)
    if tick is None: return
    prix_achat = tick.ask
    
    # Correction pour éviter "Invalid stops" (Photo d83dbeca)
    if "JPY" in symbole:
        tp = prix_achat + 0.300
        sl = prix_achat - 0.200
    else:
        tp = prix_achat + 500
        sl = prix_achat - 300

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbole,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_BUY,
        "price": prix_achat,
        "sl": round(sl, 3), # Arrondi pour le Forex
        "tp": round(tp, 3),
        "magic": 200,
        "comment": "Robot Joie Lumineuse",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    resultat = mt5.order_send(request)
    if resultat.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ ACHAT RÉUSSI sur {symbole}")
    else:
        print(f"❌ Erreur : {resultat.comment}")

while True:
    for p in paires:
        rates = mt5.copy_rates_from_pos(p, mt5.TIMEFRAME_H1, 0, 55)
        if rates is None or len(rates) < 50: continue
        clotures = [x['close'] for x in rates]
        sma5 = sum(clotures[-5:]) / 5
        sma50 = sum(clotures[-50:]) / 50
        if sma5 > sma50:
            executer_achat_securise(p)
            time.sleep(10)
    time.sleep(60)