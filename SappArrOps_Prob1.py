
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


# ------------------------------- flag/clear (Prob 1) -------------------------------------------------------------

# iterate parents
def Prob1_flag_clear_For_Each_Parent_In_arr_Mine(arr_Mine, arr_Flags, arr_Clears):
	# for each of the nearby Ns (if they are a number 1-7):
	flagged, cleared = 0, 0
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '+' or arr_Mine[r+pad,c+pad] == ' ' or arr_Mine[r+pad,c+pad] == '-' or arr_Flags[r+pad,c+pad] == 1 or arr_Clears[r+pad,c+pad] == 1: continue # Check if it's not a number or all flagged up first
			if arr_Mine[r+pad,c+pad] == '1': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 1); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '2': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 2); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '3': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 3); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '4': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 4); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '5': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 5); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '6': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 6); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '7': f, cl = Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 7); flagged += f; cleared += cl
	return flagged, cleared

# get parent's mines in cells (probabilities/arr_Prob1)
def Prob1_flag_clear_fill_arr_Prob_for_1_pN(arr_Mine, arr_Flags, arr_Clears, r, c, pN): #pN is parentN
	flagged, cleared = 0, 0
	
	# Count - and +
	# pX, pXrem, pU, pUextra = 0, 0, 0, 0
	pX = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '+').sum()
	pXrem = pN - pX # Remaining mines touched by parent N in the 3x3 block around it
	pU = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '-').sum()
	pUextra = pU - pXrem # u - (N - X) Extra uncleared fields touched by parent N in the 3x3 block around it where the remainign mines could lie
	# print(f'prob1: Found {u} cells with {pXrem} mine(s) at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')

	if pUextra > 0: # this is the same as checking arr_Flags and arr_Clears, but is again done here to let prob work be done even if the main flag_clear hasn't caught it # originally if N - X > 0 and u - (N - X) == 1: # 2 cells with 1 mine, 3 cells with 2 mines, 4 cells with 3 mines, and so on. The remaining cell can be either cleared or flagged.
		arr_Prob1 = numpy.zeros((20+pad+pad,24+pad+pad), dtype=int) # alt. dtype=str dtype=int dtype=numpy.double
		# prob = (N-X)/u
		for rS in range(r-1, r+2): # rSub
			for cS in range(c-1, c+2): # cSub
				if arr_Mine[rS, cS] == '-':
					arr_Prob1[rS, cS] = 1 # if touching 2 cells with prob 1, then touching at least 1 mine for sure.
		flagged, cleared = Prob1_flag_clear_For_Each_Child_in_5x5block_around_parent(arr_Mine, arr_Flags, arr_Clears, arr_Prob1, r, c, pXrem, pU) # this r,c is yielding 0.5s

	return flagged, cleared

# iterate parents' children (5x5 block around parent)
def Prob1_flag_clear_For_Each_Child_in_5x5block_around_parent(arr_Mine, arr_Flags, arr_Clears, arr_Prob1, r, c, pXrem, pU):
	# print(f'in Prob1_flag_clear_For_Each_Child_in_5x5block_around_parent arr_Mine[{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}, pXrem = {pXrem}, pU = {pU}') # *********************************for*debug
	# for each of the nearby Ns (if they are a number 1-7):
	flagged, cleared = 0, 0
	for rS in range(r-2, r+3):
		for cS in range(c-2, c+3):
			# print(f'    prob1: cN [{rS-pad+1}][{cS-pad+1}] = {arr_Mine[rS, cS]} arr_Flags[rS, cS] = {arr_Flags[rS, cS]} arr_Clears[r+pad,c+pad] = {arr_Clears[r+pad,c+pad]}') # *********************************for*debug
			if arr_Mine[rS, cS] == '+' or arr_Mine[rS, cS] == ' ' or arr_Mine[rS, cS] == '-' or arr_Flags[rS, cS] == 1 or arr_Clears[rS, cS] == 1: continue # skip non-numeric and flagged/cleared cells
			if rS == r and cS == c: continue # skip parent
			if arr_Mine[rS, cS] == '1': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 1); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 1', rS, cS)
			if arr_Mine[rS, cS] == '2': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 2); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 2', rS, cS)
			if arr_Mine[rS, cS] == '3': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 3); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 3', rS, cS)
			if arr_Mine[rS, cS] == '4': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 4); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 4', rS, cS)
			if arr_Mine[rS, cS] == '5': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 5); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 5', rS, cS)
			if arr_Mine[rS, cS] == '6': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 6); flagged += f; cleared += cl; continue #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 6', rS, cS)
			if arr_Mine[rS, cS] == '7': f, cl = Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, r, c, rS, cS, pXrem, pU, 7); flagged += f; cleared += cl #; print('calling Prob1_flag_clear_by_cN: N, rS, cS = 7', rS, cS)
	return flagged, cleared

