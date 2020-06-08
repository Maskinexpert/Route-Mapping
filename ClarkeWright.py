# This algorithm takes 3 arrays as input: array of only planet routes, 2d list of moons sorted into rows with the same parent, full route list.
  # Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs given to moonCalculations, m = total route combinations for moons, p = amount of planets, q = total route combinations for planets 
degreeList = []
degreeListMoon = []
# Used to calculate the distance saved from taking the shortcut x => y instead of taking the route x => main node => y
def savings(uRoute,x,y):
  savedDistance = uRoute[0][x] + uRoute[0][y] - uRoute[x][y]
  return savedDistance
# Used to calculate the distance saved from taking the shortcut moonX => moonY
def moonSavings(uRouteList,parent,x,y):
  moonSavedDistance = uRouteList[x][parent] + uRouteList[y][parent] - uRouteList[x][y]
  return moonSavedDistance

# A check to see if the current node already is in the degreeList which means they have an edge connected to it
def degree(x):
  if x in degreeList: # O(p) (worst case)
    return 1
  else:
    degreeList.append(x)
    return 0
# A similar check to the degree function but only for moons
def degreeMoon(x):
  if x in degreeListMoon: # O(n) (worst case)
    return 1
  else:
    degreeListMoon.append(x)
    return 0

# moonsCalculations is a function made to repeat the actions of the main program but for each planet sector.
# It takes the list of moons for the sector, the planet in the sector, and the full list of routes to look distance between each celestial body
def moonsCalculations(uRouteMoons,planetParent,uRouteList):
  savingsArrayMoons = []
  m = []
  tourMoon = []
  maxTourMoon = len(uRouteMoons[planetParent])-1 
  # The total amount for each possible shortcut is stored in savingsArrayMoons and then sorted in decreasing order
  for i in range(0,len(uRouteMoons[planetParent])-1): # O(n^2) (for the entire nested loop)
    for k in range(i+1,len(uRouteMoons[planetParent])):
      savingsArrayMoons.append((moonSavings(uRouteList,planetParent,uRouteMoons[planetParent][i],uRouteMoons[planetParent][k]),uRouteMoons[planetParent][i],uRouteMoons[planetParent][k]))
  sortedSavingsArrayMoon = sorted(savingsArrayMoons,reverse = True) # O(m log m)
  tourMoon = []
  # Going through the list of saved distance adding edges to the solution that does not construct a loop, or connects to nodes that already have 2 edges connected
  for o in range(0,len(sortedSavingsArrayMoon)): # O(m*6n) (worst case for the entire loop where )
    if ((sortedSavingsArrayMoon[o][1] in degreeListMoon) and (sortedSavingsArrayMoon[o][2] in degreeListMoon) and m != []) or ((sortedSavingsArrayMoon[o][1] in m) or (sortedSavingsArrayMoon[o][2] in m)): # O(4n) (worst case if either degreeListMoon or m contain all nodes)
      continue
    tourMoon.append((uRouteList[sortedSavingsArrayMoon[o][1]][sortedSavingsArrayMoon[o][2]],sortedSavingsArrayMoon[o][1],sortedSavingsArrayMoon[o][2]))
    # Nodes are added to the m list if they have 2 edges connected 
    if degreeMoon(sortedSavingsArrayMoon[o][1]) == 1: # O(n) (worst case)
      m.append(sortedSavingsArrayMoon[o][1])
    if degreeMoon(sortedSavingsArrayMoon[o][2]) == 1: # O(n) (worst case)
      m.append(sortedSavingsArrayMoon[o][2])
    # If a complete route is found skip the remaining edges
    if len(m) == maxTourMoon:
      break
  # Figure out which nodes does not have 2 edges connected to them, and the one with shortest route to the parent node gets added to the solution
  for q in m: # O(n^2) (total for loop)
    degreeListMoon.remove(q) # O(n)
  remainingRoute = min((uRouteList[degreeListMoon[0]][planetParent],planetParent,degreeListMoon[0]),(uRouteList[degreeListMoon[1]][planetParent],planetParent,degreeListMoon[1]))
  tourMoon.append(remainingRoute)

  location = planetParent
  moonCalRoute = []
  moonsWeight = 0
  # Each edge is then added to the final result in order of starting location => node2, node2 => node3
  for ea in range(0,len(tourMoon)): # O(n^3) (worst case for the entire loop)
    for ro in range(0,len(tourMoon)):
      if tourMoon[ro][1] == location:
        moonsWeight += tourMoon[ro][0]
        location = tourMoon[ro][2]
        moonCalRoute.append(location)
        tourMoon.pop(ro) # O(n) (worst case where element ro is the last element in the list)
        break
      if tourMoon[ro][2] == location:
        moonsWeight += tourMoon[ro][0]
        location = tourMoon[ro][1]
        moonCalRoute.append(location)
        tourMoon.pop(ro) # O(n) (worst case)
        break
  # O(n^2) + O(m log m) + O(m*6n) + O(n^2) + O(n^3) = O(n^3)
  return moonsWeight, moonCalRoute

