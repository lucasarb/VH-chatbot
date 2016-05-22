import sys
import traceback

#Import url haddling
import urllib2
import urllib
import json

#Import chatbot APIs
import telepot
from telepot.delegate import per_chat_id, create_open
from telepot.routing import by_chat_command



class Player(telepot.helper.ChatHandler):
	def __init__(self, seed_tuple, timeout):
		super(Player,self).__init__(seed_tuple,timeout)

		self._user = ""
		self._gamekey = ''
		self._new_game_url = 'https://az-mastermind.herokuapp.com/new_game'
		self._guess_url = 'https://az-mastermind.herokuapp.com/guess'
		self._colors = []
		self._code_length = 0
		self._num_guesses = 0
		self._past_results = []
		self._result = []
		self._solved = "false"

	def _hint(self):
		#TODO HINT MODULE TO GIVE THE BEST GUESS OF MASTERMIND
		self.sender.sendMessage('Hint features not yet available')
		return

	#Function will be activated when the player talks to bot
	def open(self, initial_msg, seed):
		self.sender.sendMessage("""
		Hello! I'm the Mastermind BOT. 

		I was created for the VANHACKATHON using Axiom Zen Mastermind API. To begin a new game of mastermind type:

		/newgame
			""")
		return True

	# Function activated when the player types /newgame
	def _newgame(self,msg):
		#starts a new game
		
		user_name = msg['from']['first_name']

		self._user = user_name

		q_newgame = {'user': user_name }

		try:
			send_newgame = urllib.urlencode(q_newgame)
		except:
			user_name = 'Player'
			q_newgame = {'user': user_name }
			send_newgame = urllib.urlencode(q_newgame)

		request = urllib2.Request(self._new_game_url, send_newgame)
		response = urllib2.urlopen(request)

		game_data = json.load(response)

		self._gamekey = game_data['game_key']
		self._colors = game_data['colors']
		self._code_length = game_data['code_length']
		self._num_guesses = game_data['num_guesses']
		self._past_results = game_data['past_results']
		self._solved = game_data['solved']

		self.sender.sendMessage("""
			Game started!
			You need to send a code consisting of 8 letters of RBGYOPCM
			(corresponding to Red, Blue, Green, Yellow, Orange, Purple, Cyan, Magenta)
			""")
		return


	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		if (msg['text'] == '/newgame'):
			self._newgame(msg)
			return
		if (msg['text'] == '/hint'):
			self._hint()
			return

		if (content_type != 'text') or (self._gamekey == ''):
			self.sender.sendMessage('If you want to begin a new game type: /newgame')
			return

		if len(msg['text']) != self._code_length:
			self.sender.sendMessage('You need to send a code consisting of 8 letters')
			return

		try:
			guess = msg['text'].upper()
			guess_check = list(guess)

			for item in guess_check:
				if item not in ['R', 'B', 'G', 'Y', 'O', 'P', 'C', 'M']:
					self.sender.sendMessage('You need to send a code consisting of 8 letters and does not contain any letter different from RBGYOPCM')
					return

			q_guess = {'code': guess,'game_key': self._gamekey}
			send_guess = urllib.urlencode(q_guess)

			request = urllib2.Request(self._guess_url, send_guess)
			response = urllib2.urlopen(request)

			game_data = json.load(response)

			self._gamekey = game_data['game_key']
			self._colors = game_data['colors']
			self._code_length = game_data['code_length']
			self._num_guesses = game_data['num_guesses']
			self._past_results = game_data['past_results']
			self._result = game_data['result']
			self._solved = game_data['solved']

		except ValueError:
			self.sender.sendMessage('There was an error in the guessing part')
			return

		if self._solved == 'true':
			self.sender.sendMessage("Congratulations %s, you are correct! The result was %s. You took %s attempts" % (self._user,guess, self._num_guesses))
			self.close()
		else:
			self.sender.sendMessage('You got %s colors in the exact place and %s near it' % (self._result['exact'], self._result['near']))
			self.sender.sendMessage('If you need a hint just type: /hint')

	def on_close(self, exception):
		if isinstance(exception, telepot.exception.WaitTooLong):
			self.sender.sendMessage('Game expired')


TOKEN = '228795069:AAEDYFUP96p8SUpDNlcqGSmksKrixKkGmD8'

bot = telepot.DelegatorBot(TOKEN, [(per_chat_id(),create_open(Player, timeout = 90))])

bot.message_loop(run_forever = True)