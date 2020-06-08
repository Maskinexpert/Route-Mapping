import copy, NearNeighbour, ClarkeWright, Christofides, TwoOpts, KOpts, SimulatedAnnealing, BranchnBound
import UniverseBuilder as u
import timeit
import importlib
uniStore = u.uniBuilder(2)
routeList = uniStore[0]
#routeMarkerKeys = uniStore[3]
routeMarkers = uniStore[1]
hiarchy = uniStore[2]
tempLength = routeMarkers['Mn0']
planetArray = []
moonArray = []


listOfPlanets = []
for i in range(0,tempLength):
  listOfPlanets.append(i)
for items in range(0,tempLength):
  planetArray.append(list(routeList[items]))
for slot1 in range(0,len(planetArray)):
  for slot in range(tempLength,len(routeList)):
    planetArray[slot1].pop(tempLength)
currentParentNumber = 0
for moons in (moons for moons in hiarchy if hiarchy[moons].parent.startswith("Pl")):
  if (moonArray != []):
    if (hiarchy[moons].parent == previousParent):
      moonArray[currentParentNumber].append(routeMarkers[moons])
    else:
      currentParentNumber += 1
      moonArray.append([routeMarkers[moons]])
  else:
    moonArray.append([routeMarkers[moons]])

  previousParent = hiarchy[moons].parent
timeList =[]
testNumber = 10
nnTimes = []
for a in range(0,testNumber):
  nnTime = timeit.timeit()
  a = NearNeighbour.nearNeighbour(routeList)
  a = a + (nnTime,)
  nnTimes.append(a)
avgLengthNn = 0
avgTimeNn = 0
for lines in range(0,len(nnTimes)):
  avgLengthNn += nnTimes[lines][1]
  avgTimeNn += nnTimes[lines][2]
timeList.append(avgTimeNn/testNumber)
toTimes = []
for b in range(0,testNumber):
  toTime = timeit.timeit()
  b = TwoOpts.twoOpt(listOfPlanets,moonArray,routeList)
  b = b + (toTime,)
  toTimes.append(b)
avgLengthTo = 0
avgTimeTo = 0
for lines in range(0,len(toTimes)):
  avgLengthTo += toTimes[lines][1]
  avgTimeTo += toTimes[lines][2]
timeList.append(avgTimeTo/testNumber)
koTimes = []
for c in range(0,testNumber):
  koTime = timeit.timeit()
  c = KOpts.kOpt(listOfPlanets,moonArray,routeList)
  c = c + (koTime,)
  koTimes.append(c)
avgLengthKo = 0
avgTimeKo = 0
for lines in range(0,len(koTimes)):
  avgLengthKo += koTimes[lines][1]
  avgTimeKo += koTimes[lines][2]
timeList.append(avgTimeKo/testNumber)
bnbTimes = []
for d in range(0,testNumber):
  bnbTime = timeit.timeit()
  d = BranchnBound.branchnBound(planetArray,moonArray, routeList)
  d = d + (bnbTime,)
  bnbTimes.append(d)
  BranchnBound = importlib.reload(BranchnBound)
avgLengthBnb = 0
avgTimeBnb = 0
for lines in range(0,len(bnbTimes)):
  avgLengthBnb += bnbTimes[lines][1]
  avgTimeBnb += bnbTimes[lines][2]
timeList.append(avgTimeBnb/testNumber)
cfTimes = []
for e in range(0,testNumber):
  cfTime = timeit.timeit()
  e = Christofides.christofides(planetArray,moonArray,routeList)
  e = e + (cfTime,)
  cfTimes.append(e)
avgLengthCf = 0
avgTimeCf = 0
for lines in range(0,len(cfTimes)):
  if len(cfTimes[lines][0]) < len(routeList):
    avgTimeCf = 1
    break
  avgLengthCf += cfTimes[lines][1]
  avgTimeCf += cfTimes[lines][2]
timeList.append(avgTimeCf/testNumber)
cwTimes = []
for f in range(0,testNumber):
  cwTime = timeit.timeit()
  f = ClarkeWright.clarkeWright(planetArray,moonArray,routeList)
  f = f + (cwTime,)
  cwTimes.append(f)
  ClarkeWright = importlib.reload(ClarkeWright)
avgLengthCw = 0
avgTimeCw = 0
for lines in range(0,len(cwTimes)):
  if len(cwTimes[lines][0]) < len(routeList):
    avgTimeCw = 1
    break
  avgLengthCw += cwTimes[lines][1]
  avgTimeCw += cwTimes[lines][2]
timeList.append(avgTimeCw/testNumber)
saTimes = []
for g in range(0,testNumber):
  saTime = timeit.timeit()
  g = SimulatedAnnealing.simAnneal(listOfPlanets,moonArray,routeList,7,4)
  g = g + (saTime,)
  saTimes.append(g)
avgLengthSa = 0
avgTimeSa = 0
for lines in range(0,len(saTimes)):
  avgLengthSa += saTimes[lines][1]
  avgTimeSa += saTimes[lines][2]
timeList.append(avgTimeSa/testNumber)
smallest = 1
for tL in range(1,len(timeList)):
  if timeList[tL] < smallest:
    smallest = timeList[tL]

print("Near Neighbour: " + str(avgLengthNn/testNumber).ljust(10,' '),str((avgTimeNn/testNumber)*1000).ljust(20,' '), str((avgTimeNn/testNumber)/smallest))
print("TwoOpts: ".ljust(16,' ') + str(avgLengthTo/testNumber).ljust(10,' '),str((avgTimeTo/testNumber)*1000).ljust(20,' '), str((avgTimeTo/testNumber)/smallest))
print("KOpts: ".ljust(16,' ') + str(avgLengthKo/testNumber).ljust(10,' '),str((avgTimeKo/testNumber)*1000).ljust(20,' '), str((avgTimeKo/testNumber)/smallest))
print("BranchnBound: ".ljust(16,' ') + str(avgLengthBnb/testNumber).ljust(10,' '),str((avgTimeBnb/testNumber)*1000).ljust(20,' '), str((avgTimeBnb/testNumber)/smallest))
print("Christofides: ".ljust(16,' ')+ str(avgLengthCf/testNumber).ljust(10,' '),str((avgTimeCf/testNumber)*1000).ljust(20,' '), str((avgTimeCf/testNumber)/smallest))
print("ClarkeWright: ".ljust(16,' ') + str(avgLengthCw/testNumber).ljust(10,' '),str((avgTimeCw/testNumber)*1000).ljust(20,' '), str((avgTimeCw/testNumber)/smallest))
print("SimAnneal: ".ljust(16,' ') + str(avgLengthSa/testNumber).ljust(10,' '), str((avgTimeSa/testNumber)*1000).ljust(20,' '), str((avgTimeSa/testNumber)/smallest))
