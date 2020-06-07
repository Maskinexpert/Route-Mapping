# This algorithm takes an array of routes between only the planets, 2d list of moons sorted into rows with the same parent, full route list.
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs given to christofidesMoons, m = mst edges for moons, p = amount of planets, q = mst edges for planets 

import Kruskal as kru

def christofidesPlanets(uRoutePlanets):
  oddNodeCounter = []
  oddNodeArray = []
  oddNodeRoutes = []
  # The minimum spanning tree is generated from the route list between planets
  mstGraph = kru.kruskal(uRoutePlanets) # O(p log p) (since time complexity of kruskal is O(E log V) and E = SUM(i = 1,p,i+=1) = (some constant c)*p = O(n))
  # A list of nodes with odd number of egdes attached is generated (list of odd nodes)
  for edges in range(0,len(mstGraph[0])+1): # O(p)
    oddNodeCounter.append(0)
  for edges in range(0,len(mstGraph[0])): # O(q)
    oddNodeCounter[mstGraph[0][edges][0]] += 1
    oddNodeCounter[mstGraph[0][edges][1]] += 1
  for i in range(0,len(oddNodeCounter)): # O(p)
    if (oddNodeCounter[i]%2) == 1:
      oddNodeArray.append(i)
  # A list of routes between each odd node is generated and sorted in order of increasing weight
  for j in range(0,len(oddNodeArray)-1): # O(p^2) (worst case where all nodes have odd number of edges attached)
    for k in range(j+1,len(oddNodeArray)): # O(p)
      oddNodeRoutes.append([uRoutePlanets[oddNodeArray[j]][oddNodeArray[k]],oddNodeArray[j],oddNodeArray[k]])
  oddNodeRoutes = sorted(oddNodeRoutes) # O(p log p)
  # Increasingly heavier routes is added to the mst-graph making each node even, but each node can only be added once so it doesn't become odd again.
  # The mst-graph now becomes and euler tour
  nodes = [oddNodeRoutes[0][1],oddNodeRoutes[0][2]]
  mstGraph[0].append((oddNodeRoutes[0][1],oddNodeRoutes[0][2]))
  stopped = False
  for m in range(1,len(oddNodeRoutes)): # O(p^3)
    for n in range(0,len(nodes)): # O(p^2) (worst case where all planet nodes except 2 is in nodes) 
      if (nodes[n] in oddNodeRoutes[m]): # O(p)
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
  # Each node of the generated euler tour is added, but skipping nodes already included in the final route
  while (len(finalRoute) < len(uRoutePlanets)): # O(p^3) (since the iterations of the loop is related to the amount of elements in mstGraph which is maximum 2p)
    stopped2 = False
    for p in range(0,len(mstGraph[0])): # O(p^2) (O(p) for mstGraph since the length of mstGraph is at maximum twice the amount of planet nodes minus 2)
      if mstGraph[0][p][0] == location:
        if mstGraph[0][p][1] not in finalRoute: # O(p)
          finalRoute.insert(finalRoute.index(location)+1,mstGraph[0][p][1]) # O(p)
          location = mstGraph[0][p][1]
          mstGraph[0].pop(p) # O(p) (worst case if location is the last in mstGraph)
          stopped2 = True
          break
        else:
          mstGraph[0].pop(p) # O(p)
          break
      elif mstGraph[0][p][1] == location:
        if mstGraph[0][p][0] not in finalRoute: # O(p)
          finalRoute.insert(finalRoute.index(location)+1,mstGraph[0][p][0]) # O(p)
          location = mstGraph[0][p][0]
          mstGraph[0].pop(p) # O(p) (worst case if location is the last in mstGraph)
          stopped2 = True
          break
        else:
          mstGraph[0].pop(p) # O(p)
          break
    if stopped2 == True:
      continue
    else:
      location = finalRoute[finalRoute.index(location)-1] # O(p)
 # O(p log p) + O(p) + O(q) + O(p) + O(p^2) + O(p log p) + O(p^3) + O(p^3) + O(p) = O(p^3)
  return finalRoute


