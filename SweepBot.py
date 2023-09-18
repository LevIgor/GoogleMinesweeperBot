from pynput.mouse import Button, Controller # DL Module pynput [Win + Mac]
mouse = Controller()
from pynput.keyboard import Key, Controller # DL Module pynput [Win + Mac]
keyboardC = Controller()
from pynput import keyboard # # DL Module pynput [Win + Mac]
from PIL import ImageGrab # DL Module Pillow/PIL [Win + Mac + Linux]
from python_imagesearch.imagesearch import imagesearch # DL Module imagesearch [Win + Mac + Linux]
import numpy # comes with imagesearch [or Pillow]
import time # built in
import sys # built in
import random #built in
import SappArrOps # custom
import SappArrOps_Prob1 # custom
import SappArrOps_Prob2 # custom
import SappArrOps_Prob3 # custom

"""This Python module is the driver seat of SweepBot.
It directs the work of the engine, SappArrOps.py.

Currently it only works on Hard difficulty and in Firefox. Color recognition in SappArrOps module [def fill_arr_Mine(arr_Mine)] needs to be adapted to work in other browsers."""


def on_press(key): # To stop press the LEFT CTRL
	# print (key)
	global keep_going
	if key == keyboard.Key.ctrl_l: # CTRL key on the Left side of the keyboard # key == keyboard.Key.space or key == keyboard.KeyCode.from_char('x') or key == keyboard.KeyCode.from_char('c') or key == keyboard.KeyCode.from_char('v') or key == keyboard.KeyCode.from_char('b')
		keep_going = False
		print('Exiting')
		# keyboardC.press(Key.alt_l)
		# keyboardC.press(Key.tab)
		# keyboardC.release(Key.tab)
		# keyboardC.release(Key.alt_l)
		sys.exit()

def waitloop():
	# Find Play Again button
	pos = imagesearch('./playagain.png', .99)
	loop = 1
	while loop:
		pos = imagesearch('./playagain.png', .99)
		if pos[0] != -1:
			loop = 0
			# print('playagain.png found, position : ', pos[0], pos[1]); xPlayAgain, yPlayAgain = pos[0], pos[1]
			# mouse.position = (xPlayAgain, yPlayAgain)#; time.sleep(0.05)
			# mouse.press(Button.left); mouse.release(Button.left); time.sleep(0.05) #0.1 0.5

