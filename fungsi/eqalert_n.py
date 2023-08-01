import telebot
import sys
from datetime import datetime

amp = sys.argv[1]
stanet = sys.argv[2]
sta = stanet.split('.')[3]
date = stanet.split('.')[0]
time = stanet.split('.')[1]

api_key = '5563930939:AAGg0cFlWMUr7Cblwzr3ybco84Urp7kmW74'
ID_TELE = 32790321
bot = telebot.TeleBot(api_key)
dt = datetime(int(date[:4]),int(date[4:6]),int(date[6:8]),int(time[:2]),int(time[2:4]),int(time[4:6]))
now = datetime.utcnow()
dif = ('%.1f')%((now-dt).total_seconds())

#print(amp)
if float(amp) >= 15:
    if float(amp) >= 90:
        pesan = u"\U0000274C"+"GEMPA BERPOTENSI DIRASAKAN "+u"\U0000203C"+"\nSNR = "+amp+"\nLOKASI = "+sta+"\n"+"WAKTU = "+date+"-"+time+"\n"+dif+" seconds ago"
        bot.send_message(ID_TELE, pesan)
    else:
        pesan = u"\U000026A0"+" TERDETEKSI GEMPA "+u"\U0000203C"+"\nSNR = "+amp+"\nLOKASI = "+sta+"\n"+"WAKTU = "+date+"-"+time+"\n"+dif+" seconds ago"
        bot.send_message(ID_TELE, pesan)
else:
    pesan = "Trigger Detected !!\nsnr="+amp+"/sta="+sta
    bot.send_message(ID_TELE, pesan)


