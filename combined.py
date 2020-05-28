import kivy
kivy.require('1.11.1')

from datetime import date

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



# TODO: add new player after already started, reset everything on front screen

total_points = {}
total_wins = {}

PIN_NUMBER = '1234'

time_remaining = ""
high_scores = [{"Name":"Gabe","Points":50,"Date":"2020-05-25"},
				{"Name":"Colton","Points":49,"Date":"2020-05-25"},
				{"Name":"Jovany","Points":48,"Date":"2020-05-25"},
				{"Name":"Obama","Points":47,"Date":"2020-05-25"},
				{"Name":"Tavares","Points":46,"Date":"2020-05-25"}]


def get_highscores():
	return high_scores


def update_overall_highscores(scores):
	high_scores=get_highscores()
	for new_score_name in scores:
		new_score_points = scores[new_score_name]
		for i in range(len(high_scores)):
			cur_score_points = high_scores[i]["Points"]
			if int(new_score_points) > cur_score_points:
				high_scores.insert(i, {"Name": new_score_name, "Points": int(new_score_points), "Date":str(date.today())})
				break
	high_scores = high_scores[0:5]


def close_any_current_popups():
	if isinstance(App.get_running_app().root_window.children[0], Popup):
				App.get_running_app().root_window.children[0].dismiss()

def create_simple_popup(title, text):
	close_any_current_popups()

	layout = GridLayout()
	layout.cols=1
	layout.add_widget(Label(text=text, halign = "center",text_size= (200, None), size_hint=(1,1)))
              
	
	popup = Popup(title=title, content=layout, size_hint=(.4,.3))
	layout.add_widget(Button(text="Close", on_press=popup.dismiss))
	return popup





class BackgroundColor(Widget):
	pass
	
class BackgroundLabel(BackgroundColor,Label):
	pass

