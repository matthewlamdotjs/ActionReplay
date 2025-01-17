from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
import time
import math
from random import seed
import random
from datetime import datetime
seed(datetime.now())

events = []
recording = False
captured = False
end = False
mouse_ctl = mouse.Controller()


# randomness wrapper
def rand():
	try:
		return random.SystemRandom().random()
	except NotImplementedError:
		return random.random()

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


# function to reset mouse position smoothly
def reset(offset_x, offset_y, mod_amplitude, x_sign, y_sign):

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

			x_mod = x_sign * math.sin(events[counter][0]) * mod_amplitude
			y_mod = y_sign * math.sin(events[counter][0]) * mod_amplitude
			(xx, yy) = (events[counter][1] + offset_x + x_mod, events[counter][2] + offset_y + y_mod)
			dx = (xx - x) / dt
			dy = (yy - y) / dt

			# amplitude sinusoidal modulation
			mod_amplitude_x = rand() * 20
			mod_amplitude_y = rand() * 20

			theta_x = 0
			theta_y = 0
			d_theta_x = 0.005 + (rand() * 0.005)
			d_theta_y = 0.005 + (rand() * 0.005)

			# traverse to start point
			for i in range(dt):

				# modulation as f(x) of time
				x_mod = math.sin(theta_x) * mod_amplitude_x
				y_mod = -math.sin(theta_y) * mod_amplitude_y

				x = x + dx
				y = y + dy
				theta_x += d_theta_x
				theta_y += d_theta_y

				# move
				mouse_ctl.position = (x + x_mod, y + y_mod)


			# prevent end jump from variant end point due to sine mod drift
			(x, y) = mouse_ctl.position
			dx = (xx - x) / dt
			dy = (yy - y) / dt
			theta_x = 0
			theta_y = 0
			d_theta_x = math.pi / dt
			d_theta_y = math.pi / dt
			mod_amplitude_x = rand() * 20
			mod_amplitude_y = rand() * 20
			x_sign = -1 if rand() > 0.5 else 1
			y_sign = -1 if rand() < 0.5 else 1
			
			for i in range(dt):

				x_mod = x_sign * math.sin(theta_x) * mod_amplitude_x
				y_mod = y_sign * math.sin(theta_y) * mod_amplitude_y
				
				x = x + dx
				y = y + dx

				theta_x += d_theta_x
				theta_y += d_theta_y

				mouse_ctl.position = (x + x_mod, y + y_mod)


# function to replay event stream with randomization for anti-bot detection circumvention
def replay():

	keyboard_ctl = keyboard.Controller()

	# re-seed? 5% chance
	if(rand() <= 0.05):
		seed(datetime.now())

	# mouse position randomization (3 pixel radius)
	offset_x = rand() * 2
	offset_y = rand() * 2
	if(rand() > 0.5):
		offset_x = -1 * offset_x
	if(rand() <= 0.5):
		offset_y = -1 * offset_y


	# amplitude sinusoidal modulation
	mod_amplitude = 1 + rand() * 3.9

	x_sign = -1 if rand() > 0.5 else 1
	y_sign = -1 if rand() < 0.5 else 1

	# reset smooth
	if(len(events) > 0):	

		# random walk to original position
		reset(offset_x, offset_y, mod_amplitude, x_sign, y_sign)

	counter = 0
	
	for event in events:

		# modulation as f(x) of time
		x_mod = x_sign * math.sin(event[0]) * mod_amplitude
		y_mod = y_sign * math.sin(event[0]) * mod_amplitude

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
				time.sleep(rand() * 0.5)

			if(event[4]):
				mouse_ctl.press(event[3])
			else:
				mouse_ctl.release(event[3])
		# scroll
		elif(len(event) == 4):
			mouse_ctl.scroll(event[1], event[2])
		# keys
		elif(len(event) == 2):
			# keydown
			if(event[1][1]):
				time.sleep(rand() * 0.2) # safe to wait here without side-effects
				keyboard_ctl.press(KeyCode.from_vk(event[1][0]))
			# keyup
			else:
				keyboard_ctl.release(KeyCode.from_vk(event[1][0]))
		else:
			pass
		# delay
		if(counter < len(events) - 1):
			time.sleep(events[counter + 1][0] - events[counter][0])

		counter+=1

	# random sleep
	time.sleep(5 * rand())

# Key control hooks
def on_press(key):
	global recording
	global captured
	global end

	# start recording
	if(not captured and not recording and key.value.vk == 55):
		print('Recording...')
		recording = True

	elif(not captured and recording):
		# stop recording and start replay loop
		if(key.value.vk == 55):
			recording = False
			captured = True
		# capture keyboard event for replay log
		else:
			events.append((time.time(), (key.value.vk, True)))
	# exit program
	elif(captured and key.value.vk == 53):
		end = True

def on_release(key):
	global events
	# log time of keyup
	if(not captured and recording and key.value.vk != 55):
		events.append((time.time(), (key.value.vk, False)))

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)
keyboard_listener.start()

print('Press the cmd key to begin capturing, then press cmd key again to end recording and start replay.')

# wait to start recording
while(not captured):
	pass

mouse_listener.stop()

# countdown to position
print('Starting in...')

for i in range(5):
    print(5 - i)
    time.sleep(1)

print('Pres esc to exit')

while(not end):
	replay()

keyboard_listener.stop()

exit(0)
