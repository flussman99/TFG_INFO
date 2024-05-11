import Rsi_Macd, MediaMovil,time,Bandas_Bollinger,Estocastico
import datetime as date
import MetaTrader5 as mt5
import pandas as pd
from EquiposdeFutbol import SBS_backtesting as SBS
from Formula1 import SF1_backtesting as F1
import schedule
import time
from datetime import timedelta
# from Disney import Disney_backtesting as Disney



# Global variables
THRESHOLD = 20
MARGIN = 10
TIME_BETWEEN_OPERATIONS = 15*60*10
STOPLOSS = 100.0
TAKEPROFIT = 100.0
compras = []

FRAMETICKS = pd.DataFrame(columns=['Accion', 'Orden', 'Fecha', 'Precio', 'Decision', 'Rentabilidad'])
HAYPOSICIONESABIERTAS=False
TIMEBTWOPERATIONS = timedelta(minutes=15)
MERCADOCERRADO=False

def handle_buy(buy, market):#modificar compra
    """Function to handle a buy operation.

    Args:
        buy : Buy operation.
        market (str): Market where the operation was openned.
    """
    position=mt5.positions_get(symbol=market)[-1].ticket
    point = mt5.symbol_info(market).point
    ticket=buy.order#aqui tenemos el ticket
    GOAL = buy['price']+point*THRESHOLD
    while True:
        tick = mt5.symbol_info_tick(market)
        if tick.ask >= GOAL:
            # Modifying the stop loss
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": market,
                "sl": tick.ask - MARGIN * point,
                "tp": tick.ask + MARGIN * point,
                "deviation": 20,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                "position": position
            }
            GOAL = tick.ask + 1 * point
            mt5.order_send(request)
        # We check if the operation has been closed in order to leave the function
        if len(mt5.positions_get(ticket=position)) == 0:
            return
        time.sleep(0.1)


def handle_sell(sell, market: str):#modificar venta
    """Function to handle a sell operation.

    Args:
        sell : Sell operation.
        market (str): Market where the operation was openned.
    """
    position=mt5.positions_get(symbol=market)[-1].ticket # esta funcion te devuelve una lista de las posiciones abiertas
    #como solo quiero una pongo la -1 porque solo tengo una posicion abierta
    point = mt5.symbol_info(market).point
    GOAL = sell['price']-point*THRESHOLD #trailing stop
    while True:
        tick = mt5.symbol_info_tick(market)
        if tick.bid <= GOAL:
            # Modifying the stop loss
            #
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": market,
                "sl": tick.bid + MARGIN * point,
                "tp": tick.bid - MARGIN * point,
                "deviation": 20,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                "position": position # el toicket que quiero modificar
            }
            GOAL = tick.bid - 1 * point
            mt5.order_send(request)
        # We check if the operation has been closed in order to leave the function
        if len(mt5.positions_get(ticket=position)) == 0:
            return
        time.sleep(0.1)



