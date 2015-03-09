"""
CapitalOne Challenge
Due 3/10/2015
Author: Gary Hoang
"""

import csv 
import string
import operator 
from states import states_to_letters, letters_to_states

# nominees
MAP = {'birdman': "Birdman", 'whiplash': "Whiplash", 
	   'sniper': "American Sniper",
	   'budapest': "The Grand Budapest Hotel",
	   'imitation': "The Imitation Game", 'selma':"Selma", 
	   'theory': "The Theory of Everything", 
	   'boyhood': "Boyhood"}

# empty dictionaries
nominees = {} # nominee counters
counters = {} # so we don't count a movie twice in one line
birdman_times = {} # dictionary to hold all of the times Birdman was tweeted about
states = {} # dictionary to hold the number of times a state tweeted through out the Oscars

def keywithmaxval(dic):
    """ 
    input is a dictionary and returns the key with the 
    greatest value.
    """  
    vals = list(dic.values())
    keys = list(dic.keys())
    return keys[vals.index(max(vals))]

def dictreset(dic):
	"""
	input is dictionary and resets all values in dictionary.
	preserves keys.
	"""
	for elem in dic.keys():
		dic[elem] = 0

def printmaxtomin(dic, string, conver_dic, text):
	"""
	input is dictionary and prints out 
	all keys from key with biggest value to key with smallest value
	"""
	print(string, file=text)
	# get dictionary values, get rid of duplicates, turn to list
	# use sorted to sort from biggest to smallest
	values = sorted(list(set(dic.values())), reverse=True)
	keys = []
	for v in values:
		for key,value in dic.items():
			if v == value:
				keys.append(key)
	counter = 1
	for k in keys:
		print(str(counter) + ": " + conver_dic[k], file=text)
		counter += 1

# Used to strip each message of all characters except for letters 
elim = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() else ' ' for c in range(256))

def main():
	print("Program Started. Please wait a while.")
	for nominee in MAP:
		nominees[nominee] = 0
		counters[nominee] = 0

	for state in letters_to_states.keys():
		states[state] = 0

	reader = csv.reader(open('oscar_tweets.csv', "rt", encoding="utf8", newline=''), dialect="excel")
	data = [line for line in reader]
	
	for line in data[1:]:
		# look at what each user wrote in their tweet
		string = line[2]
		string = string.translate(elim).lower().split()
		for key in nominees.keys():
			for word in string:
				# checking on the go
				if len(word) <= 4:
					continue
				if counters[key] == 0:
					if key in word:
						nominees[key] += 1
						counters[key] += 1
						if key == 'birdman':
							time = line[0].split()[3].split(':')
							hour = time[0]
							minute = time[1]
							tup = (hour, minute)
							if tup in birdman_times:
								birdman_times[tup] += 1
							else:
								birdman_times[tup] = 1

		# looking for states now!
		location = line[8]
		location_counter = 0
		if location: # so not an empty string!!
			location = location.translate(elim).lower()
			# to test states like "New York" and "North Dakota"
			for state in states_to_letters.keys():
				if state.lower() in location:
					states[states_to_letters[state]] += 1
					location_counter = 1
			# now testing by two letter intials
			if not location_counter:
				for word in location:
					if location_counter:
						break
					if len(word) == 2:
						if word.upper() in letters_to_states.keys():
							states[word.upper()] += 1
							location_counter = 1
							break;

		# reset our counter dictionaries
		dictreset(counters)

	# write our results to RESULTS.txt
	with open("RESULTS.txt", "w") as text_file:
		print("RESULTS:", file=text_file)
		print("==================", file=text_file)
		printmaxtomin(nominees, "Part 1: Popularity Ranking of Oscar Nominees 2015\n From most popular to least", MAP, text_file)
		print("==================", file=text_file)
		print("Part 2: Time Birdman was most tweeted about", file=text_file)
		time = keywithmaxval(birdman_times)
		print("Most Tweeted about moment: " + str(int(time[0])) + ":" + time[1] + "PM or " + str(int(time[0])+4) + ":" + time[1] + "PM PST", file=text_file)
		print("==================", file=text_file)
		# not including Washington DC.
		printmaxtomin(states, "Part 3: State Activity\n From Twitter Storm to Desert", letters_to_states, text_file)
		
	print("Finished Computuations. Gathered Results and wrote them to RESULTS.txt")

main()