from opgave import opgave as o
from opgaveholdnummer import opgaveholdnummer as ohn
from random import randint as random
hashmap = {}
hashmapHovedeopgaverKlaring = {}
hashmapHovedeopgaverKlaring["meget godt"] = 1.0
hashmapHovedeopgaverKlaring["godt"] = 0.85
hashmapHovedeopgaverKlaring["ok"] = 0.5
hashmapHovedeopgaverKlaring["meh"] = 0.25

hashmapEkstraopgaverKlaring = {}
hashmapEkstraopgaverKlaring["rigtig mange"] = 1.0
hashmapEkstraopgaverKlaring["mange"] = 0.8
hashmapEkstraopgaverKlaring["en god maengde"] = 0.6
hashmapEkstraopgaverKlaring["en sjat"] = 0.4
hashmapEkstraopgaverKlaring["lidt"] = 0.2

max_objectives = 30
filename = "./opgaver"
skema = "./rus.csv"

try:
    with open(filename, 'r') as file:
        for line in file:
            line_split = line.split(',')
            hashmap[line_split[0]] = o(int(line_split[0]), int(line_split[1]), int(line_split[2]))
except FileNotFoundError:
    print(f"File '{filename}' not found.")
except IOError:
    print(f"Error reading file '{filename}'.")


def get_opgave(opgavenum):
    return hashmap[opgavenum]

teams = {}
team_and_timestamp = {}

try:
    with open(skema, 'r') as file:
        for index, line in enumerate(file):

            if index == 0:
                continue

            line_split = line.split(',')
            timestamp = line_split[0]
            team = line_split[1]
            opg_num = line_split[2]
            theme = line_split[3]
            evaluation = ""
            evaluation2 = ""

            if (theme == "Kun points (hovedeopgave)"):
                evaluation = line_split[4]
            elif (theme == "Kun ekstra points"):
                evaluation = line_split[5]
            elif (theme == "Points og Ekstra Points"):
                evaluation = line_split[6]
                evaluation2 = line_split[7]

            if (evaluation == ""):
                print("Error: No evaluation found.")
                print("Line: " + line)

            # Remove new line from evaluation's end
            if evaluation[-1] == '\n':
                evaluation = evaluation[:-1]
            evaluation = evaluation.lower()

            if evaluation2 != "":
                if evaluation2[-1] == '\n':
                    evaluation2 = evaluation2[:-1]
                evaluation2 = evaluation2.lower()           
            
            if team not in teams:
                teams[team] = {}
                only_time = timestamp.split(' ')[1]
                time_split = only_time.split(':')
                seconds = int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])
                team_and_timestamp[team] = seconds

            if teams[team].get(opg_num) is not None:
            
                if theme == "Kun points (hovedeopgave)":
                    if teams[team][opg_num] is not None:
                        print("Error: Opgave already exists.")
                        print("Line: " + line)
                        continue
                
                if theme == "Kun ekstra points":
                    if teams[team][opg_num].get_ekstraopgave() != -1:
                        print("Error: Opgave already exists.")
                        print("Line: " + line)
                        continue

                if theme == "Points og Ekstra Points":
                    if teams[team][opg_num] is not None and teams[team][opg_num].get_ekstraopgave() != -1:
                        print("Error: Opgave already exists.")
                        print("Line: " + line)
                        continue

                
            if theme == "Kun points (hovedeopgave)":
                multiplier = hashmapHovedeopgaverKlaring[evaluation]
                var = multiplier * get_opgave(opg_num).hovedeopgave
                teams[team][opg_num] = ohn(int(opg_num), team, var, -1)
                
                # Convert time stamp 9/7/2024 15:15:04 to number of seconds
                only_time = timestamp.split(' ')[1]
                time_split = only_time.split(':')
                seconds = int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])
                if seconds > team_and_timestamp[team]:
                    team_and_timestamp[team] = seconds
                    

            elif theme == "Kun ekstra points":
                multiplier = hashmapEkstraopgaverKlaring[evaluation]
                var = multiplier * get_opgave(opg_num).ekstraopgave
                ohnObject = teams[team].get(opg_num)
                if ohnObject is None:
                    teams[team][opg_num] = ohn(int(opg_num), team, -1, var)
                else:	
                    ohnObject.set_ekstraopgave(var)
                
            elif theme == "Points og Ekstra Points":
                var = hashmapHovedeopgaverKlaring[evaluation] * get_opgave(opg_num).hovedeopgave
                var2 = hashmapEkstraopgaverKlaring[evaluation2] * get_opgave(opg_num).ekstraopgave
                teams[team][opg_num] = ohn(int(opg_num), team, var, var2)


except FileNotFoundError:
    print(f"File '{skema}' not found.")
except IOError:
    print(f"Error reading file '{skema}'.")

earliest_finisher_team = None
earliest_timestamp = None
top_5_teams = []
for team, opgaver in teams.items():
    if len(opgaver) == max_objectives:
        if earliest_timestamp is None or team_and_timestamp[team] < earliest_timestamp:
            earliest_timestamp = team_and_timestamp[team]
            earliest_finisher_team = team
            if len(top_5_teams) < 5:
                top_5_teams.append(team)
    else:
        print(f"Team: {teams} has not completed all objectives.")


# Conver to a CSV file
randomStr = random(0, 100000)
with open(f"team_data/teams_{randomStr}.csv", "a") as file:
    file.write(f"Team, Opgave, Points\n")
    for (team, opgaver) in teams.items():
        print(f"Team: {team}")
        for (opgave, points) in opgaver.items():
            print(f"Opgave: {opgave}, Points: {points.calculate_total_points()}")
            file.write(f"{team},{opgave},{points.calculate_total_points()}"+ "\n")
        print("\n")

# Final Results
# Sort teams by total points using .calculate_total_points()
# Write to final_results.csv

sorted_teams = []

for (team, opgaver) in teams.items():
    total = 0
    for (opgave, points) in opgaver.items():
        total += points.calculate_total_points()
    sorted_teams.append((team, total))

sorted_teams.sort(key=lambda x: float(x[1]), reverse=True)

with open(f"final_data/final_results.csv", "w") as file:
    file.write(f"Team, Total Points\n")
    for (team, total) in sorted_teams:
        print(f"Team: {team}, Total Points: {total}")
        file.write(f"{team},{total}\n")
    print("\n")


# with open(f"final_data/final_results.csv", "w") as file:
#     file.write(f"Team, Total Points\n")
#     for (team, opgaver) in teams.items():
#         total = 0
#         for (opgave, points) in opgaver.items():
#             total += points.calculate_total_points()
#         print(f"Team: {team}, Total Points: {total}")
#         file.write(f"{team},{total}\n")
#     print("\n")

print(f"Earliest finisher: {earliest_finisher_team}")
print(f"Top 5 teams: {top_5_teams}")