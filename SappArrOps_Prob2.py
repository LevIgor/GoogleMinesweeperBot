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


# ------------------------------- flag/clear (Prob 2, probability array pairs from a pool of 24 arrays of a 5x5 block excluding self/center) -------------------------------------------------------------

# iterate parents
def Prob2_flag_clear_For_Each_Parent_In_arr_Mine(arr_Mine, arr_Flags, arr_Clears):
	# for each of the nearby Ns (if they are a number 1-7):
	flagged, cleared = 0, 0
	for r in range(20):
		for c in range(24):
			if arr_Mine[r+pad,c+pad] == '+' or arr_Mine[r+pad,c+pad] == ' ' or arr_Mine[r+pad,c+pad] == '-' or arr_Flags[r+pad,c+pad] == 1 or arr_Clears[r+pad,c+pad] == 1: continue # Check if it's not a number or all flagged up first
			if arr_Mine[r+pad,c+pad] == '1': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 1); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '2': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 2); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '3': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 3); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '4': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 4); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '5': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 5); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '6': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 6); flagged += f; cleared += cl; continue
			if arr_Mine[r+pad,c+pad] == '7': f, cl = Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine,arr_Flags,arr_Clears,r+pad,c+pad, 7); flagged += f; cleared += cl
	return flagged, cleared

# iterate parents' children (5x5 block around parent, create array of pointers (use isinstance when parsing until int0/empty), fill each arr_Prob2, figure out how to pass cXrem and cU, maybe via fractions in arr_Prob2?)
def Prob2_flag_clear_fill_arr_Prob2s_for_1_pN(arr_Mine, arr_Flags, arr_Clears, pR, pC, pN):
	# print(f'in Prob2_flag_clear_fill_arr_Prob2s_for_1_pN arr_Mine[{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}, pXrem = {pXrem}, pU = {pU}') # *********************************for*debug
	flagged, cleared = 0, 0

	# Get parent'd info: Count - and +
	pX = (arr_Mine[pR-1:pR-1+3, pC-1:pC-1+3] == '+').sum()
	pXrem = pN - pX # Remaining mines touched by parent N in the 3x3 block around it
	pU = (arr_Mine[pR-1:pR-1+3, pC-1:pC-1+3] == '-').sum()
	pUextra = pU - pXrem # u - (N - X) Extra uncleared fields touched by parent N in the 3x3 block around it where the remainign mines could lie
	# print(f'prob1: Found {u} cells with {pXrem} mine(s) at [{r-pad+1},{c-pad+1}] = {arr_Mine[r, c]}')
	count = 0

	# iterate children for pN
	if pUextra > 0: # this is the same as checking arr_Flags and arr_Clears, but is again done here to let prob work be done even if the main flag_clear hasn't caught it # originally if N - X > 0 and u - (N - X) == 1: # 2 cells with 1 mine, 3 cells with 2 mines, 4 cells with 3 mines, and so on. The remaining cell can be either cleared or flagged.
		arr_Prob2_pointers = numpy.zeros(24, dtype=object) # 5x5 block excluding the self
		arr_Prob2_cXrem = numpy.zeros(24, dtype=int) # alt. dtype=str dtype=int dtype=numpy.double dtype=object
		arr_Prob2_cU = numpy.zeros(24, dtype=int) # alt. dtype=str dtype=int dtype=numpy.double dtype=object
		# count = 0
		for rS in range(pR-2, pR+3):
			for cS in range(pC-2, pC+3):
				# print(f'    prob2: cN [{rS-pad+1}][{cS-pad+1}] = {arr_Mine[rS, cS]} arr_Flags[rS, cS] = {arr_Flags[rS, cS]} arr_Clears[r+pad,c+pad] = {arr_Clears[r+pad,c+pad]}') # *********************************for*debug
				if arr_Mine[rS, cS] == '+' or arr_Mine[rS, cS] == ' ' or arr_Mine[rS, cS] == '-' or arr_Flags[rS, cS] == 1 or arr_Clears[rS, cS] == 1: continue # skip non-numeric and flagged/cleared cells
				if rS == pR and cS == pC: continue # skip parent
				if arr_Mine[rS, cS] == '1': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 1); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 1', rS, cS)
				if arr_Mine[rS, cS] == '2': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 2); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 2', rS, cS)
				if arr_Mine[rS, cS] == '3': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 3); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 3', rS, cS)
				if arr_Mine[rS, cS] == '4': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 4); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 4', rS, cS)
				if arr_Mine[rS, cS] == '5': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 5); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 5', rS, cS)
				if arr_Mine[rS, cS] == '6': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 6); continue #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 6', rS, cS)
				if arr_Mine[rS, cS] == '7': count = fill_arr_Prob2_for_1_cN(arr_Mine, rS, cS, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, 7) #; print('calling Prob2_flag_clear_by_cN: N, rS, cS = 7', rS, cS)

	# iterate pointers array
	if count > 1:
		flagged, cleared = Prob2_flag_clear_combine_2_cN(arr_Mine, pR, pC, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, pXrem, pU)

	return flagged, cleared

