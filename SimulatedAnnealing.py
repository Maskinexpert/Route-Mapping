#Temp for testing
import UniverseBuilder as u
uniStore = u.uniBuilder()
routeList = uniStore[0]
#routeMarkerKeys = uniStore[1]
routeMarkers = uniStore[2]
hiarchy = uniStore[3]
tempLength = routeMarkers['Mn0']
#tempArr = []
tempArrMoon = []

listOfPlanets = []
for i in range(0,tempLength):
  listOfPlanets.append(i)
### 2d array of moons each with same parent ###
currentParentNumber = 0
for moons in (moons for moons in hiarchy if hiarchy[moons].parent.startswith("Pl")):
  if (tempArrMoon != []):
    if (hiarchy[moons].parent == previousParent):
      tempArrMoon[currentParentNumber].append(routeMarkers[moons])
    else:
      currentParentNumber += 1
      tempArrMoon.append([routeMarkers[moons]])
  else:
    tempArrMoon.append([routeMarkers[moons]])

  previousParent = hiarchy[moons].parent 
####




from random import sample
from random import randint

def weightCal(tour,uRouteList):
  totalLength = 0
  for length in range(0,len(tour)-1):
    totalLength += uRouteList[length][length+1]
  return totalLength

def tempCoinflip(current,new,temp,uRouteList):
  heads = ((-weightCal(new,uRouteList)-weightCal(current,uRouteList))/temp)**2
  tails = randint(0,1)
  if heads > tails:
    return True
  else:
    return False
def simAnnealCal(tour,uRouteList,startingLocation,iterations):
  indexStore = []
  mixedRandomTour = sample(tour,len(tour))
  mixedRandomTour.insert(0,mixedRandomTour.pop(mixedRandomTour.index(startingLocation)))
  for i in range(1,len(mixedRandomTour)-1):
    for k in range(i+1,len(mixedRandomTour)):
       indexStore.append([mixedRandomTour[i],mixedRandomTour[k]])
  Tbest = mixedRandomTour[:]
  minWeight = weightCal(Tbest,uRouteList)
  Temperature = minWeight
  cTour = Tbest[:]
  for l in range(0,iterations):
    items = indexStore[randint(0,len(indexStore)-1)]
    randomTour = cTour[:]
    try:
      randomTourIndexStore = mixedRandomTour.index(items[0])
      randomTour[randomTour.index(items[1])]= items[0]
      randomTour[randomTourIndexStore] = items[1]
    except:
      print("Too many iterations")
      break
    if weightCal(randomTour,uRouteList) < weightCal(cTour,uRouteList):
      cTour = randomTour
      if weightCal(cTour,uRouteList) < minWeight:
        minWeight = weightCal(cTour,uRouteList)
        Tbest = cTour[:]
    elif tempCoinflip(cTour,randomTour,Temperature,uRouteList):
      cTour = randomTour
#Can be tweaked to be more aggressive/more relaxed for a better result
    Temperature = Temperature*0.95
  return Tbest
  
### Takes list of planet indexes, list of moon indexes, full routeList, iterations for planets, and iterations for moons ###
def simAnneal(planetList,moonList,uRouteList,plIterations,mnIterations):
  planetBest = simAnnealCal(planetList,uRouteList,0,plIterations)
  finalTourAll = planetBest
  moonTours = []
  for items in range(0,len(planetBest)):
    moonList[items].append(items)
    moons = simAnnealCal(moonList[items],uRouteList,items,mnIterations)
    moons.pop(0)
    finalTourAll[finalTourAll.index(items)+1:1] = moons
  finalTourWeight = weightCal(finalTourAll,uRouteList)
  return finalTourAll,finalTourWeight
  
print(simAnneal(listOfPlanets,tempArrMoon,routeList,7,4))