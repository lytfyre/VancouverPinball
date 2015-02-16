"""
Outputs a markdown formated results table from a folder of cleaned up brackelope results.
Expects a folder of .txt files of results
file names lexographicly ordered as they should appear in the table
each line must be of the form "POSITION# PLAYER_NAME"
a line in the file shall have no lines preceding it with a better finish. (but may have preceding tied lines)
"""
FIRST_PLACE_SCORE = 20.0
SECOND_PLACE_SCORE = 17.0
STANDARD_SCORES_START = 15.0
MULLIGAN_WEEKS = 0

import glob

def score(previous_band_score, current_band_size, score_band):
	#print score_band
	if score_band == 1:
		return FIRST_PLACE_SCORE
	elif score_band == 2:
		return SECOND_PLACE_SCORE
	elif score_band == 3:
		return STANDARD_SCORES_START - (0.5*(current_band_size - 1))
	else: 
		return previous_band_score - (0.5*(current_band_size - 1)) - 1 


files = glob.glob("*.txt")

players = {}
weeks = 0

for week_number,filename in enumerate(files):
	weeks += 1
	weekly_results = []

	score_band_sizes = {}
	with open(filename) as f:
		last_finish = 0
		score_band = 0
		
		for line in f:
			finish,player = line.strip().split(' ', 1)
			
			if last_finish != finish:
				score_band +=1
				score_band_sizes[score_band] = 0
			score_band_sizes[score_band] +=1 

			last_finish = finish
			weekly_results.append( (player,score_band) )

	band_scores = {}
	for player,band in weekly_results:
		if not band in band_scores:
			band_scores[band] = score(band_scores.get(band-1,0), score_band_sizes[band], band)
		if player not in players:
			players[player] = {}
		players[player][week_number] = band_scores[band]

# generate player totals
player_totals = {}
for player in players.keys():
	# fill with 0s for weeks that other players have results for.
	for week in range(0,weeks):
		if week not in players[player]:
			players[player][week] = 0
	points = []
	for week in sorted(players[player].keys()):
		points.append(players[player][week])
	points.sort()
	player_totals[player] = sum(points[MULLIGAN_WEEKS-1:])


# Output table header
header_line = "| Position | Player |"
for i in range (0,weeks):
	header_line += " Event "+ str(i+1) + " |"
header_line += " Points\n"
for i in range(0,weeks + 3):
	header_line += "| ------- "
print header_line

#HACK - can't use enumerate because our nobody player screws up the count.
rank = 1

#print player lines, alphabetic order. 
for player in sorted(players.keys(), key=  lambda player : player_totals[player], reverse=True):
	#we use a dummy player called "nobody" for imaginery week results. 
	if player == "nobody":
		continue
	table_line = "|"+ str(rank) +"|**"+ player + "**|"
	points = []
	for week in sorted(players[player].keys()):
		table_line += str(players[player][week]) + "|"
		points.append(players[player][week])
	table_line += "**" + str(player_totals[player]) +  "**|"
	rank+=1
	print table_line


