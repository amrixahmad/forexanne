
def send_signal(
        sl: str,
        tp1: str,
        tp2: str,
        tp3: str,
        max_tp: str,
        cl: str,
        buy: str="",
        sell: str=""):
    
    start_signal = "Follow signal:"
    signal_buy = f"\nBuy: {buy}"
    signal_sell = f"Sell: {sell}"
    base_signal = f'''                    
                    Stop Loss: {sl}
                    Take Profit: {tp1}
                    Take Profit: {tp2}
                    Take Profit: {tp3}
                    Max Take Profit: {max_tp}
                    Cut Loss: {cl}
                    
                    ✅Take care of money management
                    ✅Must layer with  gap for  3-5 pips
                    ✅Remember always close Early Layers
                    ✅If price goes deep you can still entry
                    ✅If price goes 10-15 pips can set BE
                    ✅Always Entry in the zone if Early
                '''
    
    if buy:
        return start_signal + signal_buy + base_signal
    if sell:
        return start_signal + signal_sell + base_signal
    
if __name__=="__main__":
    cmi_signal = send_signal(
        sl="2019.5",
        buy="2023-2021",
        tp1="2025",
        tp2="2025",
        tp3="2026",
        max_tp="2033",
        cl="2019"        
        )
    print(cmi_signal)