class CheckBoxLabel(ButtonBehavior, Label):
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
        	create_simple_popup("No More Time", "No Time Remaining, Please Talk to an Associate for More Time").open()
        	if self.parent.name == 'mygrid':
        		self.parent.playbutton.disabled=True

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def pause(self):
    	self.anim.cancel(self)


    def add_time(self, time):
        self.anim.cancel(self)
        self.a += time
        if self.parent.name == 'mygrid':
            self.parent.playbutton.disabled=False

        self.start()
    	

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
	kivy_timer = IncrediblyCrudeClock()
	def __init__(self, **kwargs):
		super(MyScoreGrid, self).__init__(**kwargs)
	

	def show_target(self, gameType):

		self.game_float = FloatLayout()
		self.game_float.size=self.size_hint
		self.game_float.pos = self.pos

		if gameType == 'zombie':

			one_point_button = ImageButton(source="zombie1.jpg", size_hint=(.25,.25), pos_hint={"x":.1, "y":.35}, on_press=self.update_points_from_button)
			self.game_float.add_widget(one_point_button)
			one_point_button.update_text('1')

			two_point_button = ImageButton(source="zombie2.jpg", size_hint=(.22,.22), pos_hint={"x":.7, "y":.05}, on_press=self.update_points_from_button)
			self.game_float.add_widget(two_point_button)
			two_point_button.update_text('2')

			three_point_button = ImageButton(source="zombie3.jpg", size_hint=(.2,.2), pos_hint={"x":.15, "y":.05}, on_press=self.update_points_from_button)
			self.game_float.add_widget(three_point_button)
			three_point_button.update_text('3')

			four_point_button = ImageButton(source="zombie4.jpg", size_hint=(.18,.18), pos_hint={"x":.7, "y":.35}, on_press=self.update_points_from_button)
			self.game_float.add_widget(four_point_button)
			four_point_button.update_text('4')

			five_point_button = ImageButton(source="zombie5.jpg", size_hint=(.12,.12), pos_hint={"x":.4, "y":.25}, on_press=self.update_points_from_button)
			self.game_float.add_widget(five_point_button)
			five_point_button.update_text('5')

			six_point_button = ImageButton(source="zombie6.jpg", size_hint=(.1,.1), pos_hint={"x":.55, "y":.25}, on_press=self.update_points_from_button)
			self.game_float.add_widget(six_point_button)
			six_point_button.update_text('6')

		else:
			target_button = ImageButton(source="target-updated.png", size_hint=(.6,.6), pos_hint={"x":.15, "y":.05}, on_press=self.show_points_popup)
			self.game_float.add_widget(target_button)

		self.add_widget(self.game_float)



	def show_points_popup(self, instance):
			popupGrid = GridLayout()
			popupGrid.cols=3

			popupGrid.add_widget(Button(text="1", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="2", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="3", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="4", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="5", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="6", size_hint=(.5,1), on_press=self.update_points_from_button))
			popupGrid.add_widget(Button(text="0", size_hint=(.5,1), on_press=self.update_points_from_button))

			popup = Popup(title='Add Points', content=popupGrid, size_hint=(.4,.3))
			popupGrid.add_widget(Button(text="Close", size_hint=(.3,1), on_press=popup.dismiss))

			popup.open()

	def reset_players(self):
		self.cur_player = 1
		self.cur_round = 1
		self.all_labels = []

	def add_top_row(self):
		row_of_labels = []
		for i in range(self.rounds+2):
			if i == self.rounds+1:
				row_of_labels.append(BackgroundLabel(text="Total"))
			else:
				row_of_labels.append(BackgroundLabel(text=""))

		self.all_labels.append(row_of_labels)


	def add_player_rows(self):
		for player in self.players:
			row_of_labels=[Label(text=player)]
			for i in range(self.rounds+1):
				row_of_labels.append(BackgroundLabel(text="0"))

			self.all_labels.append(row_of_labels)

		self.all_labels[self.cur_player][self.cur_round].color=(1,0,0,1)

		self.inside = GridLayout()
		self.inside.name='insideGridLayout'
		self.inside.size_hint=(1, .2)
		self.inside.pos_hint={"x":0, "y":.8}

		self.inside.cols = self.rounds+2

		for row in self.all_labels:
			for label in row:
				self.inside.add_widget(label)

		self.add_widget(self.inside)


	def add_timer(self):
		self.inside.add_widget(self.kivy_timer)


	def set_keyboard_listener(self):
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)


	def set_players(self, playernames):
		self.reset_players()

		self.players = [i for i in playernames]
		self.player_points = [0 for i in playernames]

		self.add_top_row()
		self.add_player_rows()
		self.add_timer()




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
		if keycode[1] == '0':
			self.update_scoreboard(0)
		elif keycode[1] == '1':
			self.update_scoreboard(1)
		elif keycode[1] == '2':
			self.update_scoreboard(2)
		elif keycode[1] == '3':
			self.update_scoreboard(3)
		elif keycode[1] == '4':
			self.update_scoreboard(4)
		elif keycode[1] == '5':
			self.update_scoreboard(5)
		elif keycode[1] == '6':
			self.update_scoreboard(6)

		return True


	def highlight_row(self):
		for i in range(1, len(self.all_labels)):
			for label in self.all_labels[i]:
				if i == self.cur_player:
					label.background_color = (.4,.4,.4,1)
				else:
					label.background_color = (0,0,0,0)


	def unhighlight_previous_score_label(self):
		self.all_labels[self.cur_player][self.cur_round].color=(1,1,1,1)

	def highlight_next_score_label(self):
		if self.cur_round <= self.rounds:
			self.all_labels[self.cur_player][self.cur_round].color=(1,0,0,1)

	def update_label_index(self):
		self.cur_player += 1
		if self.cur_player == len(self.players)+1:
			self.cur_player = 1
			self.cur_round += 1
		

	def update_scoreboard(self, score):
		if self.cur_round > self.rounds:
			create_simple_popup("Game Over", "No More Rounds, Please Start New Game").open()
		else:
			self.all_labels[self.cur_player][self.cur_round].text=str(score)
			self.player_points[self.cur_player-1] += score
			self.update_point_totals()
			self.unhighlight_previous_score_label()
			self.update_label_index()
			self.highlight_next_score_label()
			self.highlight_row()


	def update_points_from_button(self, instance):
		close_any_current_popups()
		points = int(instance.text)
		self.update_scoreboard(points)

		

	def update_point_totals(self):
		self.all_labels[self.cur_player][self.rounds+1].text = str(self.player_points[self.cur_player-1])


	def update_overall_points(self):
		self.inside.clear_widgets()
		self.game_float.clear_widgets()
		self.remove_widget(self.inside)
		self.remove_widget(self.game_float)

		points_to_update = {}
		for i in range(len(self.players)):
			total_points[self.players[i]] += self.player_points[i]
			points_to_update[self.players[i]] = self.player_points[i]

		update_overall_highscores(points_to_update)



	def calculate_final_winner(self):
		winner=[]
		top_score = -1
		for i in range(len(self.players)):
			if top_score < self.player_points[i]:
				top_score = self.player_points[i]
				winner.clear()
				winner.append(self.players[i])
			elif top_score == self.player_points[i]:
				winner.append(self.players[i])

		return winner, top_score

	def show_final_winner(self):
		winner, top_score = self.calculate_final_winner()

		for name in winner:
			total_wins[name] += 1

		popup = self.create_winner_popup("Congratulations to "+", ".join(winner) + ", won with " + str(top_score)+" points")		
		popup.open()

	def create_winner_popup(self, winner_text):
		close_any_current_popups()

		layout = GridLayout()
		layout.cols=1
		layout.add_widget(Label(text=winner_text, halign = "center",text_size= (200, None), size_hint=(1,1)))
		layout.add_widget(Button(text="Close", on_press=self.close_winner_and_go_to_next_screen))

		popup = Popup(title="Winner", content=layout, size_hint=(.4,.3))
		return popup


	def close_winner_and_go_to_next_screen(self, instance):
		close_any_current_popups()

		self.parent.manager.return_to_front_screen()



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

	firstplacename=ObjectProperty(None)
	firstplacepoints=ObjectProperty(None)
	firstplacedate=ObjectProperty(None)
	
	secondplacename=ObjectProperty(None)
	secondplacepoints=ObjectProperty(None)
	secondplacedate=ObjectProperty(None)

	thirdplacename=ObjectProperty(None)
	thirdplacepoints=ObjectProperty(None)
	thirdplacedate=ObjectProperty(None)

	fourthplacename=ObjectProperty(None)
	fourthplacepoints=ObjectProperty(None)
	fourthplacedate=ObjectProperty(None)

	fifthplacename=ObjectProperty(None)
	fifthplacepoints=ObjectProperty(None)
	fifthplacedate=ObjectProperty(None)

	kivy_timer = IncrediblyCrudeClock()

	def __init__(self, **kwargs):
		super(MyGrid, self).__init__(**kwargs)
		self.kivy_timer.name="kivy_timer"
		self.kivy_timer.set_time(60)
		self.kivy_timer.start()

		self.add_widget(self.kivy_timer)

		self._keyboard = Window.request_keyboard(self._keyboard_closed_main, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down_main)

		Clock.schedule_once(self.update_highscores, 0)

	def update_highscores(self, instance):
		highscores = get_highscores()
		self.firstplacename.text=highscores[0]["Name"]
		self.firstplacepoints.text=str(highscores[0]["Points"])
		self.firstplacedate.text=highscores[0]["Date"]
		
		self.secondplacename.text=highscores[1]["Name"]
		self.secondplacepoints.text=str(highscores[1]["Points"])
		self.secondplacedate.text=highscores[1]["Date"]

		self.thirdplacename.text=highscores[2]["Name"]
		self.thirdplacepoints.text=str(highscores[2]["Points"])
		self.thirdplacedate.text=highscores[2]["Date"]

		self.fourthplacename.text=highscores[3]["Name"]
		self.fourthplacepoints.text=str(highscores[3]["Points"])
		self.fourthplacedate.text=highscores[3]["Date"]

		self.fifthplacename.text=highscores[4]["Name"]
		self.fifthplacepoints.text=str(highscores[4]["Points"])
		self.fifthplacedate.text=highscores[4]["Date"]


	def _keyboard_closed_main(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


	def _keyboard_closed(self):
		pass

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		pass


	def focus_playername(self, instance):
		self.playername.focus=True


	def create_admin_popup(self):
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

		return popup


	def _on_keyboard_down_main(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'enter':
			Clock.schedule_once(self.focus_playername, .2)

		if keycode[1] == 'm' and "ctrl" in modifiers:
			self.create_admin_popup().open()

		return True

	def add_time(self, instance, pin, time):
		if pin == PIN_NUMBER:
			if not time.isdigit():
				create_simple_popup("Invalid Time Amount", "Please Enter Valid Time to Add").open()
			else:
				self.kivy_timer.add_time(float(time)*60)
				create_simple_popup("Time Added", str(time) + " minute(s) successfully added").open()
		else:
			create_simple_popup("Incorrent Pin", "Please Enter the Correct Pin").open()

		
	def set_timer(self, time_left):
		self.kivy_timer.a=time_left

	def pause_timer(self):
		self.kivy_timer.pause()

	def restart_timer(self):
		if self.kivy_timer.a > 0:
			self.kivy_timer.start()
		self.numplayers.focus=True

	def reset_player_data(self):
		total_points.clear()
		total_wins.clear()
		self.player_names = []
		self.curplayer_index = 1
		self.totalpointslabel.text = ""
		self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)
		self.displaynumplayers.text = "Number of Players: " + self.numplayers.text
		self.displayplayernames.text = "Players: " 



	def set_num_players(self):
		if not self.is_group_size_is_valid_number():
			create_simple_popup("Invalid Group Size", "Please Enter Valid Group Size").open()
		else:
			self.reset_player_data()
			Clock.schedule_once(self.focus_playername, .2)

	def init_total_points(self):
		text = "Total Points:\n\n"
		for name in self.player_names:
			text += name + ": 0\n"
		self.totalpointslabel.text = text


	def get_time_left(self):
		return self.kivy_timer.a


	def check_timer_status(self):
		if self.kivy_timer.a == 0:
			self.playbutton.on_release=print("released")


	def get_player_names(self):
		return self.player_names



	def submit_player_name(self):
		self.playername.text = self.playername.text.strip()

		if not self.is_group_size_is_valid_number():
			create_simple_popup("Invalid Group Size", "Please Enter Valid Group Size").open()

		elif self.player_already_exists():
			create_simple_popup("Invalid Player Name", "Player already added, please enter new name").open()

		elif self.player_name_is_correct_length():
			create_simple_popup("Invalid Player Name", "Player name must be at least one character").open()

		elif self.curplayer_index < int(self.numplayers.text):
			self.add_player_to_array()
			self.curplayer.text = "Enter Name for Player " + str(self.curplayer_index)


		elif self.curplayer_index == int(self.numplayers.text):
			self.add_player_to_array()
			self.curplayer.text = "All Players Added"
			self.init_total_points()

		else:
			self.curplayer.text = "No More Players Can Be Added"

		self.playername.text = ""		

		Clock.schedule_once(self.focus_playername, .1)


	def add_player_to_array(self):
		self.curplayer_index += 1
		self.player_names.append(self.playername.text)
		total_points[self.playername.text] = 0
		total_wins[self.playername.text] = 0
		text = "\""+"\", \"".join(self.player_names)+"\""
		self.displayplayernames.text = "Players: " + text


	def focus_playername(self, instance):
		self.playername.focus=True


	def player_already_exists(self):
		return self.playername.text in self.player_names

	def player_name_is_correct_length(self):
		return len(self.playername.text) == 0

	def all_players_already_added(self):
		return len(self.player_names) == int(self.numplayers.text)

	def is_group_size_is_valid_number(self):
		return self.numplayers.text.isdigit() and int(self.numplayers.text) > 0

	def ok_to_play(self):
		return self.is_group_size_is_valid_number() and self.all_players_already_added()

	def check_timer(self):
		if self.kivy_timer.a == 0:
			self.playbutton.disabled = True


	def update_total_wins(self):
		text = "Total Wins: \n\n"
		for key in total_wins:
			text += key + ": " + str(total_wins[key]) + " (" + str(total_points[key])+ " points)\n"

		self.totalpointslabel.text = text
		



class MainWindow(Screen):
	def on_enter(self, *args):
		if self.manager.ids:
			self.manager.ids.screen2.ids.myscoregrid.pause_timer()

			self.manager.ids.screen1.ids.mygrid.update_total_wins()
			self.manager.ids.screen1.ids.mygrid.set_timer(self.manager.ids.screen2.ids.myscoregrid.get_time_left())
			self.manager.ids.screen1.ids.mygrid.restart_timer()
			self.manager.ids.screen1.ids.mygrid.update_highscores(None)
			self.manager.ids.screen1.ids.mygrid.check_timer()
	

class SecondWindow(Screen):
	def on_enter(self, *args):
		self.setup_score_board()
		self.start_game_timer()
		self.pause_front_screen_timer()
		self.display_correct_game_type()

	def setup_score_board(self):
		names = self.manager.ids.screen1.ids.mygrid.get_player_names()
		self.manager.ids.screen2.ids.myscoregrid.set_players(names)
		self.manager.ids.screen2.ids.myscoregrid.set_keyboard_listener()
		self.manager.ids.screen2.ids.myscoregrid.highlight_row()

	def start_game_timer(self):
		self.manager.ids.screen2.ids.myscoregrid.set_timer(self.manager.ids.screen1.ids.mygrid.get_time_left())
		self.manager.ids.screen2.ids.myscoregrid.restart_timer()

	def pause_front_screen_timer(self):
		self.manager.ids.screen1.ids.mygrid.pause_timer()

	def display_correct_game_type(self):
		game_type = 'target'
		if self.manager.ids.screen1.ids.zombiegame.active:
			game_type = 'zombie'

		self.manager.ids.screen2.ids.myscoregrid.show_target(game_type)






class WindowManager(ScreenManager):
	def go_to_game_screen(self):
		if not self.ids.screen1.ids.mygrid.is_group_size_is_valid_number():
			create_simple_popup("Invalid Group Size", "Please Enter Valid Group Size").open()
		elif not self.ids.screen1.ids.mygrid.all_players_already_added():
			create_simple_popup("Not All Players Added", "Please Enter Remaining Players").open()
		else:
			self.current='screen2'
			self.transition.direction = "left"

	def end_current_game(self):
		self.ids.screen2.ids.myscoregrid.show_final_winner()


	def return_to_front_screen(self):
		self.current='screen1'
		self.transition.direction = "right"		
	


kv = Builder.load_file("combined.kv")

class CombinedScreenApp(App):
	def build(self):
		return kv


if __name__ == "__main__":
	CombinedScreenApp().run()