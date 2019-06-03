''' Cmpt 310 assignment 2 question 2
	Created by Liam Ling
	Date: Sun Jun 2 2019'''

def check_teams(graph, csp_sol):
	if graph == {}: # return ture if the no one is no one's friend
		return True

	teams = {}
	for person in csp_sol: # create a team dictionary
		team_num = csp_sol[person]
		if team_num not in teams:
			teams[team_num] = [person]
		else:
			teams[team_num].append(person)
	#print("teams: ", teams)
	#print("graph: ", graph)
	
	for team in teams: # check if for each person in the team, if any rest of the team member is his/her friend
		members = teams[team]
		for person in members:
			#print("person: ", person)
			for friend in graph[person]:
				#print("friends: ", graph[person], "friend: ", friend, "rest: ", members[(members.index(person)+1):])
				if friend in members[(members.index(person)+1):]:
					return False
	return True

#graph = {0: [1, 2], 1: [0], 2: [0], 3: []}
#csp_sol = {0:0, 1:1, 2:1, 3:0}
#print(check_teams(graph, csp_sol))