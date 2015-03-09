CapitalOne Challenge
Due 3/10/2015
Author: Gary Hoang
==================

Prologue:
 - Program runs only on python 3.
 - Command to run: python capitalone.py
 - Results written to RESULTS.txt
 - states.py must also be in the same directory.
 - The primary file is capitalone.py and states.py is the a file of dictionaries that convert state names to their initials and vice versa.
 - Code (with comments for clarity) is given as well.

Task:
1) Popularity Rank: A list of the most tweeted about best picture nominees (ranked from 1-8) 
	- best picture nominees were:
		Birdman, Whiplash, American Sniper, The Grand Budapest Hotel,
		The Imitation Game, Selma, The Theory of Everything, Boyhood
2) Winner Announcement Prediction: Hour and minute when the winner (Birdman) was mentioned on Twitter most frequently 
3) Location: A list of which states were the most active in tweeting about #TheOscars2015 (rank ordered from most active to least)

Approach:
Reading from csv file, info is in this order:
	0: Time				
	1: ID				
	2: text  			
	3: Retweets			
	4: GeoTag			
	5: PlaceTag			
	6: Favorites		
	7: User names 		
	8: User Location
	9: User ID
	10: Time Zone
	11: User Followers
	12: User Statuses
	13: User Friends
	14: User Handle
	15: HashTags
	16: User Mentions in Tweet

Main Premise:
Strip the fields we are interested in (user location and text) and search through for what we are looking for.

Part 1:
Used a dictionary for finding which best picture nominees were tweeted about the most. 
	- Stripped user text of all punctuation.
	- Account for cases such as mixing American Sniper with the word American by searching for key words.
		- ex. 'sniper', 'theory' - words that must come up when a user tweets about a best picture nominee
	- Extraneous cases further accounted for by simply checking if a keyword is in the stripped down user text.
	- Accounted for cases where people may have written "Birdman, Birdman, Birdman is the BEST!" by using a counter dictionary to only count Birdman once.

Part 2:
Used another dictionary for hour and minute when Birdman was most tweeted about.
	- Hour and minute in a tuple are the key
		- ex. (2, 34) is the key and represents 2:34 
	- Utilizes part 1. Whenever the keyword 'birdman' arises, we find the time the user tweeted and append to our dictionary.
	- At the end, search our dictionary for its greatest value and print out its key.
	- Note: Times given in the csv file (oscar_tweets.csv) are all four hours earlier than PST when the Oscars actually took place. I printed out the given time and added four hours to make it Pacific Standard Time.

Part 3:
Used another dictionary to hold the number of tweets in each state.
	- First stripped user location of punctuation (if there was any) or skip this field if it was empty.
	- Then check if the whole name of state is in the stripped information. If the whole name was given, we add to our dictionary and move on.
		- ex. check if 'New York', 'North Dakota', etc. were in the strings. 
	- If unsuccessful, now search by state initials (ex. CA, NY, etc.). Further reduced possibility that if a user location was, for example, Jordan, that OR (Oregon) did not get added to by checking if each word was equal to two letters. 
	- Flaws: Did not implement a city search, although this one would have been very ideal - https://pypi.python.org/pypi/us. This is ultimately the weakest point of this project.