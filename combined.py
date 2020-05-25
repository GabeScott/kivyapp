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
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
import math
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


def create_simple_popup(title, text):
	layout = GridLayout()
	layout.cols=1
	layout.add_widget(Label(text=text, halign = "center",text_size= (200, None), size_hint=(1,1)))
              
	
	popup = Popup(title=title, content=layout, size_hint=(.4,.3))
	layout.add_widget(Button(text="Close", on_press=popup.dismiss))
	return popup

total_points = {}

PIN_NUMBER = '1234'

time_remaining = ""


class BackgroundColor(Widget):
	pass
class BackgroundLabel(BackgroundColor,Label):
	pass

class ImageButton(ButtonBehavior, Image):
	text=""
	def update_text(self, text):
		self.text = text

class IncrediblyCrudeClock(Label):
    a = NumericProperty(60)  # seconds

    def set_time(self, time):
    	self.a = time

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        
        def finish_callback(animation, incr_crude_clock):
        	popup = create_simple_popup("No Time Left",'No more time left, please contact an associate to add more time')
        	popup.open()
        	if self.parent.name == 'mygrid':
        		self.parent.playbutton.disabled=True

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)



    def add_time(self, time):
     	self.a += time
     	if self.parent.name == 'mygrid':
           	self.parent.playbutton.disabled=False


    def pause(self):
    	self.anim.cancel(self)

    def on_a(self, instance, value):
        hours = math.floor(value/3600)
        minutes = math.floor((value%3600)/60)
        seconds = math.floor((value%60))
        self.text = "{:02d}".format(hours) + ":"+"{:02d}".format(minutes)+":"+"{:02d}".format(seconds)

class MyScoreGrid(FloatLayout):
	rounds = 10
	players = []
	player_points = []
	cur_player = 1
	cur_round = 1
	all_labels=[]	
	loaded = False
	kivy_timer = IncrediblyCrudeClock()
	def __init__(self, **kwargs):
		super(MyScoreGrid, self).__init__(**kwargs)

		one_point_button = ImageButton(source="zombie1.jpg", size_hint=(.25,.25), pos_hint={"x":.1, "y":.35}, on_press=self.update_points)
		self.add_widget(one_point_button)
		one_point_button.update_text('1')

		two_point_button = ImageButton(source="zombie2.jpg", size_hint=(.22,.22), pos_hint={"x":.7, "y":.05}, on_press=self.update_points)
		self.add_widget(two_point_button)
		two_point_button.update_text('2')

		three_point_button = ImageButton(source="zombie3.jpg", size_hint=(.2,.2), pos_hint={"x":.15, "y":.05}, on_press=self.update_points)
		self.add_widget(three_point_button)
		three_point_button.update_text('3')

		four_point_button = ImageButton(source="zombie4.jpg", size_hint=(.18,.18), pos_hint={"x":.7, "y":.35}, on_press=self.update_points)
		self.add_widget(four_point_button)
		four_point_button.update_text('4')

		five_point_button = ImageButton(source="zombie5.jpg", size_hint=(.12,.12), pos_hint={"x":.45, "y":.25}, on_press=self.update_points)
		self.add_widget(five_point_button)
		five_point_button.update_text('5')






	def set_players(self, playernames):

		self.cur_player = 1
		self.cur_round = 1
		self.players = [i for i in playernames]
		self.player_points = [0 for i in playernames]
		self.all_labels = []

		if self.loaded:
			self.inside.clear_widgets()
			self.remove_widget(self.inside)

		row_of_labels = []
		for i in range(self.rounds+2):
			if i == self.rounds+1:
				row_of_labels.append(BackgroundLabel(text="Total"))
			else:
				row_of_labels.append(BackgroundLabel(text=""))

		self.all_labels.append(row_of_labels)




		for player in self.players:
			row_of_labels=[Label(text=player)]
			for i in range(self.rounds+1):
				row_of_labels.append(BackgroundLabel(text="0"))

			self.all_labels.append(row_of_labels)

		self.all_labels[self.cur_player][self.cur_round].color=(1,0,0,1)

		self.inside = GridLayout()
		self.inside.size_hint=(1, .2)
		self.inside.pos_hint={"x":0, "y":.8}

		self.inside.cols = self.rounds+2

		for row in self.all_labels:
			for label in row:
				self.inside.add_widget(label)




		self.add_widget(self.inside)	
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self.loaded = True

		self.inside.name='insideGridLayout'
		self.inside.add_widget(self.kivy_timer)



	def set_timer(self, time_left):
		self.kivy_timer.set_time(time_left)

	def pause_timer(self):
		self.kivy_timer.pause()

	def restart_timer(self):
		if self.kivy_timer.a > 0:
			self.kivy_timer.start()
	def get_time_left(self):
		return self.kivy_timer.a


	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		points_to_add = 0
		intentional_keypress = True
		if keycode[1] == '0':
			points_to_add = 0
		elif keycode[1] == '1':
			points_to_add = 1
		elif keycode[1] == '2':
			points_to_add = 2
		elif keycode[1] == '3':
			points_to_add = 3
		elif keycode[1] == '4':
			points_to_add = 4
		elif keycode[1] == '5':
			points_to_add = 5
		else:
			intentional_keypress = False

		if intentional_keypress:
			if self.cur_round > self.rounds:
				if isinstance(App.get_running_app().root_window.children[0], Popup):
					App.get_running_app().root_window.children[0].dismiss()
				popup = Popup(title='Game Over', content=Label(text="No More Rounds, Please Start New Game"), size_hint=(.4,.3))
				popup.open()
			else:
				self.all_labels[self.cur_player][self.cur_round].text=str(points_to_add)
				self.player_points[self.cur_player-1] += points_to_add
				self.update_total_points()
				self.update_label_index()
				self.highlight_row()
			print(keycode[1])
		return True

	def add_zero_points(self):
		if self.cur_round > self.rounds:
			if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()
			popup = Popup(title='Game Over', content=Label(text="No More Rounds, Please Start New Game"), size_hint=(.4,.3))
			popup.open()
		else:
			self.update_label_index()
			self.highlight_row()


	def highlight_row(self):
		for i in range(1, len(self.all_labels)):
			for label in self.all_labels[i]:
				if i == self.cur_player:
					label.background_color = (.4,.4,.4,1)
				else:
					label.background_color = (0,0,0,0)


	def update_label_index(self):
		self.all_labels[self.cur_player][self.cur_round].color=(1,1,1,1)
		self.cur_player += 1

		if self.cur_player == len(self.players)+1:
			self.cur_player = 1
			self.cur_round += 1
		
		if self.cur_round <= self.rounds:
			self.all_labels[self.cur_player][self.cur_round].color=(1,0,0,1)

	def update_points(self, instance):
		if self.cur_round > self.rounds:
			popup = create_simple_popup("Game Over", "No More Rounds, Please Start New Game")
			popup.open()
		else:
			self.all_labels[self.cur_player][self.cur_round].text=instance.text
			self.player_points[self.cur_player-1] += int(instance.text)
			self.update_total_points()
			self.update_label_index()
			self.highlight_row()



	def update_total_points(self):
		self.all_labels[self.cur_player][self.rounds+1].text = str(self.player_points[self.cur_player-1])


	def update_overall_points(self):
		print(total_points)
		for i in range(len(self.players)):
			total_points[self.players[i]] += self.player_points[i]
		# self._keyboard_closed()
		

