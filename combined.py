import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button 
from kivy.uix.floatlayout import FloatLayout 
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window


players=[]

class MyScoreGrid(FloatLayout):
	rounds = 10
	players = []
	cur_player = 0
	cur_round = 1
	all_labels=[]	
	def __init__(self, **kwargs):
		super(MyScoreGrid, self).__init__(**kwargs)
	


		one_point_button = Button(text="1", size_hint=(.25,.25), pos_hint={"x":.1, "y":.35}, on_press=self.update_points)
		self.add_widget(one_point_button)

		two_point_button = Button(text="2", size_hint=(.22,.22), pos_hint={"x":.7, "y":.05}, on_press=self.update_points)
		self.add_widget(two_point_button)

		three_point_button = Button(text="3", size_hint=(.2,.2), pos_hint={"x":.15, "y":.05}, on_press=self.update_points)
		self.add_widget(three_point_button)

		four_point_button = Button(text="4", size_hint=(.18,.18), pos_hint={"x":.7, "y":.35}, on_press=self.update_points)
		self.add_widget(four_point_button)

		five_point_button = Button(text="5", size_hint=(.12,.12), pos_hint={"x":.45, "y":.25}, on_press=self.update_points)
		self.add_widget(five_point_button)





	def set_players(self, playernames):

		self.players = [i for i in playernames]

		for player in self.players:
			row_of_labels=[Label(text=player)]
			for i in range(self.rounds):
				row_of_labels.append(Label(text="0"))

			self.all_labels.append(row_of_labels)

		self.inside = GridLayout()
		self.inside.size_hint=(1, .2)
		self.inside.pos_hint={"x":0, "y":.8}

		self.inside.cols = self.rounds+1

		for row in self.all_labels:
			for label in row:
				self.inside.add_widget(label)

		self.add_widget(self.inside)	
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)



	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == '1':
			self.all_labels[self.cur_player][self.cur_round].text='1'
		elif keycode[1] == '2':
			self.all_labels[self.cur_player][self.cur_round].text='2'
		elif keycode[1] == '3':
			self.all_labels[self.cur_player][self.cur_round].text='3'
		elif keycode[1] == '4':
			self.all_labels[self.cur_player][self.cur_round].text='4'
		elif keycode[1] == '5':
			self.all_labels[self.cur_player][self.cur_round].text='5'

		self.update_label_index()
		return True



	def update_label_index(self):
		self.cur_player += 1

		if self.cur_player == len(self.players):
			self.cur_player = 0
			self.cur_round += 1

		if self.cur_round > self.rounds:
			self.cur_round = 1

	def update_points(self, instance):
		self.all_labels[self.cur_player][self.cur_round].text=instance.text
		self.update_label_index()


class MyGrid(Widget):
	player_names = []
	curplayer_index = 1

	numplayers = ObjectProperty(None)
	curplayer = ObjectProperty(None)
	playername = ObjectProperty(None)
	displaynumplayers = ObjectProperty(None)
	displayplayernames = ObjectProperty(None)

	def set_num_players(self):
		self.player_names = []
		self.curplayer_index = 1
		self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)
		self.displaynumplayers.text = "Number of Players: " + self.numplayers.text
		self.displayplayernames.text = "Players: " 



	def submit_player_name(self):

		if self.curplayer_index < int(self.numplayers.text):
			self.curplayer_index += 1
			self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)
			self.player_names.append(self.playername.text)

		elif self.curplayer_index == int(self.numplayers.text):
			self.player_names.append(self.playername.text)
			self.curplayer_index += 1
			self.curplayer.text = "All Players Added"

		else:
			self.curplayer.text = "No More Players Can Be Added"

		text = "\""+"\", \"".join(self.player_names)+"\""


		self.displayplayernames.text = "Players: " + text

		self.playername.text = ""		

		players.append(self.playername.text)


class MainWindow(Screen):
	pass

class SecondWindow(Screen):
	def on_enter(self, *args):
		names = self.manager.ids.screen1.ids.displayplayernames.text.replace("Players: ", "").replace("\"", "").replace(",", "").split(" ")
		self.manager.ids.screen2.ids.myscoregrid.set_players(names)

class WindowManager(ScreenManager):
	pass


kv = Builder.load_file("combined.kv")

class CombinedScreenApp(App):
	def build(self):
		return kv


if __name__ == "__main__":
	CombinedScreenApp().run()
