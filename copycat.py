from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
import time
import math
from random import seed
from random import random
from datetime import datetime
seed(datetime.now())

events = []
recording = False
captured = False
end = False
mouse_ctl = mouse.Controller()

# Mouse Hooks
def on_move(x, y):
    if(recording):
	    events.append((time.time(), x, y))

def on_scroll(x, y, dx, dy):
    if(recording):
	    events.append((time.time(), dx, dy, True))

def on_click(x, y, button, pressed):
    if(recording):
	    events.append((time.time(), x, y, button, pressed))

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_scroll=on_scroll,
    on_click=on_click
)

mouse_listener.start()


# reset mouse position smoothly
def reset():

	# find first mouse move event to consider as end point
	found = False
	counter = 0
	while(not found and counter < len(events)):
		if(len(events[counter]) == 3):
			
			# flag
			found = True

			# time resolution
			dt = 1000

			# save current position
			(x, y) = mouse_ctl.position
			(xx, yy) = (events[counter][1], events[counter][2])
			dx = (xx - x) / dt
			dy = (yy - y) / dt

			# amplitude sinusoidal modulation
			mod_amplitude = random() * 2.5

			# initial thetas set to random radian values
			theta_x = random()
			theta_y = random()
			d_theta_x = 0.005 + (random() * 0.005)
			d_theta_y = 0.005 + (random() * 0.005)

			# traverse to start point
			for i in range(dt):

				# modulation as f(x) of time
				x_mod = math.sin(theta_x) * mod_amplitude
				y_mod = math.cos(theta_y) * mod_amplitude

				x = x + dx
				y = y + dx
				theta_x += d_theta_x
				theta_y += d_theta_y

				# move
				mouse_ctl.position = (x + x_mod, y + y_mod)


# replay event stream with randomization for anti-bot detection circumvention
def replay():

	# re-seed? 5% chance
	if(random() <= 0.05):
		seed(datetime.now())

	# mouse position randomization (3 pixel radius)
	offset_x = random() * 3
	offset_y = random() * 3
	if(random() > 0.5):
		offset_x = -1 * offset_x
	if(random() <= 0.5):
		offset_y = -1 * offset_y

	# amplitude sinusoidal modulation
	mod_amplitude = random() * 1.9

	counter = 0
	
	for event in events:

		# modulation as f(x) of time
		x_mod = math.sin(event[0]) * mod_amplitude
		y_mod = math.cos(event[0]) * mod_amplitude

		global end
		if(end):
			break

		# move
		if(len(event) == 3):
			mouse_ctl.position = (event[1] + offset_x + x_mod,
				event[2] + offset_y + y_mod)
		# click
		elif(len(event) == 5):
			# random pause just incase
			if(event[3] != Button.right):
				time.sleep(random() * 0.5)

			if(event[4]):
				mouse_ctl.press(event[3])
			else:
				mouse_ctl.release(event[3])
		# scroll
		elif(len(event) == 4):
			mouse_ctl.scroll(event[1], event[2])
		else:
			pass
		# delay
		if(counter < len(events) - 1):
			time.sleep(events[counter + 1][0] - events[counter][0])

		counter+=1

	# random sleep
	time.sleep(5 * random())

	# random walk to original position
	reset()

# Key control hooks
def on_press(key):
	global recording
	global captured
	global end
	if(not captured and not recording and key.value.vk == 49):
		print('Recording...')
		recording = True
	elif(not captured and recording and key.value.vk == 49):
		recording = False
		captured = True
	elif(captured and key.value.vk == 53):
		end = True
	pass

def on_release(key):
    pass

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()

print('Press the space bar to begin capturing, then press the space bar again to end recording and start replay.')

while(not captured):
	pass

mouse_listener.stop()

# countdown to position
print('Starting in...')

for i in range(5):
    print(5 - i)
    time.sleep(1)

print('Pres ESC to exit')

while(not end):
	replay()

keyboard_listener.stop()

exit(0)
