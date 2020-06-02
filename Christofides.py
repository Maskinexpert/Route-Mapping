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
#  tempArr.append(list(routeList[items]))
#for slot1 in range(0,len(tempArr)):
#  for slot in range(tempLength,len(routeList)):
#    tempArr[slot1].pop(tempLength)
#print(tempArr)


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

#  previousParent = hiarchy[moons].parent 
####


import Kruskal as kru

def christofidesPlanets(uRoutePlanets):
  oddNodeCounter = []
  oddNodeArray =[]
  oddNodeRoutes = []
  mstGraph = kru.kruskal(uRoutePlanets)
  for edges in range(0,len(mstGraph[0])+1):
    oddNodeCounter.append(0)
  for edges in range(0,len(mstGraph[0])):
    oddNodeCounter[mstGraph[0][edges][0]] += 1
    oddNodeCounter[mstGraph[0][edges][1]] += 1
  for i in range(0,len(oddNodeCounter)):
    if (oddNodeCounter[i]%2) == 1:
      oddNodeArray.append(i)
  for j in range(0,len(oddNodeArray)-1):
    for k in range(j+1,len(oddNodeArray)):
      oddNodeRoutes.append([uRoutePlanets[oddNodeArray[j]][oddNodeArray[k]],oddNodeArray[j],oddNodeArray[k]])
  oddNodeRoutes = sorted(oddNodeRoutes)
  nodes = [oddNodeRoutes[0][1],oddNodeRoutes[0][2]]
  mstGraph[0].append((oddNodeRoutes[0][1],oddNodeRoutes[0][2]))
  stopped = False
  for m in range(1,len(oddNodeRoutes)):
    for n in range(0,len(nodes)):
      if (nodes[n] in oddNodeRoutes[m]):
        stopped = True
        break
    if stopped == False:
      mstGraph[0].append((oddNodeRoutes[m][1],oddNodeRoutes[m][2]))
      nodes.extend([oddNodeRoutes[m][1],oddNodeRoutes[m][2]])
    else:
      stopped = False
  location = 0
  finalRoute = [0]
  tempCount = 0
  while (len(finalRoute) < len(uRoutePlanets)):
    stopped2 = False
    for p in range(0,len(mstGraph[0])):
      if mstGraph[0][p][0] == location:
        if mstGraph[0][p][1] not in finalRoute:
          finalRoute.insert(finalRoute.index(location)+1,mstGraph[0][p][1])
          location = mstGraph[0][p][1]
          mstGraph[0].pop(p)
          stopped2 = True
          break
        else:
          mstGraph[0].pop(p)
          
          break
      elif mstGraph[0][p][1] == location:
        if mstGraph[0][p][0] not in finalRoute:
          finalRoute.insert(finalRoute.index(location)+1,mstGraph[0][p][0])
          location = mstGraph[0][p][0]
          mstGraph[0].pop(p)
          stopped2 = True
          break
        else:
          mstGraph[0].pop(p)
          break
    if stopped2 == True:
      continue
    else:
      location = finalRoute[finalRoute.index(location)-1]

  return finalRoute


def christofidesMoons(uRouteList,moonParent,moonList):
  moonArray = []
  allList = [moonParent]
  allList.extend(moonList)
  for c in range(0,len(allList)):
    moonArray.append([])
    for d in range(0,len(allList)):
      moonArray[c].append(uRouteList[c][d])
  oddNodeCounterMoon = []
  oddNodeArrayMoon =[]
  oddNodeRoutesMoon = []
  mstGraphMoon = kru.kruskal(moonArray)
  for items in range(0,len(mstGraphMoon[0])):
    mstGraphMoon[0][items] = (allList[mstGraphMoon[0][items][0]],allList[mstGraphMoon[0][items][1]])
  for edges in range(0,len(mstGraphMoon[0])+1):
    oddNodeCounterMoon.append(0)
  for edges in range(0,len(mstGraphMoon[0])):
    oddNodeCounterMoon[allList.index(mstGraphMoon[0][edges][0])] += 1
    oddNodeCounterMoon[allList.index(mstGraphMoon[0][edges][1])] += 1
  for i in range(0,len(oddNodeCounterMoon)):
    if (oddNodeCounterMoon[i]%2) == 1:
      oddNodeArrayMoon.append(i)
  for j in range(0,len(oddNodeArrayMoon)-1):
    for k in range(j+1,len(oddNodeArrayMoon)):
      oddNodeRoutesMoon.append([uRouteList[oddNodeArrayMoon[j]][oddNodeArrayMoon[k]],oddNodeArrayMoon[j],oddNodeArrayMoon[k]])
  oddNodeRoutesMoon = sorted(oddNodeRoutesMoon)
  nodes = [oddNodeRoutesMoon[0][1],oddNodeRoutesMoon[0][2]]
  mstGraphMoon[0].append((oddNodeRoutesMoon[0][1],oddNodeRoutesMoon[0][2]))
  stopped = False
  for m in range(1,len(oddNodeRoutesMoon)):
    for n in range(0,len(nodes)):
      if (nodes[n] in oddNodeRoutesMoon[m]):
        stopped = True
        break
    if stopped == False:
      mstGraphMoon[0].append((oddNodeRoutesMoon[m][1],oddNodeRoutesMoon[m][2]))
      nodes.extend([oddNodeRoutesMoon[m][1],oddNodeRoutesMoon[m][2]])
    else:
      stopped = False
  location = moonParent
  finalRouteMoon = [moonParent]
  while (len(finalRouteMoon) < len(moonList)+1):
    stopped2 = False
    for p in range(0,len(mstGraphMoon[0])):
      if mstGraphMoon[0][p][0] == location:
        if mstGraphMoon[0][p][1] not in finalRouteMoon:
          finalRouteMoon.insert(finalRouteMoon.index(location)+1,mstGraphMoon[0][p][1])
          location = mstGraphMoon[0][p][1]
          mstGraphMoon[0].pop(p)
          stopped2 = True
          break
        else:
          mstGraphMoon[0].pop(p)
          
          break
      elif mstGraphMoon[0][p][1] == location:
        if mstGraphMoon[0][p][0] not in finalRouteMoon:
          finalRouteMoon.insert(finalRouteMoon.index(location)+1,mstGraphMoon[0][p][0])
          location = mstGraphMoon[0][p][0]
          mstGraphMoon[0].pop(p)
          stopped2 = True
          break
        else:
          mstGraphMoon[0].pop(p)
          break
    if stopped2 == True:
      continue
    else:
      location = finalRouteMoon[finalRouteMoon.index(location)-1]
  finalRouteMoon.pop(0)
  return finalRouteMoon
### 
def christofides(uRoutePlanets, uRouteMoons, uRouteList):
  planets = christofidesPlanets(uRoutePlanets)
  finalRouteAll = planets
  totalLength = 0
  for sectors in range(0,len(planets)):
    moons = christofidesMoons(uRouteList,sectors,uRouteMoons[sectors])
    finalRouteAll[finalRouteAll.index(sectors)+1:1] = moons
  for length in range(1,len(finalRouteAll)):
    totalLength += uRouteList[finalRouteAll[length-1]][finalRouteAll[length]]
  return finalRouteAll,totalLength

#print(christofides(tempArr,tempArrMoon,routeList))