# check if parent's probabilities satisfy child's needs (flag/clear)
def Prob1_flag_clear_by_cN(arr_Mine, arr_Prob1, pR, pC, r, c, pXrem, pU, cN):
	flagged, cleared, cProbHits = 0, 0, 0

	# Count - and +
	cXrem = cN - (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '+').sum() # Remaining mines touched by child N in the 3x3 block around it
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Prob1[rS, cS] == 1: cProbHits += 1
	cU = (arr_Mine[r-1:r-1+3, c-1:c-1+3] == '-').sum() # Uncleared fields touched by child N in the 3x3 block around it but not with mines
	cUextra = cU - cProbHits
	# print(f'        prob1: pXrem = {pXrem} and pU = {pU} and cProbHits = {cProbHits} and cXrem = {cXrem} and cUextra = {cUextra}') # *********************************for*debug
	
	# Clears
	    # if you're touching 2 cells with 1 mine and you need 1 mine and you have extra cells, then clear the extra cells
	# 1
	if pXrem == 1 and pU == 2 and cProbHits == 2 and cXrem == 1 and cUextra > 0: # [pXrem == 1 and pU == 2] is 1 mine in 2 cells of parent or probability of 1/2. cProbHits == 2 means child is touching both cells with 1/2
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)
	# 2
	if pXrem == 1 and pU == 3 and cProbHits == 3 and cXrem == 1 and cUextra > 0:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)
	# 3
	if pXrem == 2 and pU == 4 and cProbHits == 3 and cXrem == 1 and cUextra > 0:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)
	# 4
	if pXrem == 2 and pU == 3 and cProbHits == 2 and cXrem == 1 and cUextra > 0:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)
	# 5
	if pXrem == 2 and pU == 3 and cProbHits == 3 and cXrem == 2 and cUextra > 0:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)
	# 6
	if pXrem == 3 and pU == 4 and cProbHits == 3 and cXrem == 2 and cUextra > 0:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      CLEAR Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		cleared += prob1Clear(arr_Mine, arr_Prob1, r, c)

	# Flags
	# 1
	if pXrem == 1 and pU == 3 and cProbHits == 2 and cXrem == 2 and cUextra == 1:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)
	# 2
	if pXrem == 1 and pU == 2 and cProbHits == 2 and cXrem == 2 and cUextra == 1:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)
	# 3
	if pXrem == 1 and pU == 3 and cProbHits == 2 and cXrem == 3 and cUextra == 2:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)
	# 4
	if pXrem == 1 and pU == 2 and cProbHits == 2 and cXrem == 4 and cUextra == 3:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)
	# 4
	if pXrem == 1 and pU == 2 and cProbHits == 2 and cXrem == 3 and cUextra == 2:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)
	# 5 Parent here is Probability Child in Prob2
	if pXrem == 1 and pU == 3 and cProbHits == 3 and cXrem == 2 and cUextra == 1:
		print(f'Prob1_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
		print(f'      FLAG Prob1_Child found with {cXrem} mine(s) in {cU} cells at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
		flagged += prob1Flag(arr_Mine, arr_Prob1, r, c)

	return flagged, cleared

def prob1Clear(arr_Mine, arr_Prob1, r, c):
	cleared = 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-' and arr_Prob1[rS, cS] == 0:
				# print(f'            prob1 Clear at [rS-pad+1, cS-pad+1]={[rS-pad+1, cS-pad+1]} / arr_Mine[rS, cS]={arr_Mine[rS, cS]}')
				mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12)#; time.sleep(1)#; time.sleep(.05)
				mouse.press(Button.left); mouse.release(Button.left)
				cleared += 1
	return cleared
def prob1Flag(arr_Mine, arr_Prob1, r, c):
	flagged = 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-' and arr_Prob1[rS, cS] == 0:
				# print(f'            prob1 Flag at [rS-pad+1, cS-pad+1]={[rS-pad+1, cS-pad+1]} / arr_Mine[rS, cS]={arr_Mine[rS, cS]}')
				arr_Mine[rS, cS] = '+'
				mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12)#; time.sleep(1)#; time.sleep(.05)
				mouse.press(Button.right); mouse.release(Button.right)
				flagged += 1
	return flagged
