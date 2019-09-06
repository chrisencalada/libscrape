import json

with open('list_of_dicts.json') as json_file:
	data = json.load(json_file)

hold = []
for x in data:
	for y in x:
		hold.append(y)


for x in hold:
	print(x['ID'])
