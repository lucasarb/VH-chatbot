import sys
import time
import pprint
import telepot

BOT_TOKEN = '228795069:AAEDYFUP96p8SUpDNlcqGSmksKrixKkGmD8'

def handle(msg):
	
	return

bot = telepot.Bot(BOT_TOKEN)

bot.message_loop(handle)
print 'Listening...'

while True:
	time.sleep(30)

