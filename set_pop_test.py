import random

print("popping:")
set1 = set(range(7))
set2 = set(range(7,14))
games = [set1, set2]
pops = {"g1":[], "g2":[]}
for i in range(1000):
	g1, g2 = random.sample(games,2)
	p1 = set1.pop()
	p2 = set2.pop()
	set1.add(p2)
	set2.add(p1)
print(set1)
print(set2)

print("\nshuffling")

set1 = set(range(7))
set2 = set(range(7,14))
games = [set1, set2]
pops = {"g1":[], "g2":[]}
for i in range(1000):
	g1, g2 = random.sample(games,2)
	p1 = random.sample(sorted(set1), 1)[0]
	p2 = random.sample(sorted(set2), 1)[0]
	set1.remove(p1)
	set2.remove(p2)
	set1.add(p2)
	set2.add(p1)
print(set1)
print(set2)