def open_buy(trading_data: dict):
    """Function to open a buy operation.

    Args:
        trading_data (dict): Dictionary with all the needed data.

    Returns:
        A buy.
    """
    symbol_info = mt5.symbol_info(trading_data['market'])
    if symbol_info is None:
        print("[Thread - orders]", trading_data['market'], "not found, can not call order_check()")
        return None
    
    counter = 0

    # We only open the operation if the spread is 0
    # we check the spread 300000 times
    #nuestro margen de spread es del 0.5% por eso esta puesto el 0.005 ademas counter solo mirara 1 minuto los sprea sino no hago la operacion

    spread= symbol_info.ask- symbol_info.bid

    while (spread / symbol_info.ask) > 0.005:        
        if counter<60:
            counter += 1
            symbol_info = mt5.symbol_info(trading_data['market'])
        else:
            now = date.datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            print("[Thread - orders]", dt_string, "- Spread too high. Spread =", spread)
            print(symbol_info.ask)    
            print(symbol_info.bid)    

            return None
        


    point = mt5.symbol_info(trading_data['market']).point
    price = mt5.symbol_info_tick(trading_data['market']).ask #para la compra

    account_info = mt5.account_info()

    if account_info is None:
        print("[Thread - orders] Failed to get account info.")
        return None

    # Calcular el costo estimado de la operación de compra
    cost = price * trading_data['lotage']

    # Verificar si tienes suficiente dinero en la cuenta
    if account_info.balance < cost:
        print("[Thread - orders] Not enough money in the wallet to open the buy position.")
        return None
    

    deviation = 20

    #trading_data['lotage'],
    buy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": trading_data['market'],
        "volume": float(trading_data['lotage']),
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": float(price - price* 0.025),
        "tp": float(price + price*0.01),
        "deviation": deviation, #no sabemos q es
        "magic": 234000,#no sabemos q es
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the buy
    print(buy)
    result=mt5.order_send(buy)
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
    #print(result)

    print("[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(trading_data['market'],trading_data['lotage'],price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("[Thread - orders] Failed buy: retcode={}".format(result.retcode))
        return None
    return result


def open_sell(trading_data: dict):
    """Function to open a sell operation.

    Args:
        trading_data (dict): Dictionary with all the needed data.

    Returns:
        A sell.
    """
    symbol_info = mt5.symbol_info(trading_data['market'])
    if symbol_info is None:
        print("[Thread - orders]", trading_data['market'], "not found, can not call order_check()")
    
        return None
    
    counter = 0

    spread= symbol_info.ask- symbol_info.bid

    while (spread / symbol_info.ask) > 0.005:        
        if counter<60:
            counter += 1
            symbol_info = mt5.symbol_info(trading_data['market'])
        else:
            now = date.datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            print("[Thread - orders]", dt_string, "- Spread too high. Spread =", spread)
            print(symbol_info.ask)    
            print(symbol_info.bid)    

            return None
    # si el símbolo no está disponible en MarketWatch, lo añadimos
    if not symbol_info.visible:
        print("[Thread - orders]", trading_data['market'], "is not visible, trying to switch on")
        if not mt5.symbol_select(trading_data['market'], True):
            print("[Thread - orders] symbol_select({}) failed, exit",trading_data['market'])
            return None
    
    point = mt5.symbol_info(trading_data['market']).point
    price = mt5.symbol_info_tick(trading_data['market']).bid
    deviation = 20
    sell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": trading_data['market'],
        "volume": float(trading_data['lotage']),
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + STOPLOSS * point,
        "tp": price - TAKEPROFIT * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the sell
    result = mt5.order_send(sell)

    print("[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(trading_data['market'],trading_data['lotage'],price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("[Thread - orders] failed sell: {}".format(result.retcode))
        return None
    return sell


def check_buy(nombre:str) -> bool:
    """Function to check if we can open a buy.

    Returns:
        bool: True if we can, false if not.
    """
    if nombre == 'RSI':
        return Rsi_Macd.check_buy()
    elif nombre == 'Media Movil':
        return MediaMovil.check_buy()
    elif nombre == 'Bandas':
        return Bandas_Bollinger.check_buy()
    elif nombre == 'Estocastico':
        return Estocastico.check_buy()
    elif nombre == 'Futbol':
        return SBS.check_buy()
    elif nombre == 'Formula1':
        return F1.check_buy()
    # elif nombre == 'Disney':
    #     return Disney.check_buy()


def check_sell(nombre : str) -> bool:
    """Function to check if we can open a sell"""

    if nombre == 'RSI':
        return Rsi_Macd.check_sell()
    elif nombre == 'Media Movil':
        return MediaMovil.check_sell()
    elif nombre == 'Bandas':
        return Bandas_Bollinger.check_sell()
    elif nombre == 'Estocastico':
        return Estocastico.check_sell()
    elif nombre == 'Futbol':
        return SBS.check_sell()
    elif nombre == 'Formula1':
        return F1.check_sell()
    # elif nombre == 'Disney':
    #     return Disney.check_sell()
    

def cerrar_posicion(orders: dict):
    """Esta función cierra la posición que recibe como argumento"""
    print(orders)
    price=mt5.symbol_info_tick(orders.symbol).bid

    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'position': orders.ticket,
        'magic': orders.magic,
        'symbol': orders.symbol,
        'volume': orders.volume,
        "price": price,
        'deviation': 20,
        'type': mt5.ORDER_TYPE_SELL,
        'type_filling': mt5.ORDER_FILLING_IOC,
        'type_time': mt5.ORDER_TIME_GTC,
        'comment': "cerrar"
    }
    return mt5.order_send(request)
def cerrar_todas_las_posiciones(trading_data):
    """Esta función cierra TODAS las posiciones abiertas y gestiona posibles errores"""
    
    results = []
    orders = mt5.positions_get(symbol=trading_data['market'])
    for position in orders:
        result = cerrar_posicion(position)
        print("venta")
        print(result)
        results.append(result)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Posición {position.ticket} cerrada correctamente.")
        else:
            print(f"Ha ocurrido un error al cerrar la posición {position.ticket}: {mt5.last_error()}")
    
    return results
    

def is_market_open(trading_data):
 # Convertir check_time a un objeto datetime
    check_time = date.datetime.now().time().strftime("%H:%M:%S")
    print(check_time)

    #check_time_dt = date.datetime.fromtimestamp(check_time)

    session_index = 0  
    # Obtener la información de sesión para el símbolo y día de la semana especificados
    sessions = mt5.symbol_info_session_trade(trading_data['market'], get_current_day())
    
    # Comprobar si hay sesiones definidas para el día y el índice especificados
    if session_index < len(sessions):
        session = sessions[session_index]
        session_start = session.from_
        session_end = session.to
        
        # Comprobar si check_time está dentro del intervalo de sesión
        if session_start <= check_time <= session_end:
            return True
    
    return False

def comprobar_mercado(trading_data):

    hora_actual = date.datetime.now().strftime("%H:%M")
    hora_actual=    date.datetime.strptime(hora_actual, "%H:%M")
    check_time = hora_actual + date.timedelta(hours=1)
    check_time=check_time.time()
    checktime_formateado = check_time.strftime("%H:%M")
 

    tick = mt5.symbol_info_tick(trading_data['market'])
    tiempo_unix = tick[0]  # Obtenemos el tiempo en formato UNIX
    hora = pd.to_datetime(tiempo_unix, unit='s').time()  # Convertimos a formato hora
    hora_en_formato = hora.strftime("%H:%M")


    if hora_en_formato == checktime_formateado:
        return True
    else:
        return False

def get_current_day():
    current_day = date.datetime.now().strftime("%A")
    print(current_day)
    
    if(current_day=='Monday'):
        return mt5.DAY_OF_WEEK_MONDAY
    elif(current_day=='Tuesday'):
        return mt5.DAY_OF_WEEK_TUESDAY
    elif(current_day=='Wednesday'):
        return mt5.DAY_OF_WEEK_WEDNESDAY
    elif(current_day=='Thursday'):
        return mt5.DAY_OF_WEEK_THURSDAY
    elif(current_day=='Friday'):
        return mt5.DAY_OF_WEEK_FRIDAY
    elif(current_day=='Tuesday'):
        return mt5.DAY_OF_WEEK_SATURDAY
    
    else: return mt5.DAY_OF_WEEK_SUNDAY

def calcular_rentabilidad_operacion(precio_compra,precio_venta):
    rentabilidad = ((precio_venta-precio_compra)/ precio_compra) * 100
    return rentabilidad

def insertar_ticks(tipo, result, trading_data, compras):
    global FRAMETICKS, MERCADOCERRADO
    

    ticks_frame = pd.DataFrame(columns=['Accion', 'Orden', 'Fecha', 'Precio', 'Decision', 'Rentabilidad'])
    if tipo == 'MERCADO CERRADO' and not MERCADOCERRADO:
        new_data = {'Accion': trading_data['market'], 'Orden': "No hay orden", 'Fecha': date.datetime.now(), 'Precio': "-", 'Decision': "Mercado Cerrado"}
        ticks_frame.loc[len(ticks_frame)] = new_data
        MERCADOCERRADO = True
    else:
        if tipo == 'Compra':
            new_data = {'Accion': trading_data['market'], 'Orden': result.order, 'Fecha': date.datetime.now(), 'Precio': result.price, 'Decision': "Compra"}
            ticks_frame.loc[len(ticks_frame)] = new_data
        elif tipo == 'Ventas':
            for sell in result:
                print(compras[0].price, compras[0].order)
                rentabilidad = calcular_rentabilidad_operacion(compras[0].price, sell.price)
                new_data = {'Accion': trading_data['market'], 'Orden': compras[0].order, 'Fecha': date.datetime.now(), 'Precio': sell.price, 'Decision': "Venta", 'Rentabilidad': rentabilidad}
                ticks_frame.loc[len(ticks_frame)] = new_data
                compras.pop(0)
        elif tipo == 'NO HA HABIDO EL RESULTADO ELEGIDO':
            new_data = {'Accion': trading_data['market'], 'Orden': "No hay orden", 'Fecha': date.datetime.now(), 'Precio': "-", 'Decision': "No ha habido el resultado elegido"}
            ticks_frame.loc[len(ticks_frame)] = new_data
        else:
            new_data = {'Accion': trading_data['market'], 'Orden': "No hay orden", 'Fecha': date.datetime.now(), 'Precio': "-", 'Decision': "No hay operacion"}
            ticks_frame.loc[len(ticks_frame)] = new_data

        MERCADOCERRADO = False
        
    
    FRAMETICKS = pd.concat([FRAMETICKS, ticks_frame], ignore_index=True)
    print("Ordenes")
    print(FRAMETICKS)

   
def diftime(t1,t2):
    if t1-t2>TIMEBTWOPERATIONS:
        print("Diferencia de tiempo mayor a 15 minutos")
        print(t1-t2)
        return True
    else:
        return False
    
def ventas_sin_cerrar(ventasSinCerrar, trading_data):
    global FRAMETICKS,compras
    ticks_frame = pd.DataFrame(columns=['Accion', 'Orden', 'Fecha', 'Precio', 'Decision', 'Rentabilidad'])
    for sell in ventasSinCerrar:
        print(compras[0].price, compras[0].order)
        rentabilidad = calcular_rentabilidad_operacion(compras[0].price, sell.price)
        new_data = {'Accion': trading_data['market'], 'Orden': compras[0].order, 'Fecha': date.datetime.now(), 'Precio': sell.price, 'Decision': "Venta", 'Rentabilidad': rentabilidad}
        ticks_frame.loc[len(ticks_frame)] = new_data
        compras.pop(0)

    compras.clear() #limpio el array de compras
    FRAMETICKS = pd.concat([FRAMETICKS, ticks_frame], ignore_index=True)
     # Insert row at the end of FRAMETICKS
    new_row = pd.DataFrame({'Decision': ['Inversion finalizada']}, index=[len(FRAMETICKS)])
    FRAMETICKS = pd.concat([FRAMETICKS, new_row], ignore_index=True)


def parar_inversion(trading_data):
    global FRAMETICKS
    # check the presence of open positions
    orders = mt5.positions_get(symbol=trading_data['market'])
    if orders is not None:
        ventasSinCerrar = cerrar_todas_las_posiciones(trading_data)
        ventas_sin_cerrar(ventasSinCerrar, trading_data)
    else:
         # Insert row at the end of FRAMETICKS
        new_row = pd.DataFrame({'Decision': ['Inversion finalizada']}, index=[len(FRAMETICKS)])
        FRAMETICKS = pd.concat([FRAMETICKS, new_row], ignore_index=True)
        print("No hay posiciones abiertas")
    frame=FRAMETICKS
    # Vaciar el DataFrame FRAMETICKS
    FRAMETICKS = pd.DataFrame(columns=['Accion', 'Orden', 'Fecha', 'Precio', 'Decision', 'Rentabilidad'])
    return frame

def thread_orders(pill2kill, trading_data: dict, estrategia_directo):
    """Function executed by a thread. It opens and handles operations.

    Args:
        pill2kill (Threading.Event): Event to stop the thread's execution.
        trading_data (dict): Dictionary with all the needed data 
        for opening operations.
    """
    print("[THREAD - orders] - Working")
    

    print("[THREAD - orders] - Checking operations")

    global FRAMETICKS,HAYPOSICIONESABIERTAS    

   
    tiempoUltima=0
    while not pill2kill.wait(trading_data['time_period']):
        if(comprobar_mercado(trading_data)):
            if len(compras) < 2 and check_buy(estrategia_directo):  
                # if(tiempoUltima==0 or diftime(date.datetime.now(),tiempoUltima)):          
                    buy = open_buy(trading_data)
                    if buy is not None:
                        HAYPOSICIONESABIERTAS=True
                        insertar_ticks("Compra", buy, trading_data, compras)
                        compras.append(buy)
                        now = date.datetime.now()
                        tiempoUltima = now
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                        print("[Thread - orders] Buy open -", dt_string)
                        buy = None
                # else: print("Diferencia de tiempo menor a 15 minutos")
            elif HAYPOSICIONESABIERTAS and check_sell(estrategia_directo):
                    sell = cerrar_todas_las_posiciones(trading_data)
                    if sell is not None:
                        HAYPOSICIONESABIERTAS=False
                        insertar_ticks("Ventas", sell, trading_data, compras) 
                        compras.clear() 
                        now = date.datetime.now()
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                        print("[Thread - orders] Close position -", dt_string)
                        sell = None
            else:
                insertar_ticks("Nada", None, trading_data, compras) 
                print("NO SE ABRE OPERACION")          
        else:
            insertar_ticks("MERCADO CERRADO", None, trading_data, compras) 
            print("MERCADO CERRADO")
            

def thread_orders_creativas(pill2kill, trading_data: dict, estrategia_directo):
    """Function executed by a thread. It opens and handles operations.

    Args:
        pill2kill (Threading.Event): Event to stop the thread's execution.
        trading_data (dict): Dictionary with all the needed data 
        for opening operations.
    """
    print("[THREAD - orders - Creativas] - Working")

    print("[THREAD] - Checking operations")

    global FRAMETICKS,HAYPOSICIONESABIERTAS

    while not pill2kill.wait(20):
        if(comprobar_mercado(trading_data)):
            Nuevo,comprobacion = check_buy(estrategia_directo)
            if(Nuevo):#ha habido partdo nuevo
                if(len(compras) < 10 and comprobacion):#coincide resultado con la eleccion del usuario
                    buy = open_buy(trading_data)
                    if buy is not None:
                        HAYPOSICIONESABIERTAS=True
                        compras.append(buy)
                        insertar_ticks("Compra", buy, trading_data, compras)
                        now = date.datetime.now()
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                        print("[Thread - orders] Buy open -", dt_string)
                        buy = None
                elif(HAYPOSICIONESABIERTAS and check_sell(estrategia_directo)):
                    sell = cerrar_todas_las_posiciones(trading_data)
                    if sell is not None:
                        HAYPOSICIONESABIERTAS=False
                        insertar_ticks("Ventas", sell, trading_data, compras)
                        compras.clear() 
                        now = date.datetime.now()
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                        print("[Thread - orders] Close position -", dt_string)
                        sell = None
                else:#no coincide resultado con la eleccion del usuario
                    insertar_ticks("NO HA HABIDO EL RESULTADO ELEGIDO", None, trading_data, compras) 
                    print("NO HA HABIDO EL RESULTADO ELEGIDO")
            else:#no ha habido partdo nuevo
                print("NO HA HABIDO EVENTO NUEVO")
        else:
            insertar_ticks("MERCADO CERRADO", None, trading_data, compras) 
            print("MERCADO CERRADO")


# def thread_orders_creativas(pill2kill, trading_data: dict, estrategia_directo):
#     """Function executed by a thread. It opens and handles operations.

#     Args:
#         pill2kill (Threading.Event): Event to stop the thread's execution.
#         trading_data (dict): Dictionary with all the needed data 
#         for opening operations.
#     """
#     print("[THREAD - orders - Creativas] - Working")
    
#     print("[THREAD] - Checking operations")

#     global FRAMETICKS, HAYPOSICIONESABIERTAS   

#     def execute_thread():
        #  if(comprobar_mercado(trading_data)):
        #     Nuevo,comprobacion = check_buy(estrategia_directo)
        #     if(Nuevo):#ha habido partdo nuevo
        #         if(len(compras) < 10 and comprobacion):#coincide resultado con la eleccion del usuario
        #             buy = open_buy(trading_data)
        #             if buy is not None:
        #                 HAYPOSICIONESABIERTAS=True
        #                 compras.append(buy)
        #                 insertar_ticks("Compra", buy, trading_data, compras)
        #                 now = date.datetime.now()
        #                 dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        #                 print("[Thread - orders] Buy open -", dt_string)
        #                 buy = None
        #         elif(HAYPOSICIONESABIERTAS and check_sell(estrategia_directo)):
        #             sell = cerrar_todas_las_posiciones(trading_data)
        #             if sell is not None:
        #                 HAYPOSICIONESABIERTAS=False
        #                 insertar_ticks("Venta Creativas", sell, trading_data, compras)
        #                 compras.clear() 
        #                 now = date.datetime.now()
        #                 dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        #                 print("[Thread - orders] Close position -", dt_string)
        #                 sell = None
        #         else:#no coincide resultado con la eleccion del usuario
        #             insertar_ticks("NO HA HABIDO EL RESULTADO ELEGIDO", None, trading_data, compras) 
        #             print("NO HA HABIDO EL RESULTADO ELEGIDO")
        #     else:#no ha habido partdo nuevo
        #         print("NO HA HABIDO EVENTO NUEVO")
        # else:
        #     print("MERCADO CERRADO")

#     # Schedule the execution of thread_orders_creativas at 9 am every day
#     schedule.every().day.at("09:00").do(execute_thread)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)