import sys
import random
import traceback
import telepot
from telepot.delegate import per_chat_id, create_open

class Player(telepot.helper.ChatHandler):
	def __init__(self, seed_tuple, timeout):
		super(Player,self).__init__(seed_tuple,timeout)
		self._answer = random.randint(0,99)

	def _hint(self, answer, guess):
		if answer > guess:
			return 'larger'
		else:
			return 'smaller'

	def open(self, initial_msg, seed):
		self.sender.sendMessage('Guess my number')
		return True

	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		if content_type != 'text':
			self.sender.sendMessage('Give me a number, please.')
			return
		
		try:
			guess = int(msg['text'])
		except ValueError:
			self.sender.sendMessage('Give me number, please.')
			return

		if guess != self._answer:
			#give a hint
			hint = self._hint(self._answer,guess)
			self.sender.sendMessage(hint)
		else:
			self.sender.sendMessage('Correct!!')
			self.close()
	def on_close(self, exception):
		if isinstance(exception, telepot.exception.WaitTooLong):
			self.sender.sendMessage('Game expired. The answer is %d' % self._answer)


TOKEN = '228795069:AAEDYFUP96p8SUpDNlcqGSmksKrixKkGmD8'

bot = telepot.DelegatorBot(TOKEN, [(per_chat_id(),create_open(Player, timeout = 30))])

bot.message_loop(run_forever = True)