from pynput.mouse import Button, Controller # DL Module pynput [Win + Mac]
mouse = Controller()
from pynput.keyboard import Key, Controller # DL Module pynput [Win + Mac]
keyboard = Controller()
# from pynput import keyboard # # DL Module pynput [Win + Mac]
import numpy # comes with imagesearch
from PIL import ImageGrab # DL Module Pillow/PIL [Win + Mac + Linux]
import time # built in

"""This Python module is the engine of SweepBot.py.
It fills and refills the array of mine fields to calculate probabilities and find good moves.
I have yet to try out the Max Tree RA, or the human like search in order to optimize the code."""

d, x0, y0, pad = 0, 0, 0, 0 # set from SweepBot.py

def fill_arr_Mine(arr_Mine, getFlags):
	# x col y row
	xn0,yn0,cn0_1,cn0_2 = x0+13,y0+12, (229, 194, 159), (215, 184, 153) # 12,12 # Zero mines 0_1 (229, 194, 159) 0_2 (215, 184, 153) $1:$1048576
	xn1,yn1,cn1 = x0+12,y0+13, (25, 118, 210) # 12,13 # 1 (25, 118, 210)
	xn2,yn2,cn2 = x0+12,y0+18, (56, 142, 60) # 12,18 # 2 (56, 142, 60)
	xn3,yn3,cn3 = x0+14,y0+8, (211, 47, 47) # 14,8 # 3 (211, 47, 47)
	xn4,yn4,cn4 = x0+14,y0+15, (123, 31, 162) # 14,15 # 4 (123, 31, 162)
	xn5,yn5,cn5 = x0+13,y0+7, (255, 143, 0) # 13, 7 # 5 (255, 143, 0)
	xn6,yn6,cn6 = x0+9, y0+14, (0, 151, 167) # 9,14 # 6 (0, 151, 167)
	xn7,yn7,cn7 = x0+12, y0+7, (66, 66, 66) # 12,7 # 6 (0, 151, 167)
	# xn8,yn8,cn8 = x0+c, y0+r, (0, 151, 167) # c,r # 6 (0, 151, 167)
	xnu,ynu,cnu_1,cnu_2 = x0+12,y0+12, (170, 215, 81), (162, 209, 73) # 12,12 # Uncleared field ?_1 (170, 215, 81) light green ?_2 (162, 209, 73) dark green
	xnX,ynX,cnX = x0+11,y0+8, (242, 54, 7) # 11,8 # Flag (242, 54, 7)

	# print(f'getFlags = {getFlags}')
	count = 0
	unrec = 1
	while unrec:
		unrec = 0
		count += 1
		if count > 50:
			return 1 # getting unrec too many times means something is wrong ... exit
		image = ImageGrab.grab()
		for r in range(20): # 20 rows [0-19]
			for c in range(24): # 24 columns [0-23]
				if arr_Mine[r+pad,c+pad] == '-' or arr_Mine[r+pad,c+pad] == ' ': # 
					c1 = image.getpixel((xn1+d*c, yn1+d*r))
					if c1 == cn1: arr_Mine[r+pad,c+pad] = '1'; continue
					# flags used to be here by popularity
					if getFlags == 1:
						cX = image.getpixel((xnX+d*c, ynX+d*r)) # flag/mine x marks the spot # ok to comment out these two line (1 below too) if not pausing in the middle
						# print (f'cX == cnX: {cX} == {cnX} [{r}][{c}]')
						if cX == cnX: arr_Mine[r+pad,c+pad] = '+'; continue # flag/mine x marks the spot
					c2 = image.getpixel((xn2+d*c, yn2+d*r))
					if c2 == cn2: arr_Mine[r+pad,c+pad] = '2'; continue
					c0 = image.getpixel((xn0+d*c, yn0+d*r))
					if c0 == cn0_1 or c0 == cn0_2: arr_Mine[r+pad,c+pad] = ' '; continue
					cu = image.getpixel((xnu+d*c, ynu+d*r)) # unknown/uncleared
					if cu == cnu_1 or cu == cnu_2: arr_Mine[r+pad,c+pad] = '-'; continue # unknown/uncleared
					c3 = image.getpixel((xn3+d*c, yn3+d*r))
					if c3 == cn3: arr_Mine[r+pad,c+pad] = '3'; continue
					c4 = image.getpixel((xn4+d*c, yn4+d*r))
					if c4 == cn4: arr_Mine[r+pad,c+pad] = '4'; continue
					c5 = image.getpixel((xn5+d*c, yn5+d*r))
					if c5 == cn5: arr_Mine[r+pad,c+pad] = '5'; continue
					c6 = image.getpixel((xn6+d*c, yn6+d*r))
					if c6 == cn6: arr_Mine[r+pad,c+pad] = '6'; continue
					c7 = image.getpixel((xn7+d*c, yn7+d*r))
					if c7 == cn7: arr_Mine[r+pad,c+pad] = '7'; continue
					# c8 = image.getpixel((xn8+d*c, yn8+d*r))
					# if c8 == cn8: arr_Mine[r+pad,c+pad] = '8'
					
					# arr_Mine[r+pad,c+pad] = '?'
					unrec = 1 # field not recognized
					# arr_Mine_Flags = arr_Mine == '+'
					# if flags != arr_Mine_Flags.sum(): unrec = 1
	return 0

