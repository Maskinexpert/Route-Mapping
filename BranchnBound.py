# This algorithm takes an list of planets, 2d list of moons sorted into rows with the same parent, full route list.
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs, p = amount of planet nodes, a = all nodes in the route list
import math 
maxsize = float('inf') 
nodeTree = {}
upperBound = maxsize

# Parent is the node location in nodeTree dictionary rather than the planet number
class node:
  def __init__(self, location, planetName, matrix, cost, depth, *parent):
    self.l = location
    self.n = planetName
    self.m = matrix
    self.c = cost
    self.d = depth
    self.p = parent

def weightCalBnB(tour,uRouteList):
  totalLengthBnB = 0
  for lengthBnB in range(0,len(tour)-1): # O(p)
    totalLengthBnB += uRouteList[lengthBnB][lengthBnB+1]
  # O(p)
  return totalLengthBnB

def listCopier(uRoute):
  tempArr = []
  for items in range(0,len(uRoute)): # O(a)
    tempArr.append(list(uRoute[items]))
  # O(a)
  return tempArr


def reducer(uRoute):
  #First rows
  reducedWeight = 0
  for i in range(0,len(uRoute)): # O(p^2)
    rowSmall = min(uRoute[i]) # O(p)
    if rowSmall == maxsize:
      continue
    reducedWeight += rowSmall
    for k in range(0,len(uRoute[i])): # O(p)
      uRoute[i][k] -= rowSmall
  #Then coloumns
  for j in range(0,len(uRoute)): # O(p^2)
    colSmall = maxsize
    for l in range(0,len(uRoute)): # O(p)
      if uRoute[l][j] < colSmall:
        colSmall = uRoute[l][j]
    if colSmall == maxsize:
      continue
    for m in range(0,len(uRoute)): # O(p)
      uRoute[m][j] -= colSmall
    reducedWeight += colSmall
  # O(p^2) + O(p^2) = O(p^2) 
  return uRoute,reducedWeight
  
def removeNode(uRoute,node,parent):
  for i in range(0,len(uRoute)): # O(p)
    try:
      uRoute[parent][i] = maxsize
    except:
      continue
  for j in range(0,len(uRoute)): # O(p)
      uRoute[j][node] = maxsize
      uRoute[j][parent] = maxsize
  # O(p) + O(p) = O(p)
  return uRoute
### Takes the location in the nodeTree dictionary as input and the current route ### 
def pathBuilder(node, length):
  currentRoute = []
  currentNode = node
  for i in range(0,length): # O(p)
    currentRoute = [nodeTree[currentNode].n] + currentRoute
    currentNode = nodeTree[currentNode].p[0]
  # O(p)
  return currentRoute
  
def recursiveStepBnB(uRoute,startLocation,parent,currentDepth):
  level = currentDepth + 1
  stepList = listCopier(uRoute) # O(a)
  removeNode(stepList,startLocation,nodeTree[parent].n) # O(p)
  stepList, stepCost = reducer(stepList) # O(p^2)
  stepCost += (nodeTree[parent].c + nodeTree[parent].m[nodeTree[parent].n][startLocation])
  currentLocation = (list(nodeTree)[-1])+1 # O(p!) (since copying a list linear, but the length of the list is p! if all possible routes are present) 
  nodeTree[currentLocation] = node(currentLocation, startLocation, stepList, stepCost, level, parent)
  global upperBound
  if stepCost >= upperBound:
    return
  elif level == len(uRoute)-1:
    upperBound = stepCost
    return
  for x in (x for x in range(0,len(stepList)) if stepList[startLocation][x] != maxsize): # O(p!)
    recursiveStepBnB(nodeTree[currentLocation].m,x,currentLocation,level)
  # O(a) + O(p) + O(p^2) + O(p!) + O(p!) = O(p!)
  return 
  
  ### Takes 2d array of planet distances, 
def branchnBound(uRoutePl, uRouteMn, uRouteList):
  bnbPlList = listCopier(uRoutePl) # O(p)
  for elementRow in range(0,len(bnbPlList)): # O(p^2)
    for elementCol in range(0,len(bnbPlList[elementRow])): # O(p)
      if bnbPlList[elementRow][elementCol] == 0:
        bnbPlList[elementRow][elementCol] = maxsize
  global nodeTree
  finalRouteAll = [0]
  reducedTable, cost = reducer(bnbPlList) # O(p^2)
  nodeTree[0] = node(0, 0, reducedTable, cost, 0)
  for nodes in range(1,len(uRoutePl)): # O(p*p!)
    recursiveStepBnB(nodeTree[0].m,nodes,nodeTree[0].l,0) # O(p!)
  global upperBound
  for keys in nodeTree: # O(p!+p) (since contents of the if statement is only run once, is the worst case time complexity going through the entire p! long nodeTree and then doing and action that costs p) 
    if nodeTree[keys].c == upperBound and nodeTree[keys].d == len(uRoutePl)-1:
      lastNode = nodeTree[keys].l
      finalRouteAll.extend(pathBuilder(lastNode, len(uRoutePl)-1)) # O(p)
      break
  moonTours = []
  for items in range(0,len(uRouteMn)): # O((p*n!)+(p^2*n)+(p*n))
    upperBound = maxsize
    nodeTree = {}
    uRouteMnCopy = list(uRouteMn[items]) # O(n)
    uRouteMnCopy = [items] + uRouteMnCopy
    moonArray = []
    moonTempArray = []
    for sectorRow in range(0,len(uRouteMnCopy)): # O(n^2)
      moonTempArray = []
      for sectorCol in range(0,len(uRouteMnCopy)): # O(n)
        moonTempArray.append(uRouteList[uRouteMnCopy[sectorRow]][uRouteMnCopy[sectorCol]])
      moonArray.append(list(moonTempArray))
    for elementRow in range(0,len(moonArray)): # O(n^2)
      for elementCol in range(0,len(moonArray[elementRow])): # O(n)
        if moonArray[elementRow][elementCol] == 0:
          moonArray[elementRow][elementCol] = maxsize
    reducedMoonTable, moonCost = reducer(moonArray) # O(n^2)
    nodeTree[0] = node(0, 0, reducedMoonTable, moonCost, 0)
    for nodes in range(1,len(moonArray)): # O(n!)
      recursiveStepBnB(nodeTree[0].m,nodes,nodeTree[0].l,0)
    for keys in nodeTree: # O(n!+(p*n)+n)
      if nodeTree[keys].c == upperBound and nodeTree[keys].d == len(moonArray)-1:
        lastNode = nodeTree[keys].l
        moons = pathBuilder(lastNode, len(moonArray)-1) # O(n)
        convertedMoons = []
        for moonIndex in moons: # O(n)
          convertedMoons.append(uRouteMnCopy[moonIndex])
        finalRouteAll[finalRouteAll.index(items)+1:1] = convertedMoons # O((p*n)+n)
        break
  finalRouteWeight = 0
  for xBnB in range(0,len(finalRouteAll)-1): # O(p*n)
    finalRouteWeight += uRouteList[finalRouteAll[xBnB]][finalRouteAll[xBnB+1]]
  
  # O(p) + O((p*n!)+(p^2*n)+(p*n)) + O(p^2) + O(p^2) + O(p*n) + O(p!+p) + O(p*p!) = O(p*p!)
  return finalRouteAll, finalRouteWeight
