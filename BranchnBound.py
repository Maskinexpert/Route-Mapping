
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
#def listCopier(uRoute,startEnd):
#  tempArr = []
#  for items in range(startEnd[0],startEnd[1]):
#    tempArr.append(list(uRoute[items]))
#  return tempArr

#for items in range(0,tempLength):
#  tempArr.append(list(routeList[items]))
#for slot1 in range(0,len(tempArr)):
#  for slot in range(tempLength,len(routeList)):
#    tempArr[slot1].pop(tempLength)
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
#### 2d array of moon plus parent planet distances  
#for sections in tempArrMoon:
#  for items2 in range(0,len(tempArrMoon[sections])):
    



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
  for lengthBnB in range(0,len(tour)-1):
    totalLengthBnB += uRouteList[lengthBnB][lengthBnB+1]
  return totalLengthBnB

def listCopier(uRoute):
  tempArr = []
  for items in range(0,len(uRoute)):
    tempArr.append(list(uRoute[items]))
  return tempArr


def reducer(uRoute):
  #First rows
  reducedWeight = 0
  for i in range(0,len(uRoute)):
    rowSmall = min(uRoute[i])
    if rowSmall == maxsize:
      continue
    reducedWeight += rowSmall
    for k in range(0,len(uRoute[i])):
      uRoute[i][k] -= rowSmall
  #Then coloumns
  for j in range(0,len(uRoute)):
    colSmall = maxsize
    for l in range(0,len(uRoute)):
      if uRoute[l][j] < colSmall:
        colSmall = uRoute[l][j]
    if colSmall == maxsize:
      continue
    for m in range(0,len(uRoute)):
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
#  for v in stepList:
#    for el in v:
#      print(str(el).rjust(6,' ')+' ', end = '')
#    print(' ')
#  for kl in range(0,2):
#    for lkj in range(0,len(stepList)):
#      print('_', end = '')
#  print(" ")
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
  #finalRouteWeight = weightCalBnB(finalRouteAll,uRouteList)
  
  return finalRouteAll, finalRouteWeight
  
#c = branchnBound(tempArr,tempArrMoon, routeList)

#print(c)
#detert = nodeTree[nodeTree[nodeTree[lastNode].p[0]].p[0]].m
#detert2 = nodeTree[nodeTree[lastNode].p[0]].m
#print(c)
#detert = nodeTree[list(nodeTree)[-1]].m
#dp = nodeTree[list(nodeTree)[-1]].p
#dp2 = nodeTree[1].p
#print(dp2)
#for v in detert:
#  for el in v:
#    print(str(el).rjust(6,' ')+' ', end = '')
#  print(' ')