class MyGrid(Widget):
	player_names = []
	curplayer_index = 1

	numplayers = ObjectProperty(None)
	curplayer = ObjectProperty(None)
	playername = ObjectProperty(None)
	displaynumplayers = ObjectProperty(None)
	displayplayernames = ObjectProperty(None)
	totalpointslabel = ObjectProperty(None)
	playbutton=ObjectProperty(None)

	kivy_timer = IncrediblyCrudeClock()

	def __init__(self, **kwargs):
		super(MyGrid, self).__init__(**kwargs)
		self.kivy_timer.name="kivy_timer"
		self.kivy_timer.set_time(60)
		self.kivy_timer.start()

		self.add_widget(self.kivy_timer)

		self._keyboard = Window.request_keyboard(self._keyboard_closed_main, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down_main)

	def _keyboard_closed_main(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


	def _keyboard_closed(self):
		print("CLOSED")

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		pass


	def focus_playername(self, instance):
		self.playername.focus=True



	def _on_keyboard_down_main(self, keyboard, keycode, text, modifiers):
		print(keycode)
		print(text)
		print(modifiers)

		if keycode[1] == 'enter':
			Clock.schedule_once(self.focus_playername, .2)

		if keycode[1] == 'm' and "ctrl" in modifiers:
			popupGrid = GridLayout()
			popupGrid.cols=2

			pin_input = TextInput(multiline=False, size_hint=(.5,.6))
			time_input = TextInput(multiline=False, size_hint=(.5,.6))
			pin_input.password=True

			popupGrid.add_widget(Label(text="Enter PIN",size_hint=(.5,.6)))
			popupGrid.add_widget(pin_input)
			popupGrid.add_widget(Label(text="Minutes to add:", size_hint=(.5,.6)))
			popupGrid.add_widget(time_input)
			popupGrid.add_widget(Label(text="", size_hint=(.5,.4)))
			popupGrid.add_widget(Label(text="", size_hint=(.5,.4)))
			popupGrid.add_widget(Button(text="Add", size_hint=(.5,1), on_press=lambda *args: self.add_time(*args, pin_input.text, time_input.text)))
			popup = Popup(title='Admin Portal', content=popupGrid, size_hint=(.4,.3))
			popupGrid.add_widget(Button(text="Close", size_hint=(.5,1), on_press=popup.dismiss))

			popup.open()

		return True

	def add_time(self, instance, pin, time):
		if pin == PIN_NUMBER:
			if not time.isdigit():
				popup = create_simple_popup("Invalid Time Amount", "Please Enter Valid Time to Add")
				popup.open()
			else:
				self.kivy_timer.pause()
				self.kivy_timer.add_time(float(time)*60)
				self.kivy_timer.start()
				popup = create_simple_popup("Time Added", time+ " Minutes Added Successfully")
				popup.open()
		else:
			popup = create_simple_popup("Incorrect PIN", time+ " Please Enter Correct PIN and try again")
			popup.open()

		

	def set_timer(self, time_left):
		self.kivy_timer.a=time_left

	def pause_timer(self):
		self.kivy_timer.pause()

	def restart_timer(self):
		if self.kivy_timer.a > 0:
			self.kivy_timer.start()
		self.numplayers.focus=True


	def set_num_players(self):
		if not self.numplayers.text.isdigit() or int(self.numplayers.text) <= 0:
			if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()
			popup = create_simple_popup("Enter Number of Players","Please Enter a Valid Number of Players")
			popup.open()
		else:
			total_points.clear()
			self.player_names = []
			self.curplayer_index = 1
			self.totalpointslabel.text = ""
			self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)
			self.displaynumplayers.text = "Number of Players: " + self.numplayers.text
			self.displayplayernames.text = "Players: " 




	def init_total_points(self):
		text = "Total Points:\n\n"
		for name in self.player_names:
			text += name + ": 0\n"
		self.totalpointslabel.text = text

		self._keyboard = Window.request_keyboard(self._keyboard_closed_main, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down_main)


	def get_time_left(self):
		return self.kivy_timer.a


	def check_timer_status(self):
		if self.kivy_timer.a == 0:
			self.playbutton.on_release=print("released")



	def submit_player_name(self):
		if not self.numplayers.text.isdigit() or int(self.numplayers.text) <= 0:
			if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()
			popup = create_simple_popup("Enter Number of Players","Please Enter a Valid Number of Players")
			popup.open()

		if self.playername.text in self.player_names:
			if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()
			popup = create_simple_popup("Invalid Player Name","Player Already Added, Please Choose New Name")
			popup.open()

		if len(self.playername.text) == 0:
			if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()
			popup = create_simple_popup("Invalid Player Name","Please Enter at Least One Character")
			popup.open()

		elif self.curplayer_index < int(self.numplayers.text):
			self.curplayer_index += 1
			self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)
			self.player_names.append(self.playername.text)
			total_points[self.playername.text] = 0
			text = "\""+"\", \"".join(self.player_names)+"\""
			self.displayplayernames.text = "Players: " + text

		elif self.curplayer_index == int(self.numplayers.text):
			self.player_names.append(self.playername.text)
			total_points[self.playername.text] = 0
			self.curplayer_index += 1
			self.curplayer.text = "All Players Added"
			self.init_total_points()
			text = "\""+"\", \"".join(self.player_names)+"\""
			self.displayplayernames.text = "Players: " + text

		else:
			self.curplayer.text = "No More Players Can Be Added"

		self.playername.text = ""		

		self.playername.focus=True

	def ok_to_play(self):
		return len(self.player_names) == int(self.numplayers.text)

		