def christofidesMoons(uRouteList,moonParent,moonList):
  moonArray = []
  allList = [moonParent]
  allList.extend(moonList)
  for c in range(0,len(allList)): # O(n^2)
    moonArray.append([])
    for d in range(0,len(allList)): # O(n)
      moonArray[c].append(uRouteList[c][d])
  oddNodeCounterMoon = []
  oddNodeArrayMoon =[]
  oddNodeRoutesMoon = []
  # The minimum spanning tree is generated from the route list between planets
  mstGraphMoon = kru.kruskal(moonArray) # O(n log n) (since time complexity of kruskal is O(E log V) and E = SUM(i = 1,n,i+=1) = (some constant c)*n = O(n))
  for items in range(0,len(mstGraphMoon[0])): # O(m)
    mstGraphMoon[0][items] = (allList[mstGraphMoon[0][items][0]],allList[mstGraphMoon[0][items][1]])
  # A list of nodes with odd number of egdes attached is generated (list of odd nodes)
  for edges in range(0,len(mstGraphMoon[0])+1): # O(n)
    oddNodeCounterMoon.append(0)
  for edges in range(0,len(mstGraphMoon[0])): # O(m)
    oddNodeCounterMoon[allList.index(mstGraphMoon[0][edges][0])] += 1
    oddNodeCounterMoon[allList.index(mstGraphMoon[0][edges][1])] += 1
  for i in range(0,len(oddNodeCounterMoon)): # O(n)
    if (oddNodeCounterMoon[i]%2) == 1:
      oddNodeArrayMoon.append(i)
  # A list of routes between each odd node is generated and sorted in order of increasing weight
  for j in range(0,len(oddNodeArrayMoon)-1): # O(n^2) (worst case where all nodes have odd number of edges attached)
    for k in range(j+1,len(oddNodeArrayMoon)): # O(n)
      oddNodeRoutesMoon.append([uRouteList[oddNodeArrayMoon[j]][oddNodeArrayMoon[k]],oddNodeArrayMoon[j],oddNodeArrayMoon[k]])
  oddNodeRoutesMoon = sorted(oddNodeRoutesMoon) # O(n log n)
  # Increasingly heavier routes is added to the mst-graph making each node even, but each node can only be added once so it doesn't become odd again.
  # The mst-graph now becomes and euler tour
  nodes = [oddNodeRoutesMoon[0][1],oddNodeRoutesMoon[0][2]]
  mstGraphMoon[0].append((oddNodeRoutesMoon[0][1],oddNodeRoutesMoon[0][2]))
  stopped = False
  for m in range(1,len(oddNodeRoutesMoon)): # O(n^3)
    for n in range(0,len(nodes)): # O(n^2) (worst case where all nodes except 2 is in nodes list)
      if (nodes[n] in oddNodeRoutesMoon[m]): # O(n)
        stopped = True
        break
    if stopped == False:
      mstGraphMoon[0].append((oddNodeRoutesMoon[m][1],oddNodeRoutesMoon[m][2]))
      nodes.extend([oddNodeRoutesMoon[m][1],oddNodeRoutesMoon[m][2]])
    else:
      stopped = False
  location = moonParent
  finalRouteMoon = [moonParent]
  # Each node of the generated euler tour is added, but skipping nodes already included in the final route
  while (len(finalRouteMoon) < len(moonList)+1): # O(n^3) (since the iterations of the loop is related to the amount of elements in mstGraphMoon which is maximum 2n)
    stopped2 = False
    for p in range(0,len(mstGraphMoon[0])): # O(n^2) (O(n) for mstGraphMoon since the length of mstGraphMoon is at maximum twice the amount of planet nodes minus 2)
      if mstGraphMoon[0][p][0] == location:
        if mstGraphMoon[0][p][1] not in finalRouteMoon: # O(n)
          finalRouteMoon.insert(finalRouteMoon.index(location)+1,mstGraphMoon[0][p][1]) # O(n)
          location = mstGraphMoon[0][p][1]
          mstGraphMoon[0].pop(p) # O(n) (worst case if location is the last in mstGraphMoon)
          stopped2 = True
          break
        else: 
          mstGraphMoon[0].pop(p) # O(n)
          break
      elif mstGraphMoon[0][p][1] == location:
        if mstGraphMoon[0][p][0] not in finalRouteMoon: # O(n)
          finalRouteMoon.insert(finalRouteMoon.index(location)+1,mstGraphMoon[0][p][0]) # O(n)
          location = mstGraphMoon[0][p][0]
          mstGraphMoon[0].pop(p) # O(n)
          stopped2 = True
          break
        else:
          mstGraphMoon[0].pop(p) # O(n)
          break
    if stopped2 == True:
      continue
    else:
      location = finalRouteMoon[finalRouteMoon.index(location)-1] # O(n)
  finalRouteMoon.pop(0)
  # O(n^2) + O(n) + O(n log n) + O(m) + O(n) + O(m) O(n) + O(n^2) + O(n log n) + O(n^3) + O(n^3) = O(n^3)
  return finalRouteMoon
### 
def christofides(uRoutePlanets, uRouteMoons, uRouteList):
  # A Christofides heuristic is applied to the list of planets
  planets = christofidesPlanets(uRoutePlanets) # O(p^3)
  finalRouteAll = planets
  totalLength = 0
  # A Christofides heuristic is applied to the list of moons for each planet sector 
  for sectors in range(0,len(planets)): # O(p*n^3)
    moons = christofidesMoons(uRouteList,sectors,uRouteMoons[sectors]) # O(n^3)
    finalRouteAll[finalRouteAll.index(sectors)+1:1] = moons # O((p*n)+n) (worst case when the last array of moons is added to the end of the list)
  # A final route length is calculated from final route
  for length in range(1,len(finalRouteAll)): # O(p+(p*n))
    totalLength += uRouteList[finalRouteAll[length-1]][finalRouteAll[length]]
  # O(p^3) + O(p*n^3) + O(p+(p*n)) = O(p^3 + p*n^3)
  # Route and length is returned
  return finalRouteAll,totalLength

#print(christofides(tempArr,tempArrMoon,routeList))