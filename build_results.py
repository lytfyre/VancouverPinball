"""
Outputs a markdown formated results table from a folder of results.
Expects a folder of .txt files of results
file names lexographicly ordered as they should appear in the table
a header precedes results, in the form of a JSON block, between "---" lines.
each results line should be of the form "POSITION#,PLAYER_NAME"
a line in the file shall have no lines preceding it with a better finish. (but may have preceding tied entry)
"""
FIRST_PLACE_SCORE = 20.0
SECOND_PLACE_SCORE = 18.0
STANDARD_SCORES_START = 16.0
MULLIGANS = 0


import glob, json, datetime

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
event_info = {}

events = 0

for event_number,filename in enumerate(files):
	events += 1
	evently_results = []

	event_info_string = ""
	
	score_band_sizes = {}
	with open(filename) as f:
		last_finish = 0
		score_band = 0

		
		in_info = False
		
		for line in f:
			# events have a header block of JSON, delminated by "---"
			if line == "---\n":
				if (in_info):
					event_info_string += "}\n"
				else: 
					event_info_string +="{\n"
				in_info = not in_info
			elif (in_info):
				event_info_string += line
			else:
				finish,player = line.strip().split(',', 1)
				if last_finish != finish:
					score_band +=1
					score_band_sizes[score_band] = 0
				score_band_sizes[score_band] +=1 

				last_finish = finish
				evently_results.append( (player,score_band) )

	event_info[event_number] = json.loads(event_info_string)

	band_scores = {}
	for player,band in evently_results:
		if not band in band_scores:
			band_scores[band] = score(band_scores.get(band-1,0), score_band_sizes[band], band)
		if player not in players:
			players[player] = {}
		players[player][event_number] = band_scores[band]

# generate player totals
player_totals = {}
for player in players.keys():
	# fill with 0s for events that other players have results for.
	for event in range(0,events):
		if event not in players[player]:
			players[player][event] = 0
	points = []
	for event in sorted(players[player].keys()):
		points.append(players[player][event])
	points.sort()
	player_totals[player] = sum(points)


# Output table header
header_line = "| Position | Points | Player |"
for i in range(0,events):
	header_line +=" |"
header_line += "\n | | | |"
for i in range (0,events):
	header_line += event_info[i]["name"]+ " | "
header_line += "\n | | | |"
for i in range(0,events):
	d= datetime.datetime.strptime(event_info[i]["date"],'%Y-%m-%d').date()
	header_line += d.strftime('%b %d') + " | "
header_line += "\n"
for i in range(0,events + 3):
	header_line += "| :-------: "
print header_line

#HACK - can't use enumerate because our nobody player can screw up the count.
rank = 1

#print player lines, alphabetic order. 
for player in sorted(players.keys(), key=  lambda player : player_totals[player], reverse=True):
	if player == "nobody": #dummy player
		continue

	table_line = "| **"+ str(rank) +"**|"+ str(player_totals[player]) +"|**"+ player + "**|"
	points = []

	for event in sorted(players[player].keys()):
		table_line += str(players[player][event]) + "|"
		points.append(players[player][event])


	rank+=1
	print table_line