def setup_for_play():
	# # Find minefield [Difficulty: Hard only]
	# pos = imagesearch('./anchor.png')
	# if pos[0] != -1: print('anchor.png found, position : ', pos[0], pos[1]); xAnchor, yAnchor = pos[0], pos[1]
	# else: print("can't see game"); sys.exit()
	# x0,y0 = xAnchor-12,yAnchor+48 # set top left corner x,y coordinates based on 'Hard' dropdown menu selection screenshot
	# d = 25
	# pad = 2 # pas 2 rows and 2 columns around the arrays arr_Mine and arr_Prob
	# SappArrOps.d, SappArrOps.x0, SappArrOps.y0, SappArrOps.pad = d, x0, y0, pad # set support module vars
	# SappArrOps_Prob1.d, SappArrOps_Prob1.x0, SappArrOps_Prob1.y0, SappArrOps_Prob1.pad = d, x0, y0, pad # set support module vars
	# SappArrOps_Prob2.d, SappArrOps_Prob2.x0, SappArrOps_Prob2.y0, SappArrOps_Prob2.pad = d, x0, y0, pad # set support module vars
	# SappArrOps_Prob3.d, SappArrOps_Prob3.x0, SappArrOps_Prob3.y0, SappArrOps_Prob3.pad = d, x0, y0, pad # set support module vars

	# Find Try Again button
	pos = imagesearch('./tryagain.png', .99)
	if pos[0] != -1:
		print('tryagain.png found, position : ', pos[0], pos[1]); xTryAgain, yTryAgain = pos[0], pos[1]
		mouse.position = (xTryAgain, yTryAgain)#; time.sleep(0.05)
		mouse.press(Button.left); mouse.release(Button.left); time.sleep(0.05) #0.1 0.5

	# Find Play Again button
	pos = imagesearch('./playagain.png', .99)
	if pos[0] != -1:
		print('playagain.png found, position : ', pos[0], pos[1]); xPlayAgain, yPlayAgain = pos[0], pos[1]
		mouse.position = (xPlayAgain, yPlayAgain)#; time.sleep(0.05)
		mouse.press(Button.left); mouse.release(Button.left); time.sleep(0.05) #0.1 0.5

	# Fill arr_Mine
	arr_Mine = numpy.zeros((20+pad+pad,24+pad+pad), dtype=str); arr_Mine[:] = ' ' # alt. dtype=int
	arr_Mine[2:22, 2:26] = '-' # pad_1_zero
	do_setup_for_play = SappArrOps.fill_arr_Mine(arr_Mine, 1) # returns 0 on success, 1 on failure fill_arr_Mine(arr_Mine, getFlags [1 = yes, 0 = no])
	# print(numpy.array2string(arr_Mine[2:22, 2:26], formatter={'str_kind':lambda x: x}))
	
	# Fill support arrays arr_Flags and arr_Clears
	arr_Flags = numpy.zeros((20+pad+pad,24+pad+pad), dtype=int) # alt. dtype=str
	arr_Flags[2:22, 2:26] = 0 # pad_1_zero
	arr_Clears = numpy.zeros((20+pad+pad,24+pad+pad), dtype=int) # alt. dtype=str
	arr_Clears[2:22, 2:26] = 0 # pad_1_zero
	# if arr_Mine '-' == 480 [Hard diff] then starting fresh - random click then initial flag, otherwise fill arr_Flags and arr_Clear and set flags via arr_Mine.sum()

	if (arr_Mine == '-').sum() == 480:
		# Start game at random field
		mouse.position = (x0+d*random.randrange(0,23+1), y0+d*random.randrange(0,19+1)); time.sleep(0.15) # 1st cell at x0,y0 + distance_of_each_cell * randcell#
		mouse.press(Button.left); mouse.release(Button.left)
		mouse.position = (x0-12, y0-12); time.sleep(0.05) #0.1 0.5
		while (arr_Mine == '-').sum() == 480:
			do_setup_for_play = SappArrOps.fill_arr_Mine(arr_Mine, 1)
		# run initial flagging 
		flagged = SappArrOps.flag(arr_Mine, arr_Flags)
		flags = 0
		flags += flagged
		# flaggedProb1, clearedProb1 = SappArrOps_Prob1.flag_and_clear_arr_Prob(arr_Mine)
	else:
		SappArrOps.fill_arrFlags_arrClears_on_startup(arr_Mine, arr_Flags, arr_Clears)
		flags = (arr_Mine == '+').sum()
		flagged = 0
		# print('arr_Flags:')
		# print(arr_Flags[2:22, 2:26])
		# print('arr_Clears:')
		# print(arr_Clears[2:22, 2:26])
	return arr_Mine, arr_Flags, arr_Clears, flagged, flags, do_setup_for_play, x0, y0


# Find minefield [Difficulty: Hard only]
pos = imagesearch('./anchor2.png', .99)
if pos[0] != -1: print('anchor.png found, position : ', pos[0], pos[1]); xAnchor, yAnchor = pos[0], pos[1]
else: print("can't see game"); sys.exit()
x0,y0 = xAnchor-12,yAnchor+48 # set top left corner x,y coordinates based on 'Hard' dropdown menu selection screenshot
d = 25
pad = 2 # pas 2 rows and 2 columns around the arrays arr_Mine and arr_Prob
SappArrOps.d, SappArrOps.x0, SappArrOps.y0, SappArrOps.pad = d, x0, y0, pad # set support module vars
SappArrOps_Prob1.d, SappArrOps_Prob1.x0, SappArrOps_Prob1.y0, SappArrOps_Prob1.pad = d, x0, y0, pad # set support module vars
SappArrOps_Prob2.d, SappArrOps_Prob2.x0, SappArrOps_Prob2.y0, SappArrOps_Prob2.pad = d, x0, y0, pad # set support module vars
SappArrOps_Prob3.d, SappArrOps_Prob3.x0, SappArrOps_Prob3.y0, SappArrOps_Prob3.pad = d, x0, y0, pad # set support module vars