def clarkeWright (uRoutePlanets, uRouteMoons, uRouteList):
  savingsArray = []
  l = []
  tour = []
  edgeList = []
  maxTour = len(uRoutePlanets)-1
  node1 = (-1,-1)
  node2 = (-2,-2)
  # The total amount for each possible shortcut is stored in savingsArray and then sorted in decreasing order
  for i in range(1,len(uRoutePlanets)-1): #O(p^2) (for the entire loop)
    for k in range(i+1,len(uRoutePlanets)):
      savingsArray.append((savings(uRoutePlanets,i,k),i,k))
  sortedSavingsArray = sorted(savingsArray,reverse = True) # O(q log q)
  # Going through the list of saved distance adding edges to the solution that does not construct a loop, or connects to nodes that already have 2 edges connected
  for o in range(0,len(sortedSavingsArray)): # O(q*(2p+2p*q^2+p)) = O(2p*q^3+2p*q+p*q) (total for entire loop)
    # If node1 and node2 are in the same "chain" of edges is the edge skipped
    if ((sortedSavingsArray[o][1] in l) or (sortedSavingsArray[o][2] in l)): # O(2p) (worst case if l contains all nodes)
      continue
    # Adds node1 or node2 to the "chain" where the other node exists, but not if they are in the same "chain". If neither is in a "chain" make new "chain"
    elif ((sortedSavingsArray[o][1] in degreeList) or (sortedSavingsArray[o][2] in degreeList)): # O(2p*q^2)
      for i in range(0,len(edgeList)): # O(q^2) 
        for k in edgeList[i]: # (worst case O(q-1) which equals to O(q))
          if sortedSavingsArray[o][1] == k:
            node1 = (k,i)
          if sortedSavingsArray[o][2] == k:
            node2 = (k,i)
      if node1[1] == node2[1]:
        node1 = (-1,-1)
        node2 = (-2,-2)
        continue
      # Catches cases where node1 and node2 are in a chain but not the same chain
      elif ((node1[0] > -1) and (node2[0] > -1)):
        edgeList[node1[1]].extend(edgeList[node2[1]]) # O(p) (worst case)
        del edgeList[node2[1]]
        node1 = (-1,-1)
        node2 = (-2,-2)
      # If either node1 or node2 are in a "chain" add the other node to that "chain"
      elif (node1[0] > -1):
        edgeList[node1[1]].append(sortedSavingsArray[o][2])
      else:
        edgeList[node2[1]].append(sortedSavingsArray[o][1])
    else:
      edgeList.append([sortedSavingsArray[o][1],sortedSavingsArray[o][2]])
    # Edge is added to tour and nodes are added to the l list if they have 2 edges connected
    tour.append((uRoutePlanets[sortedSavingsArray[o][1]][sortedSavingsArray[o][2]],sortedSavingsArray[o][1],sortedSavingsArray[o][2]))
    if degree(sortedSavingsArray[o][1]) == 1:
      l.append(sortedSavingsArray[o][1])
    if degree(sortedSavingsArray[o][2]) == 1:
      l.append(sortedSavingsArray[o][2])
    if len(l) == maxTour:
      break
  # Figure out which nodes does not have 2 edges connected to them, and the one with shortest route to the parent node gets added to the solution
  for p in l: # O(p^2)
    degreeList.remove(p)
  remainingRoute = min((uRoutePlanets[0][degreeList[0]],0,degreeList[0]),(uRoutePlanets[0][degreeList[1]],0,degreeList[1]))
  tour.append(remainingRoute)
  result = []
  # The subroute of moons for each sector collected to 1 array
  for planetParent in range(0,len(uRouteMoons)): # O(p*n^3)
    result.extend([moonsCalculations(uRouteMoons,planetParent,uRouteList)])
    del degreeListMoon[:]
  
  # Each edge is then added to the final length in order of starting location => node2, node2 => node3, and the nodes are added to the final route
  location = 0
  cwRoute = [0]
  cwRoute.extend(result[0][1])
  weight = result[0][0]
  for ea in range(0,len(tour)): # O(p^2*n)
    for ro in range(0,len(tour)): # O(p*n)
      if tour[ro][1] == location:
        location = tour[ro][2]
        weight += tour[ro][0] + result[location][0]
        cwRoute.append(location)
        cwRoute.extend(result[location][1]) # O(n)
        tour.pop(ro)
        break
      if tour[ro][2] == location:
        location = tour[ro][1]
        weight += tour[ro][0] + result[location][0]
        cwRoute.append(location)
        cwRoute.extend(result[location][1]) # O(n)
        tour.pop(ro)
        break
  
  # O(p^2) + O(q log q) + O(2p*q^3 + 2p*q + p*q) + O(p^2) + O(p*n^3) + O(p^2*n) = O(2p*q^3) + O(p*n^3)
  # Final route and length is returned
  return cwRoute, weight
#print(clarkeWright(tempArr,tempArrMoon,routeList))