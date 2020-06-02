#Temp for testing
#import UniverseBuilder as u
#uniStore = u.uniBuilder()
#routeList = uniStore[0]
#routeMarkerKeys = uniStore[1]
#routeMarkers = uniStore[2]
#hiarchy = uniStore[3]
#tempLength = routeMarkers['Mn0']
#tempArr = []
#tempArrMoon = []

#for items in range(0,tempLength):
#  tempArr.append(routeList[items])
#  for slot in range(tempLength,len(routeList[items])):
#    tempArr[items].pop(tempLength)
#currentParentNumber = 0
#for moons in (moons for moons in hiarchy if hiarchy[moons].parent.startswith("Pl")):
#  if (tempArrMoon != []):
#    if (hiarchy[moons].parent == previousParent):
#      tempArrMoon[currentParentNumber].append(routeMarkers[moons])
#    else:
#      currentParentNumber += 1
#      tempArrMoon.append([routeMarkers[moons]])
#  else:
#    tempArrMoon.append([routeMarkers[moons]])
#
#  previousParent = hiarchy[moons].parent 
### Takes only planets array of UniverseBuilder[0], 2d list of moons sorted into groups with the same parent, full UniverseBuilder[0] ###

degreeList = []
degreeListMoon = []
def savings(uRoute,x,y):
  savedDistance = uRoute[0][x] + uRoute[0][y] - uRoute[x][y]
  return savedDistance
def moonSavings(uRouteList,parent,x,y):
  moonSavedDistance = uRouteList[x][parent] + uRouteList[y][parent] - uRouteList[x][y]
  return moonSavedDistance

def degree(x):
  if x in degreeList:
    return 1
  else:
    degreeList.append(x)
    return 0
def degreeMoon(x):
  if x in degreeListMoon:
    return 1
  else:
    degreeListMoon.append(x)
    return 0
##### Remember moonsCalculations looks up distance from moons to parent to find distance #####
def moonsCalculations(uRouteMoons,planetParent,uRouteList):
  savingsArrayMoons = []
  m = []
  tourMoon = []
  maxTourMoon = len(uRouteMoons[planetParent])-1
  for i in range(0,len(uRouteMoons[planetParent])-1):
    for k in range(i+1,len(uRouteMoons[planetParent])):
      savingsArrayMoons.append((moonSavings(uRouteList,planetParent,uRouteMoons[planetParent][i],uRouteMoons[planetParent][k]),uRouteMoons[planetParent][i],uRouteMoons[planetParent][k]))
  sortedSavingsArrayMoon = sorted(savingsArrayMoons,reverse = True)
  tourMoon = []
  for o in range(0,len(sortedSavingsArrayMoon)):
    if ((sortedSavingsArrayMoon[o][1] in degreeListMoon) and (sortedSavingsArrayMoon[o][2] in degreeListMoon) and m != []) or ((sortedSavingsArrayMoon[o][1] in m) or (sortedSavingsArrayMoon[o][2] in m)):
      continue
    tourMoon.append((uRouteList[sortedSavingsArrayMoon[o][1]][sortedSavingsArrayMoon[o][2]],sortedSavingsArrayMoon[o][1],sortedSavingsArrayMoon[o][2]))
    if degreeMoon(sortedSavingsArrayMoon[o][1]) == 1:
      m.append(sortedSavingsArrayMoon[o][1])
    if degreeMoon(sortedSavingsArrayMoon[o][2]) == 1:
      m.append(sortedSavingsArrayMoon[o][2])
    if len(m) == maxTourMoon:
      break
  for q in m:
    degreeListMoon.remove(q)
  remainingRoute = min((uRouteList[degreeListMoon[0]][planetParent],planetParent,degreeListMoon[0]),(uRouteList[degreeListMoon[1]][planetParent],planetParent,degreeListMoon[1]))
  tourMoon.append(remainingRoute)
  tourMoon = sorted(tourMoon, key=lambda x: x[1])
  location = planetParent
  moonCalRoute = []
  moonsWeight = 0
  for ea in range(0,len(tourMoon)):
    for ro in range(0,len(tourMoon)):
      if tourMoon[ro][1] == location:
        moonsWeight += tourMoon[ro][0]
        location = tourMoon[ro][2]
        moonCalRoute.append(location)
        tourMoon.pop(ro)
        break
      if tourMoon[ro][2] == location:
        moonsWeight += tourMoon[ro][0]
        location = tourMoon[ro][1]
        moonCalRoute.append(location)
        tourMoon.pop(ro)
        break
  return moonsWeight, moonCalRoute

