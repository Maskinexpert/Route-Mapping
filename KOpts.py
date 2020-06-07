# This algorithm takes an list of planets, 2d list of moons sorted into rows with the same parent, full route list.
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs, m = all possible routes for moons, p = amount of planet nodes, q = all possible routes for the set of planets 

from random import sample
# Function used to calculate the length of the current route, takes the route and the entire route list as inputs.
def weightCal(tour,uRouteList):
  totalLength = 0
  for length in range(0,len(tour)-1): # O(p)
    totalLength += uRouteList[length][length+1]
  # O(p)
  return totalLength

# Function used to switch the nodes position and check for any improvements. 
# Takes the locations that need to be visited, the entire universe route list, and the starting location of the route.
def kOptCal(tour,uRouteList,startingLocation):
  indexStore = []
  # A random tour is generated from the tour input, and the starting location is moved to the first place in the tour.
  mixedRandomTour = sample(tour,len(tour)) # O(p) (sample has a complexity of k where k is the sampled items, here every item is sampled)
  mixedRandomTour.insert(0,mixedRandomTour.pop(mixedRandomTour.index(startingLocation))) # O(p)
  Tmark = mixedRandomTour[:] # O(p)
  change = True
  # Each possible pair of nodes are geneated so they can be easily selected to be switched in the next section.
  for i in range(1,len(mixedRandomTour)-1): # O(p^2)
    for k in range(i+1,len(mixedRandomTour)):
       indexStore.append([mixedRandomTour[i],mixedRandomTour[k]])
  # 2 nodes is switched and the length of this new route is calculated and compared to the orignal route/currently best route. 
    # If an improvement has been made, then the currently best route is updated to be the new route, and the algorithm loops.
    # If no improvements was made, then the route is the most optimized route the algorithm can make.
  while change == True: # O(q^2 * p) (the loop itself has a worst case complexity of O(q) since it could end up having every single edge changedd)
    change = False
    Tbest = Tmark
    for items in indexStore: # O(q*p) 
      randomTour = Tmark[:] # O(p)
      randomTourIndexStore = mixedRandomTour.index(items[0]) # O(p)
      randomTour[randomTour.index(items[1])]= items[0] # O(p)
      randomTour[randomTourIndexStore] = items[1] 
      if weightCal(randomTour,uRouteList) < weightCal(Tbest,uRouteList): # O(p)
        Tbest = randomTour
        change = True
    Tmark = Tbest
  # O(q^2*p) + O(p^2) + O(p) + O(p) =  O(q^2*p) (since q will always be larger than p)
  return Tmark

# The kOpts function runs the calculation aspect of the program for each sub-problem and returns a complete route list.
# It takes the list of planets, the 2d list of all moons sorted into rows with the same planet node, and the entire route list.
def kOpt(planetList,moonList,uRouteList):
  # Generates the optimal list of planets
  planetBest = kOptCal(planetList,uRouteList,0) # O(q^2*p)
  finalTourAll = planetBest
  moonTours = []
  # For each planet node, generate the sub-problem moon route, and place these after their respective planet node.
  for items in range(0,len(planetBest)): # O(p*m^2*n)
    moonListCopy = list(moonList[items]) # O(n)
    moonListCopy.append(items)
    moons = kOptCal(moonListCopy,uRouteList,items) # O(m^2 * n)
    moons.pop(0)
    finalTourAll[finalTourAll.index(items)+1:1] = moons # O((p*n)+n) (worst case when the last array of moons is added to the end of the list)
  finalTourWeight = 0
  # The length of the entire route is calculated and returned.
  for xKO in range(0,len(finalTourAll)-1): # O(p*n)
    finalTourWeight += uRouteList[finalTourAll[xKO]][finalTourAll[xKO+1]]
  # O(q^2*p) + O(p*m^2*n) = O(q^2*p) (since q will always be larger than m in this universe)
  return finalTourAll,finalTourWeight