# Main Loop
gamesFinished = 0
gamesProb1, gamesProb2 = 0, 0
did_prob1, did_prob2 = 0, 0
countGames = 0
do_setup_for_play = 1
keep_going = True
with keyboard.Listener(on_press=on_press) as listener:
	while keep_going:
		if do_setup_for_play == 1:
			passes = 0
			print('initial setup')
			if countGames == 1:
				gamesFinished += 1
				if did_prob1 > 0: gamesProb1 += 1
				if did_prob2 > 0: gamesProb2 += 1
				did_prob1, did_prob2 = 0, 0
				countGames = 0
			if gamesFinished > 0: waitloop() # let the flowers grow
			arr_Mine, arr_Flags, arr_Clears, flagged, flags, do_setup_for_play, x0, y0 = setup_for_play()
		if flags == 99:
			if countGames == 1:
				gamesFinished += 1
				if did_prob1 > 0: gamesProb1 += 1
				if did_prob2 > 0: gamesProb2 += 1
				did_prob1, did_prob2 = 0, 0
				countGames = 0
			SappArrOps.lastcheck_popempties(arr_Mine)
			print(f'done! flags = {99-flags}. gamesFinished = {gamesFinished} gamesProb1 = {gamesProb1} gamesProb2 = {gamesProb2}')
			# keep_going = False
			waitloop() # let the flowers grow
			arr_Mine, arr_Flags, arr_Clears, flagged, flags, do_setup_for_play, x0, y0 = setup_for_play()
		
		countGames = 1

		# simple flag and clear
		if flags < 99 and do_setup_for_play == 0:
			cleared = 1
			while cleared:
				cleared = SappArrOps.clear(arr_Mine, arr_Clears)
				mouse.position = (x0-12, y0-12); time.sleep(.05) #.10 0.15 # sleep to let animations play out before refilling arr_Mine
				do_setup_for_play = SappArrOps.fill_arr_Mine(arr_Mine, 0)
				print(numpy.array2string(arr_Mine[2:22, 2:26], formatter={'str_kind':lambda x: x}))
				# the 2 lines below used to be outside the loop
				flagged = SappArrOps.flag(arr_Mine, arr_Flags) # 1
				flags += flagged # 2
				print(f'flags = {flags}, flags remaining = {99-flags}. gamesFinished = {gamesFinished} gamesProb1 = {gamesProb1} gamesProb2 = {gamesProb2}')
			# print(numpy.array2string(arr_Mine[2:22, 2:26], formatter={'str_kind':lambda x: x}))
			# print(f'flags = {flags}, flags remaining = {99-flags}')
		
		# probability 1 array flag and clear
		if flags < 99 and do_setup_for_play == flagged == cleared == 0:
			flaggedProb1, clearedProb1 = SappArrOps_Prob1.Prob1_flag_clear_For_Each_Parent_In_arr_Mine(arr_Mine, arr_Flags, arr_Clears)
			if flaggedProb1 > 0 or clearedProb1 > 0: did_prob1 = 1
			flags += flaggedProb1
			mouse.position = (x0-12, y0-12); time.sleep(.05) #.10 0.15 # sleep to let animations play out before refilling arr_Mine 
			do_setup_for_play = SappArrOps.fill_arr_Mine(arr_Mine, 0)
			print(numpy.array2string(arr_Mine[2:22, 2:26], formatter={'str_kind':lambda x: x}))
			print(f'flags [after probability] = {flags}, flags remaining = {99-flags}. gamesFinished = {gamesFinished} gamesProb1 = {gamesProb1} gamesProb2 = {gamesProb2}')

		# probability 2 arrays combined flag and clear
		if flags < 99 and do_setup_for_play == flagged == cleared == flaggedProb1 == clearedProb1 == 0:
				flaggedProb2, clearedProb2 = SappArrOps_Prob2.Prob2_flag_clear_For_Each_Parent_In_arr_Mine(arr_Mine, arr_Flags, arr_Clears)
				if flaggedProb2 > 0 or clearedProb2 > 0: did_prob2 = 1
				flags += flaggedProb2
				mouse.position = (x0-12, y0-12); time.sleep(.05) #.10 0.15 # sleep to let animations play out before refilling arr_Mine
				if passes == 2:
					do_setup_for_play = SappArrOps.fill_arr_Mine(arr_Mine, 0)
				passes+=1
				print(numpy.array2string(arr_Mine[2:22, 2:26], formatter={'str_kind':lambda x: x}))
				print(f'flags [after probability 2] = {flags}, flags remaining = {99-flags}. gamesFinished = {gamesFinished} gamesProb1 = {gamesProb1} gamesProb2 = {gamesProb2}')

		if flags < 99 and do_setup_for_play == flagged == cleared == flaggedProb1 == clearedProb1 == flaggedProb2 == clearedProb2 == 0:
			if passes == 2:
				print('out of moves')
				sys.exit()

		# # massive probability array flag and clear
		# if flags < 99 and do_setup_for_play == 0:
		# 	if flagged == cleared == flaggedProb == clearedProb == 0:
		# 		flaggedProbMassive, clearedMassive = SappArrOps.arr_Prob_Massive_fill(arr_Mine)
		# 		flags += flaggedProbMassive

	listener.join()







