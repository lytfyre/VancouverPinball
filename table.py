MULLIGAN_WEEKS = 2

import glob

files = glob.glob("*.txt")

players = {}
weeks = 0

for week_number, filename in enumerate(files):
	weeks+=1
	with open(filename) as f:
		for line in f:
			player,points = line.strip().split(',',1)
			if player not in players:
				players[player] = {}
			players[player][week_number] = int(points)

player_totals = {}
player_totals_mulligans = {}
player_scratch_weeks = {}
for player in players.keys():
	#fill with 0s for weeks that other players have results for.
	for week in range(0,weeks):
		if week not in players[player]:
			players[player][week] = 0
	points = []
	for week in sorted(players[player].keys()):
		points.append(players[player][week])
	points.sort()
	player_totals[player] = sum(points)
	player_totals_mulligans[player] = sum(points[MULLIGAN_WEEKS:])


header_line = "| Position | Raw Points | Qualifying Points | Player |"
for i in range(0,weeks):
	header_line+=" Week " + str(i+1)+ " |"
header_line+= "\n"
for i in range(0,weeks+4):
	header_line+="| -------"
print header_line

#print player lines
rank = 1
for player in sorted(players.keys(), key=  lambda player : player_totals_mulligans[player], reverse=True):
	if player == "nobody":
		continue
	table_line = "| "+ str(rank) + " | " + str(player_totals[player]) + " | " + str(player_totals_mulligans[player]) + " | **" + player + "** | "
	for week in sorted(players[player].keys()):
		table_line+= str(players[player][week])+ " | "
	rank+=1
	print table_line