#imports
#core
from random import random, randint, shuffle, choice, randrange;
from math import floor;

#temporary
#import time;

registry = {
	"player": "@",			#the player
	
	"unknown": "?",			#an unknown tile
	
	"wall": "#",			#walls we can't go through
	"space": " ",			#spaces we can go through
	
	"entrance": ":",		#the entrance to the maze
	"exit": "0",			#the exit of the exit
	
	"treasure-small": "*",	#small amounts of treasure
	"treasure-large": "="	#large amounts of treasure
};

difficulties = {
	"easy": 0.75,
	"normal": 1,
	"hard": 1.25,
	"insane": 2
};

def space(width = 16, height = 8, ch = registry["wall"]):
	area = [];
	for y in range(height):
		area.append([]);
		for x in range(width):
			area[y].append(ch);
	x
	return area;

def chooseremove(items):
    # pick an item index
    if items:
        index = randrange( len(items) )
        return items.pop(index)
    # nothing left!
    return None


class coord:
	def __init__(self, x = 1, y = 1):
		self.x = x;
		self.y = y;

#def to check a space for neighbours
def checkneighbors(area, cur):
	neighbours = {"left": True, "right": True, "up": True, "down": True};
	if(cur.x > 2):
		#we are not near the left edge
		if(area[cur.y][cur.x - 2] == registry["wall"]):
			#we can move left
			neighbours["left"] = False;
	
	if(cur.x < len(area[0]) - 3):
		if(area[cur.y][cur.x + 2] == registry["wall"]):
			#we can move right
			neighbours["right"] = False;
	
	if(cur.y > 2):
		if(area[cur.y - 2][cur.x] == registry["wall"]):
			#we can move up
			neighbours["up"] = False;
	
	if(cur.y < len(area) - 3):
		if(area[cur.y + 2][cur.x] == registry["wall"]):
			#we can move down
			neighbours["down"] = False;
	return neighbours;

#def to determine which sides can be moved to based on neighbour data from the def above
def getpossibleneighbours(neighbours):
	possiblesides = [];
	if(not neighbours["left"]):
		possiblesides.append("left");
	if(not neighbours["right"]):
		possiblesides.append("right");
	if(not neighbours["up"]):
		possiblesides.append("up");
	if(not neighbours["down"]):
		possiblesides.append("down");
	
	return possiblesides;

def maze(width = 17, height = 9):
	#this maze generator works on odd numbers
	if(width % 2 == 0):
		width += 1;
	if(height % 2 == 0):
		height += 1;
	
	
	area = space(width, height); #create an area to build the maze
	area[1][1] = " "; #fill in the initial space
	nodes = [coord(1, 1)]; #node to continue from
	
	while True:
		#break out of the loop if there are no more nodes to choose from
		if(len(nodes) == 0):	
			break;
		
		shuffle(nodes); #shuffle the bag of nodes
		cur = chooseremove(nodes); #grab a random node from the bag
		
		neighbours = checkneighbors(area, cur); #check which neighbouring spots are free
		
		possiblesides = getpossibleneighbours(neighbours); #determine the possible sides that we could move to
		
		#there are no posible sides that we can go to here, let's move on
		if(len(possiblesides) == 0):
			continue;
		
		newside = choice(possiblesides); #choose a random side from the list of possible sides
		#todo implement loops here
		
		#add a new section to the maze based on which sides
		if(newside == "left"):
			area[cur.y][cur.x - 1] = " ";
			area[cur.y][cur.x - 2] = " ";
			nodes.append(coord(cur.x - 2, cur.y));
		elif(newside == "right"):
			area[cur.y][cur.x + 1] = " ";
			area[cur.y][cur.x + 2] = " ";
			nodes.append(coord(cur.x + 2, cur.y));
		elif(newside == "up"):
			area[cur.y - 1][cur.x] = " ";
			area[cur.y - 2][cur.x] = " ";
			nodes.append(coord(cur.x, cur.y - 2));
		elif(newside == "down"):
			area[cur.y + 1][cur.x] = " ";
			area[cur.y + 2][cur.x] = " ";
			nodes.append(coord(cur.x, cur.y + 2));
		
		neighbours[newside] = True;
		
		possiblesides = getpossibleneighbours(neighbours); #update the list of possible sides
		
		if(len(possiblesides) > 0):
			nodes.append(cur);
			shuffle(nodes); #shuffle the nodes
		
	
	return area;

#def to print a space to stdout
def printspace(area):
	for row in area:
		print("".join(row));

def difftomult(diff = "normal"):
	if(diff == "easy"):
		return 0.75;
	elif(diff == "normal"):
		return 1;
	elif(diff == "hard"):
		return 1.25;
	elif(diff == "insane"):
		return 2;