def lastcheck_popempties(arr_Mine):
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '-':
				mouse.position = (x0+(c)*d+12, y0+(r)*d+12)#; time.sleep(.05)
				mouse.press(Button.left); mouse.release(Button.left)
			else: 
				continue

# ------------------------------- flag/clear (Simple) -------------------------------------------------------------

def flag(arr_Mine, arr_Flags):
	flagged = 0
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '+' or arr_Mine[r+pad,c+pad] == ' ' or arr_Mine[r+pad,c+pad] == '-' or arr_Flags[r+pad,c+pad] == 1: continue
			if arr_Mine[r+pad,c+pad] == '1': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 1); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '2': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 2); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '3': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 3); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '4': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 4); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '5': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 5); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '6': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 6); flagged += f; continue
			if arr_Mine[r+pad,c+pad] == '7': f = flag_by_N(arr_Mine,arr_Flags,r+pad,c+pad, 7); flagged += f
	return flagged

def clear(arr_Mine, arr_Clears):
	cleared = 0
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '+' or arr_Mine[r+pad,c+pad] == ' ' or arr_Mine[r+pad,c+pad] == '-' or arr_Clears[r+pad,c+pad] == 1: continue
			if arr_Mine[r+pad,c+pad] == '1': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 1); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '2': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 2); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '3': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 3); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '4': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 4); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '5': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 5); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '6': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 6); cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '7': cl = clear_by_N(arr_Mine,arr_Clears,r+pad,c+pad, 7); cleared += cl
	return cleared

def flag_by_N(arr_Mine, arr_Flags, r, c, N):
	flagged = 0

	# Count - and +
	X = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '+').sum() # mines touched by N in the 3x3 block around it
	u = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '-').sum() # Uncleared fields touched by N in the 3x3 block around

	# Flag +
	if u + X == N and u > 0:
		for rS in range(r-1, r+2): # rSub
			for cS in range(c-1, c+2): # cSub
				if arr_Mine[rS, cS] == '-':
					arr_Mine[rS, cS] = '+'
					mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12)#; time.sleep(.05)
					mouse.press(Button.right); mouse.release(Button.right)
					# print('mark X [r,c] ', rS, cS)
					flagged += 1
					if flagged == N: break; break # was return flagged # 27

	# Mark if all flags have been set for this N to avoid revisiting
	if X + flagged == N: arr_Flags[r][c] = 1#; print('arr_Flags:'); print(arr_Flags)

	return flagged

def clear_by_N(arr_Mine, arr_Clears, r, c, N):
	cleared = 0

	# Count - and +
	X = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '+').sum() # mines touched by N in the 3x3 block around it
	u = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '-').sum() # Uncleared fields touched by N in the 3x3 block around

	# Clear -
	if X == N and u > 0:
		for rS in range(r-1, r+2): # rSub
			for cS in range(c-1, c+2): # cSub
				if arr_Mine[rS, cS] == '-':
					mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12)#; time.sleep(.05)
					mouse.press(Button.left); mouse.release(Button.left)
					# print('clear u [r,c] ', rS, cS)
					cleared += 1

	# Mark if all empties have been cleared for this N to avoid revisiting
	if u - cleared == 0: arr_Clears[r][c] = 1#; print('arr_Clears:'); print(arr_Clears)

	return cleared

def fill_arrFlags_arrClears_on_startup(arr_Mine, arr_Flags, arr_Clears):
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '+' or arr_Mine[r+pad,c+pad] == ' ' or arr_Mine[r+pad,c+pad] == '-': continue
			if arr_Mine[r+pad,c+pad] == '1': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 1); continue
			if arr_Mine[r+pad,c+pad] == '2': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 2); continue
			if arr_Mine[r+pad,c+pad] == '3': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 3); continue
			if arr_Mine[r+pad,c+pad] == '4': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 4); continue
			if arr_Mine[r+pad,c+pad] == '5': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 5); continue
			if arr_Mine[r+pad,c+pad] == '6': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 6); continue
			if arr_Mine[r+pad,c+pad] == '7': flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 7)

