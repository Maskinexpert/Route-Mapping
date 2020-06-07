# This algorithm takes an list of planets, 2d list of moons sorted into rows with the same parent, full route list.
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = amount of moon inputs, m = all possible routes for moons, p = amount of planet nodes,
                                   # q = all possible routes for the set of planets, a = all nodes in the route list
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
  return uRoute,reducedWeight
  
def removeNode(uRoute,node,parent):
  for i in range(0,len(uRoute)):
    try:
      uRoute[parent][i] = maxsize
    except:
      print(parent)
  for j in range(0,len(uRoute)):
      uRoute[j][node] = maxsize
      uRoute[j][parent] = maxsize
  return uRoute
### Takes the location in the nodeTree dictionary as input and the current route ### 
def pathBuilder(node, length):
  currentRoute = []
  currentNode = node
  for i in range(0,length):
    currentRoute = [nodeTree[currentNode].n] + currentRoute
    currentNode = nodeTree[currentNode].p[0]
  return currentRoute
  
def recursiveStepBnB(uRoute,startLocation,parent,currentDepth):
  level = currentDepth + 1
  stepList = listCopier(uRoute)
  removeNode(stepList,startLocation,nodeTree[parent].n)
  stepList, stepCost = reducer(stepList)
  stepCost += (nodeTree[parent].c + nodeTree[parent].m[nodeTree[parent].n][startLocation])
  if stepCost == maxsize:
    print(nodeTree[parent].m[nodeTree[parent].n][startLocation])

  currentLocation = (list(nodeTree)[-1])+1
  nodeTree[currentLocation] = node(currentLocation, startLocation, stepList, stepCost, level, parent)
  global upperBound
  if stepCost >= upperBound:
    return
  elif level == len(uRoute)-1:
    upperBound = stepCost
    return
  for x in (x for x in range(0,len(stepList)) if stepList[startLocation][x] != maxsize):
    recursiveStepBnB(nodeTree[currentLocation].m,x,currentLocation,level)
  return 
  
  ### Takes 2d array of planet distances, 
def branchnBound(uRoutePl, uRouteMn, uRouteList):
  bnbPlList = listCopier(uRoutePl)
  for elementRow in range(0,len(bnbPlList)):
    for elementCol in range(0,len(bnbPlList[elementRow])):
      if bnbPlList[elementRow][elementCol] == 0:
        bnbPlList[elementRow][elementCol] = maxsize
  global nodeTree
  finalRouteAll = [0]
  reducedTable, cost = reducer(bnbPlList)
  nodeTree[0] = node(0, 0, reducedTable, cost, 0)
  for nodes in range(1,len(uRoutePl)):
    recursiveStepBnB(nodeTree[0].m,nodes,nodeTree[0].l,0)
  global upperBound
  for keys in nodeTree:
    if nodeTree[keys].c == upperBound and nodeTree[keys].d == len(uRoutePl)-1:
      lastNode = nodeTree[keys].l
      finalRouteAll.extend(pathBuilder(lastNode, len(uRoutePl)-1))
      break
  moonTours = []
  for items in range(0,len(uRouteMn)):
    upperBound = maxsize
    nodeTree = {}
    uRouteMnCopy = list(uRouteMn[items])
    uRouteMnCopy = [items] + uRouteMnCopy
    moonArray = []
    moonTempArray = []
    for sectorRow in range(0,len(uRouteMnCopy)):
      moonTempArray = []
      for sectorCol in range(0,len(uRouteMnCopy)):
        moonTempArray.append(uRouteList[uRouteMnCopy[sectorRow]][uRouteMnCopy[sectorCol]])
      moonArray.append(list(moonTempArray))
    for elementRow in range(0,len(moonArray)):
      for elementCol in range(0,len(moonArray[elementRow])):
        if moonArray[elementRow][elementCol] == 0:
          moonArray[elementRow][elementCol] = maxsize
    reducedMoonTable, moonCost = reducer(moonArray)
    nodeTree[0] = node(0, 0, reducedMoonTable, moonCost, 0)
    for nodes in range(1,len(moonArray)):
      recursiveStepBnB(nodeTree[0].m,nodes,nodeTree[0].l,0)
    for keys in nodeTree:
      if nodeTree[keys].c == upperBound and nodeTree[keys].d == len(moonArray)-1:
        lastNode = nodeTree[keys].l
        moons = pathBuilder(lastNode, len(moonArray)-1)
        convertedMoons = []
        for moonIndex in moons:
          convertedMoons.append(uRouteMnCopy[moonIndex])
        finalRouteAll[finalRouteAll.index(items)+1:1] = convertedMoons
        break
  finalRouteWeight = 0
  for xBnB in range(0,len(finalRouteAll)-1):
    finalRouteWeight += uRouteList[finalRouteAll[xBnB]][finalRouteAll[xBnB+1]]

  
  return finalRouteAll, finalRouteWeight
