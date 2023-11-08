import bot
import matplotlib.pyplot as plt

# Creating a bot
b = bot.Bot(0.01, 15*60, "EURUSD")

usr = 51468408
password = "YHPuThmy"


# Login into mt5
if not b.mt5_login(usr, password):
    quit()
b.thread_tick_reader()
#b.thread_slope_abs_rel()
#b.thread_MACD()
#b.thread_RSI()
#b.thread_orders()
b.wait()

# Haciendo una gráfica de los datos
lista_segundos = b.get_ticks()
xAxis = []
yAxis = []
i = 1
if len(lista_segundos) < 10000:
    for element in b.get_ticks():
        xAxis.append(i)
        yAxis.append(element)
        i += 1

plt.plot(xAxis, yAxis)
plt.show()