def flag_clear_by_N_on_startup(arr_Mine,arr_Flags,arr_Clears, r, c, N):
	# Count - and +
	X = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '+').sum() # mines touched by N in the 3x3 block around it
	u = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '-').sum() # Uncleared fields touched by N in the 3x3 block around

	# Mark if all flags have been set for this N to avoid revisiting
	if N == X: arr_Flags[r][c] = 1#; print(arr_Flags)
	# Mark if all empties have been cleared for this N to avoid revisiting
	if u == 0: arr_Clears[r][c] = 1#; print(arr_Clears)





# ------------------------------- flag/clear (Prob 3, mines remaining configurations check - if > 1: guess on mine appearing in fewest configurations) -------------------------------------------------------------


# ------------------------------- Prob Massive-------------------------------------------------------------

def arr_Prob_Massive_fill(arr_Mine):
	# for each of the nearby Ns (if they are a number 1-7):
	flagged, cleared = 0, 0
	arr_Prob_Massive = numpy.zeros((20+pad+pad,24+pad+pad), dtype=numpy.double) # alt. dtype=str dtype=int
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '1': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 1); continue
			if arr_Mine[r+pad,c+pad] == '2': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 2); continue
			if arr_Mine[r+pad,c+pad] == '3': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 3); continue
			if arr_Mine[r+pad,c+pad] == '4': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 4); continue
			if arr_Mine[r+pad,c+pad] == '5': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 5); continue
			if arr_Mine[r+pad,c+pad] == '6': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 6); continue
			if arr_Mine[r+pad,c+pad] == '7': arr_Prob_Massive_fill_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 7)

	print(arr_Prob_Massive[2:22, 2:26])
	flagged, cleared = flag_and_clear_arr_Prob_Massive(arr_Mine, arr_Prob_Massive) # this r,c is yielding 0.5s

	return flagged, cleared

def arr_Prob_Massive_fill_by_N(arr_Mine, arr_Prob_Massive, r, c, N):

	# Count - and +
	X, u = 0, 0 # +, - = 0, 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-':
				u += 1
			if arr_Mine[rS, cS] == '+':
				X += 1

	# if N - X > 0 and u - (N - X) == 1: # 2 cells with 1 mine, 3 cells with 2 mines, 4 cells with 3 mines, and so on. The remaining cell can be either cleared or flagged.
	if N - X == 1 and u == 2:
		print(f'Massive Found {u} cells with {N-X} mine(s) at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		for rS in range(r-1, r+2): # rSub
			for cS in range(c-1, c+2): # cSub
				if arr_Mine[rS, cS] == '-':
					arr_Prob_Massive[rS, cS] = 1/2 # if touching 2 cells with prob 1, then touching at least 1 mine for sure.

	return

def flag_and_clear_arr_Prob_Massive(arr_Mine, arr_Prob_Massive):
	# for each of the nearby Ns (if they are a number 1-7):
	flagged, cleared = 0, 0
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '1': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 1); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '2': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 2); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '3': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 3); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '4': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 4); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '5': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 5); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '6': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 6); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '7': f, cl = flag_and_clear_arr_Prob_Massive_by_N(arr_Mine,arr_Prob_Massive,r+pad,c+pad, 7); flagged += f; cleared += cl

	return flagged, cleared

def flag_and_clear_arr_Prob_Massive_by_N(arr_Mine, arr_Prob_Massive, r, c, N):
	flagged, cleared = 0, 0
	# Count - and +
	probHitsFromArr_Prob = 0
	X, u = 0, 0 # +, - = 0, 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-':
				u += 1
			if arr_Mine[rS, cS] == '+':
				X += 1
			probHitsFromArr_Prob += arr_Prob_Massive[rS, cS]

	if u == 5:
		if probHitsFromArr_Prob == 1/2+1/2+1/2+1/2: # definitely touching at least 1
			if N-X-2 == 0: # Clear. The extra mine from Prob satisfies the N requirement and what N is already touching (X)
				# print(F'Clear in flag_and_clear_arr_Prob_x_mines_in_y_cells_by_N. probHitsFromArr_Prob == 2/3 + 2/3. N={N} / arr_Mine[r+pad-1, c+pad-1]={arr_Mine[r, c]}')
				for rS in range(r-1, r+2): # rSub
					for cS in range(c-1, c+2): # cSub
						if arr_Mine[rS, cS] == '-' and arr_Prob_Massive[rS, cS] == 0:
							print(f'probability Massive Clear at [rS-pad+1, cS-pad+1]={[rS-pad+1, cS-pad+1]} / arr_Mine[rS, cS]={arr_Mine[rS, cS]}')
							mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12)#; time.sleep(.05)
							mouse.press(Button.left); mouse.release(Button.left)
							# print('probability clear u [r,c] ', rS, cS)
							cleared += 1

	return flagged, cleared