# for each child create an arr_Prob2 and store it's pointer in an array of painters (arr_Prob2_pointers)
def fill_arr_Prob2_for_1_cN(arr_Mine, cR, cC, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, count, cN): #pN is parentN
	# Count - and +
	cX = (arr_Mine[cR-1:cR-1+3, cC-1:cC-1+3] == '+').sum()
	cXrem = cN - cX # Remaining mines touched by child N in the 3x3 block around it
	cU = (arr_Mine[cR-1:cR-1+3, cC-1:cC-1+3] == '-').sum()
	cUextra = cU - cXrem # u - (N - X) Extra uncleared fields touched by child N in the 3x3 block around it where the remainign mines could lie
	
	if cUextra > 0: # this is the same as checking arr_Flags and arr_Clears, but is again done here to let prob work be done even if the main flag_clear hasn't caught it # originally if N - X > 0 and u - (N - X) == 1: # 2 cells with 1 mine, 3 cells with 2 mines, 4 cells with 3 mines, and so on. The remaining cell can be either cleared or flagged.
		arr_Prob2 = numpy.zeros((20+pad+pad,24+pad+pad), dtype=int) # alt. dtype=str dtype=int dtype=numpy.double
		for rS in range(cR-1, cR+2): # rSub
			for cS in range(cC-1, cC+2): # cSub
				if arr_Mine[rS, cS] == '-':
					arr_Prob2[rS, cS] = 1 # if touching 2 cells with prob 1, then touching at least 1 mine for sure.
		arr_Prob2_pointers[count] = arr_Prob2
		arr_Prob2_cXrem[count] = cXrem
		arr_Prob2_cU[count] = cU
		count += 1

	return count

# iterate arr_Prob2_pointers array combining two at a time
def Prob2_flag_clear_combine_2_cN(arr_Mine, pR, pC, arr_Prob2_pointers, arr_Prob2_cXrem, arr_Prob2_cU, pXrem, pU):
	flagged, cleared = 0, 0
	for i in range(25):
		if isinstance(arr_Prob2_pointers[i+1], numpy.ndarray):
			f, cl = Prob2_flag_clear_by_pN(arr_Mine, pR, pC, pXrem, pU, arr_Prob2_pointers[i], arr_Prob2_cXrem[i], arr_Prob2_cU[i], arr_Prob2_pointers[i+1], arr_Prob2_cXrem[i+1], arr_Prob2_cU[i+1])
			flagged += f; cleared += cl
		else:
			break # reached end or only one child
	return flagged, cleared