def clarkeWright (uRoutePlanets, uRouteMoons, uRouteList):
  savingsArray = []
  l = []
  tour = []
  edgeList = []
  maxTour = len(uRoutePlanets)-1
  node1 = (-1,-1)
  node2 = (-2,-2)
  for i in range(1,len(uRoutePlanets)-1):
    for k in range(i+1,len(uRoutePlanets)):
      savingsArray.append((savings(uRoutePlanets,i,k),i,k))
  sortedSavingsArray = sorted(savingsArray,reverse = True)
  for o in range(0,len(sortedSavingsArray)):
    ###Cathes cases where node1 and node2 are in a chain but not the same chain###
    if ((sortedSavingsArray[o][1] in l) or (sortedSavingsArray[o][2] in l)):
      continue
    elif ((sortedSavingsArray[o][1] in degreeList) or (sortedSavingsArray[o][2] in degreeList)):
      for i in range(0,len(edgeList)):
        for k in edgeList[i]:
          if sortedSavingsArray[o][1] == k:
            node1 = (k,i)
          if sortedSavingsArray[o][2] == k:
            node2 = (k,i)
      if node1[1] == node2[1]:
        node1 = (-1,-1)
        node2 = (-2,-2)
        continue
      elif ((node1[0] > -1) and (node2[0] > -1)):
        edgeList[node1[1]].extend(edgeList[node2[1]])
        del edgeList[node2[1]]
        node1 = (-1,-1)
        node2 = (-2,-2)
      elif (node1[0] > -1):
        edgeList[node1[1]].append(sortedSavingsArray[o][2])
      else:
        edgeList[node2[1]].append(sortedSavingsArray[o][1])
    else:
      edgeList.append([sortedSavingsArray[o][1],sortedSavingsArray[o][2]])
    tour.append((uRoutePlanets[sortedSavingsArray[o][1]][sortedSavingsArray[o][2]],sortedSavingsArray[o][1],sortedSavingsArray[o][2]))
    if degree(sortedSavingsArray[o][1]) == 1:
      l.append(sortedSavingsArray[o][1])
    if degree(sortedSavingsArray[o][2]) == 1:
      l.append(sortedSavingsArray[o][2])
    if len(l) == maxTour:
      break
  for p in l:
    degreeList.remove(p)
  remainingRoute = min((uRoutePlanets[0][degreeList[0]],0,degreeList[0]),(uRoutePlanets[0][degreeList[1]],0,degreeList[1]))
  tour.append(remainingRoute)
  result = []
  ### Add moon tour weight for each node ###
  for planetParent in range(0,len(uRouteMoons)):
    result.extend([moonsCalculations(uRouteMoons,planetParent,uRouteList)])
    del degreeListMoon[:]
  

  
  tour = sorted(tour, key=lambda x: x[1])

  location = 0
  cwRoute = [0]
  cwRoute.extend(result[0][1])
  weight = result[0][0]
  for ea in range(0,len(tour)):
    for ro in range(0,len(tour)):
      if tour[ro][1] == location:
        location = tour[ro][2]
        weight += tour[ro][0] + result[location][0]
        cwRoute.append(location)
        cwRoute.extend(result[location][1])
        tour.pop(ro)
        break
      if tour[ro][2] == location:
        location = tour[ro][1]
        weight += tour[ro][0] + result[location][0]
        cwRoute.append(location)
        cwRoute.extend(result[location][1])
        tour.pop(ro)
        break
  
  
  return cwRoute, weight
#print(clarkeWright(tempArr,tempArrMoon,routeList))