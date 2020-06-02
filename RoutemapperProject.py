import copy, NearNeighbor, ClarkeWright, Christofides, TwoOpts, KOpts, SimulatedAnnealing, BranchnBound
import UniverseBuilder as u

uniStore = u.uniBuilder()
routeList = uniStore[0]
routeMarkerKeys = uniStore[1]
routeMarkers = uniStore[2]
hiarchy = uniStore[3]
tempLength = routeMarkers['Mn0']
tempArr = []
tempArrMoon = []


listOfPlanets = []
for i in range(0,tempLength):
  listOfPlanets.append(i)
for items in range(0,tempLength):
  tempArr.append(list(routeList[items]))
for slot1 in range(0,len(tempArr)):
  for slot in range(tempLength,len(routeList)):
    tempArr[slot1].pop(tempLength)
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
a = NearNeighbor.nearNeighbour(routeList,routeMarkers)
b = TwoOpts.twoOpt(listOfPlanets,tempArrMoon,routeList)
c = KOpts.kOpt(listOfPlanets,tempArrMoon,routeList)
d = BranchnBound.branchnBound(tempArr,tempArrMoon, routeList)
e = Christofides.christofides(tempArr,tempArrMoon,routeList)
f = ClarkeWright.clarkeWright(tempArr,tempArrMoon,routeList)
g = SimulatedAnnealing.simAnneal(listOfPlanets,tempArrMoon,routeList,7,4)
print("Near Neighbor: " + str(a))
print("TwoOpts: ".ljust(15,' ') + str(b))
print("KOpts: ".ljust(15,' ') + str(c))
print("BnB: ".ljust(15,' ') + str(d))
print("Christofides: ".ljust(15,' ') + str(e))
print("ClarkeWright: ".ljust(15,' ') + str(f))
print("SimAnneal: ".ljust(15,' ') + str(g))

#for v in routeList:
#  for el in v:
#    print(str(el).rjust(6,' ')+' ', end = '')
#  print(' ')
#for kl in range(0,2):
#  for lkj in range(0,len(routeList)):
#    print('_', end = '')
#print(" ")
#print(routeMarkers)