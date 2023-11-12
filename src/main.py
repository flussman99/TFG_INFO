import bot
import matplotlib.pyplot as plt

# Creating a bot
b = bot.Bot(1, 15*60, "SAN.MAD")
with open("login.txt", 'r') as f:
    lines = f.readlines()
    usr = int(lines[0].strip())
    password = lines[1].strip()
    server = lines[2].strip()

# Login into mt5
if not b.mt5_login(usr,password,server):
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
#plt.savefig()
