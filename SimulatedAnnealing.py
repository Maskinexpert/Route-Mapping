# This algorithm takes an list of planets, 2d list of moons sorted into rows with the same parent, full route list.
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs, m = all possible routes for moons,  p = amount of planet nodes,
                                   # q = all possible routes for the set of planets, c = constant amount of iterations as given by function call
from random import sample
from random import randint
# Function used to calculate the length of the current route, takes the route and the entire route list as inputs.
def weightCal(tour,uRouteList):
  totalLength = 0
  for length in range(0,len(tour)-1): # O(p)
    totalLength += uRouteList[length][length+1]
  # O(p)
  return totalLength

def tempCoinflip(current,new,temp,uRouteList):
  heads = ((-weightCal(new,uRouteList)-weightCal(current,uRouteList))/temp)**2 # O(p)
  tails = randint(0,1)
  if heads > tails:
    # O(p)
    return True
  else:
    # O(p)
    return False
def simAnnealCal(tour,uRouteList,startingLocation,iterations):
  indexStore = []
  # A random tour is generated from the tour input, and the starting location is moved to the first place in the tour.
  mixedRandomTour = sample(tour,len(tour)) # O(p) (sample has a complexity of k where k is the sampled items, here every item is sampled)
  mixedRandomTour.insert(0,mixedRandomTour.pop(mixedRandomTour.index(startingLocation))) # O(p)
  Tbest = mixedRandomTour[:] # O(p)
  # Each possible pair of nodes are geneated so they can be easily selected to be switched in the next section.
  for i in range(1,len(mixedRandomTour)-1): # O(p^2)
    for k in range(i+1,len(mixedRandomTour)):
       indexStore.append([mixedRandomTour[i],mixedRandomTour[k]])
  minWeight = weightCal(Tbest,uRouteList)
  Temperature = minWeight
  cTour = Tbest[:] # O(p)
  for l in range(0,iterations): # O(c*p) 
    items = indexStore[randint(0,len(indexStore)-1)] # O(log q)
    randomTour = cTour[:] # O(p)
    try:
      randomTourIndexStore = mixedRandomTour.index(items[0]) # O(p)
      randomTour[randomTour.index(items[1])]= items[0] # O(p)
      randomTour[randomTourIndexStore] = items[1]
    except:
      break
    if weightCal(randomTour,uRouteList) < weightCal(cTour,uRouteList): # O(p)
      cTour = randomTour
      if weightCal(cTour,uRouteList) < minWeight: # O(p)
        minWeight = weightCal(cTour,uRouteList) # O(p)
        Tbest = cTour[:]
    elif tempCoinflip(cTour,randomTour,Temperature,uRouteList): # O(p)
      cTour = randomTour
#Can be tweaked to be more aggressive/more relaxed for a better result
    Temperature = Temperature*0.95
  # O(p) + O(p) + O(p) + O(p) + O(c*p) + O(p^2) = O(p^2)
  return Tbest
  

def simAnneal(planetList,moonList,uRouteList,plIterations,mnIterations):
  planetBest = simAnnealCal(planetList,uRouteList,0,plIterations) # O(p^2)
  finalTourAll = planetBest
  moonTours = []
  for items in range(0,len(planetBest)): # O(p*n + p^2*n) (since p^2 will always be larger than n^2)
    moonList[items].append(items) 
    moons = simAnnealCal(moonList[items],uRouteList,items,mnIterations) # O(n^2)
    moons.pop(0)
    finalTourAll[finalTourAll.index(items)+1:1] = moons # O((p*n)+n) (worst case when the last array of moons is added to the end of the list)
  finalTourWeight = 0
  for xSA in range(0,len(finalTourAll)-1): # O(p*n)
    finalTourWeight += uRouteList[finalTourAll[xSA]][finalTourAll[xSA+1]]
  # O(p^2) + O(p*n + p^2*n) + O(p*n) = O(p*n + p^2*n)
  return finalTourAll,finalTourWeight