def placestuff(maze, difficulty = "normal"):
	print("Placing treasure....");
	diffmult = difftomult(difficulty); #convert the difficulty to a multiplier
	treasurecount = 0;
	#loop over every space
	y = 0;
	for row in maze:
		x = 0;
		for ch in row:
			if(ch == registry["space"]):
				#we have a space
				
				#place treasure
				chance = int(floor((1 / diffmult) * random() * 10));
				#print("stuffchance:", chance);
				if(chance == 0):
					treasurecount += 1;
					#1 in 4 chance to place large treasure
					if(randint(0, 4) == 0):
						maze[y][x] = registry["treasure-large"];
					else:
						maze[y][x] = registry["treasure-small"];
			
			x += 1;
		
		y += 1;
	
	print("Placed " + str(treasurecount) + " treasures");

#def to place the entrance and exit in a maze
def placedoors(maze, firstfloor = False, lastexit = [1, 1]):
	placements = {};
	if(firstfloor):
		#we are on the first floor, the entrance should be a gap on the edge of the maze
		#the space at (1, 1) is guaranteed to be a space because of the generation algorithm, so we can place the entrance there
		maze[0][1] = registry["space"];
		#record this in the object placements dictionary
		placements["firstfloor"] = True;
		placements["entrance"] = [1, 0];
	else:
		#we are not on the first floor, place the entrance in the same location as the exit on the previous floor
		#todo check to see if there is a wall in the location that we have been told to place the entrance, and if so we should place it in the nearest free spot
		#make sure that the entrance is on the screen
		if(lastexit[0] > len(maze[0]) - 1):
			lastexit[0] = len(maze[0]) - 1;
		if(lastexit[1] > len(maze) - 1):
			lastexit[1] = len(maze) - 1;
		
		maze[lastexit[1]][lastexit[0]] = registry["entrance"];
		
		#make sure that the player can actually move when they start playing
		
		if(lastexit[0] == len(maze[1]) - 1 and lastexit[1] == len(maze) - 1):
			#we are in the bottom corner, add a space so the player can get out
			maze[lastexit[1]][lastexit[0] - 1] = registry["space"];
		
		#record the entrance location in the placements dictionary
		placements["firstfloor"] = False;
		placements["entrance"] = lastexit;
	
	while True:
		exitloc = [randint(0, len(maze[0]) - 1), randint(0, len(maze) - 1)];
		#make sure that there is a space at the generated position
		#print("w", len(maze[0]), "h", len(maze));
		#print(exitloc);
		if(maze[exitloc[1]][exitloc[0]] != registry["space"]):
			continue;
		else:
			maze[exitloc[1]][exitloc[0]] = registry["exit"]; #place the exit
			placements["exit"] = exitloc; #record the exit's location
			break;
	
	return placements; #return the coordinates of the locations at which we placed the doors

#def to convert a difficulty into a viewsize - currently unused
def difftoviewsize(diff):
	if(diff == "easy"):
		return [9, 9];
	elif(diff == "normal"):
		return [7, 7];
	elif(diff == "hard"):
		return [5, 5];
	elif(diff == "insane"):
		return [3, 3];
	else:
		raise ValueError("Invalid difficulty " + diff);

#def to extract the view that a player will see from a maze, translating a difficulty into a view size
def playerview(maze, playerloc = (1, 0), diff = "normal"):
	if(diff == "easy"):
		return extractview(maze, playerloc, 9, 9);
	elif(diff == "normal"):
		return extractview(maze, playerloc, 7, 7);
	elif(diff == "hard"):
		return extractview(maze, playerloc, 5, 5);
	elif(diff == "insane"):
		return extractview(maze, playerloc, 3, 3);
	else:
		raise ValueError("Invalid difficulty " + diff);
#raw view extraction from mazes
def extractview(maze, playerloc = (1, 0), width = 3, height = 3):
	view = space(width, height, registry["unknown"]);
	xbounds = [playerloc[0] - ((width - 1) / 2), playerloc[0] + ((width - 1) / 2)];
	ybounds = [playerloc[1] - ((height - 1) / 2), playerloc[1] + ((height - 1) / 2)];
	#make sure that the bounds are within the maze
	if(xbounds[0] < 0):
		xbounds[0] = 0;
	if(ybounds[0] < 0):
		ybounds[0] = 0;
	if(xbounds[1] > len(maze[0]) - 1):
		xbounds[1] = len(maze[0]) - 1;
	if(ybounds[1] > len(maze) - 1):
		ybounds[1] = len(maze) - 1;
	
	#print("xbounds", xbounds);
	#print("ybounds", ybounds);
	playerviewloc = (playerloc[0] - xbounds[0], playerloc[1] - ybounds[0]);
	#print("Player in view at", playerviewloc);
	
	#copy out a section of the maze to serve as the view
	y = 0;
	for row in maze:
		x = 0;
		for ch in row:
			if(x >= xbounds[0] and x <= xbounds[1] and y >= ybounds[0] and y <= ybounds[1]):
				#we are inside the view bounds
				#print("adding char " + ch + " at abs (" + str(x) + ", " + str(y) + ")");
				view[int(y - ybounds[0])][int(x - xbounds[0])] = ch;
				
			
			x += 1;
		
		y += 1;
	
	#place the player in the view
	view[int(playerviewloc[1])][int(playerviewloc[0])] = registry["player"];
	
	return view;

#def to test the maze generator
def test():
	printspace(maze(40, 30));

if __name__ == "__main__":
	test();