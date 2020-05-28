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

### Array of only planet to planet routes ###
#tempArr = routeList[:]
#for items in range(tempLength,len(tempArr)):
#  tempArr.pop(tempLength)
#for slot1 in range(0,len(tempArr)):
#  for slot in range(tempLength,len(tempArr[0])):
#    tempArr[slot1].pop(tempLength)
###
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


def weightCal(tour,uRouteList):
  totalLength = 0
  for length in range(0,len(tour)):
    totalLength += uRouteList[length][length+1]
  return totalLength

def twoOptCal(tour,uRouteList,startingLocation):
  indexStore = []
  mixedRandomTour = sample(tour,len(tour))
  mixedRandomTour.insert(0,mixedRandomTour.pop(mixedRandomTour.index(startingLocation)))
  Tmark = mixedRandomTour[:]
  for i in range(1,len(mixedRandomTour)-1):
    for k in range(i+1,len(mixedRandomTour)):
       indexStore.append([mixedRandomTour[i],mixedRandomTour[k]])
  Tbest = Tmark
  for items in indexStore:
    randomTour = Tmark[:]
    randomTourIndexStore = mixedRandomTour.index(items[0])
    randomTour[randomTour.index(items[1])]= items[0]
    randomTour[randomTourIndexStore] = items[1]
    if weightCal(randomTour,uRouteList) < weightCal(Tbest,uRouteList):
      Tbest = randomTour
  Tmark = Tbest
  return Tmark
### Takes list of planet indexes, list of moon indexes, and full routeList ###
def twoOpt(planetList,moonList,uRouteList):
  planetBest = kOptCal(planetList,uRouteList,0)
  finalTourAll = planetBest
  moonTours = []
  for items in range(0,len(planetBest)):
    moonList[items].append(items)
    moons = kOptCal(moonList[items],uRouteList,items)
    moons.pop(0)
    finalTourAll[finalTourAll.index(items)+1:1] = moons
  finalTourWeight = weightCal(finalTourAll,uRouteList)
  return finalTourAll,finalTourWeight
print(kOpt(listOfPlanets,tempArrMoon,routeList))