# check if two children's probabilities satisfy parent's needs (flag/clear)
def Prob2_flag_clear_by_pN(arr_Mine, pR, pC, pXrem, pU, arr_Prob2_c1, cXrem_1, cU_1, arr_Prob2_c2, cXrem_2, cU_2):
# def Prob2_flag_clear_by_pN(arr_Mine, arr_Prob2, pR, pC, r, c, pXrem, pU, cN):
	flagged, cleared, pProbHits_c1, pProbHits_c2 = 0, 0, 0, 0

	# check if arr_Prob2_c1 and arr_Prob2_c2 step on each others' toes. Will forgo overlap merging until I get cases with an overlap merge need.
	arr_Prob2_c1_AND_c2 = numpy.bitwise_and(arr_Prob2_c1, arr_Prob2_c2)
	andCheck = numpy.all(arr_Prob2_c1_AND_c2 == 0)
	if andCheck == 0: # no overlap
		#pProbHits: pProbHits_c1 and pProbHits_c2
		for rS in range(pR-1, pR+2): # rSub
			for cS in range(pC-1, pC+2): # cSub
				if arr_Prob2_c1[rS, cS] == 1: pProbHits_c1 += 1
		for rS in range(pR-1, pR+2): # rSub
			for cS in range(pC-1, pC+2): # cSub
				if arr_Prob2_c2[rS, cS] == 1: pProbHits_c2 += 1
		pUextra = pU - pProbHits_c1 - pProbHits_c2
	
		# Clears
		    # if you're touching 2 cells with 1 mine and you need 1 mine and you have extra cells, then clear the extra cells
		# 1
		if pXrem == 2 and pUextra > 0:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		# 2
		if pXrem == 2 and pUextra > 0:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 2 and cU_2 == 3 and pProbHits_c2 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		if pXrem == 2 and pUextra > 0:
			if cXrem_1 == 2 and cU_1 == 3 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		# 3
		if pXrem == 3 and pUextra > 0:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 2 and cU_2 == 3 and pProbHits_c2 == 3:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		if pXrem == 3 and pUextra > 0:
			if cXrem_2 == 2 and cU_2 == 3 and pProbHits_c2 == 3:
				if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		# 4
		if pXrem == 2 and pUextra > 0:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 2 and cU_2 == 3 and pProbHits_c2 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		if pXrem == 2 and pUextra > 0:
			if cXrem_1 == 2 and cU_1 == 3 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'CLEAR Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					cleared += prob2Clear(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)

		# Flags
		# 1
		if pXrem == 3 and pUextra == 1:
			if cXrem_1 == 1 and cU_1 == 3 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'FLAG Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					flagged += prob2Flag(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		if pXrem == 3 and pUextra == 1:
			if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
				if cXrem_1 == 1 and cU_1 == 3 and pProbHits_c1 == 2:
					print(f'FLAG Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					flagged += prob2Flag(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		# 2
		if pXrem == 3 and pUextra == 1:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'FLAG Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					flagged += prob2Flag(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		# 3
		if pXrem == 3 and pUextra == 1:
			if cXrem_1 == 1 and cU_1 == 2 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 4 and pProbHits_c2 == 2:
					print(f'FLAG Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					flagged += prob2Flag(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)
		if pXrem == 3 and pUextra == 1:
			if cXrem_1 == 1 and cU_1 == 4 and pProbHits_c1 == 2:
				if cXrem_2 == 1 and cU_2 == 2 and pProbHits_c2 == 2:
					print(f'FLAG Prob2_Parent found with {pXrem} mine(s) in {pU} cells at [{pR-pad+1},{pC-pad+1}] = {arr_Mine[pR, pC]}')
					flagged += prob2Flag(arr_Mine, arr_Prob2_c1_AND_c2, pR, pC)

	return flagged, cleared

def prob2Clear(arr_Mine, arr_Prob2, r, c):
	cleared = 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-' and arr_Prob2[rS, cS] == 0:
				# print(f'            prob2 Clear at [rS-pad+1, cS-pad+1]={[rS-pad+1, cS-pad+1]} / arr_Mine[rS, cS]={arr_Mine[rS, cS]}')
				mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12); time.sleep(2)#; time.sleep(.05)
				mouse.press(Button.left); mouse.release(Button.left)
				cleared += 1
	return cleared
def prob2Flag(arr_Mine, arr_Prob2, r, c):
	flagged = 0
	for rS in range(r-1, r+2): # rSub
		for cS in range(c-1, c+2): # cSub
			if arr_Mine[rS, cS] == '-' and arr_Prob2[rS, cS] == 0:
				# print(f'            prob2 Flag at [rS-pad+1, cS-pad+1]={[rS-pad+1, cS-pad+1]} / arr_Mine[rS, cS]={arr_Mine[rS, cS]}')
				arr_Mine[rS, cS] = '+'
				mouse.position = (x0+(cS-pad)*d+12, y0+(rS-pad)*d+12); time.sleep(2)#; time.sleep(.05)
				mouse.press(Button.right); mouse.release(Button.right)
				flagged += 1
	return flagged