class MainWindow(Screen):
	def on_enter(self, *args):
		if self.manager.ids:
			text = "Total Points: \n\n"
			for key in total_points:
				text += key + ": " + str(total_points[key]) + "\n"
			self.manager.ids.screen1.ids.totalpointslabel.text = text
			self.manager.ids.screen1.ids.mygrid.set_timer(self.manager.ids.screen2.ids.myscoregrid.get_time_left())
			self.manager.ids.screen1.ids.mygrid.restart_timer()
			self.manager.ids.screen2.ids.myscoregrid.pause_timer()
			if self.manager.ids.screen1.ids.mygrid.kivy_timer.a == 0:
				self.manager.ids.screen1.ids.mygrid.playbutton.disabled = True
	

class SecondWindow(Screen):
	def on_enter(self, *args):
		names = self.manager.ids.screen1.ids.displayplayernames.text.replace("Players: ", "").replace("\"", "").replace(",", "").split(" ")
		self.manager.ids.screen2.ids.myscoregrid.set_players(names)
		self.manager.ids.screen2.ids.myscoregrid.set_timer(self.manager.ids.screen1.ids.mygrid.get_time_left())
		self.manager.ids.screen2.ids.myscoregrid.restart_timer()
		self.manager.ids.screen1.ids.mygrid.pause_timer()	
		self.manager.ids.screen2.ids.myscoregrid.highlight_row()

class WindowManager(ScreenManager):
	def go_to_game_screen(self):
		if self.ids.screen1.ids.mygrid.ok_to_play():
			self.current='screen2'
			self.transition.direction = "left"
		else:
			popup = create_simple_popup("Enter Number of Players","Please Enter a Valid Number of Players")
			popup.open()
	


kv = Builder.load_file("combined.kv")

class CombinedScreenApp(App):
	def build(self):
		return kv


if __name__ == "__main__":
	CombinedScreenApp().run()