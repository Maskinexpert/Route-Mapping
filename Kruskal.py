#Temp for testing
import UniverseBuilder as u
from sys import maxsize


uniStore = u.uniBuilder()
routeList = uniStore[0]
#routeMarkerKeys = uniStore[1]
routeMarkers = uniStore[2]
#hiarchy = uniStore[3]
#

###################################
##NEVER USE WITH FULL EDGE MATRIX##
###################################
def Kruskal(uRoute, freshRouteKeys):
  if (len(uRoute[0]) > 12):
    #Incase a too large edge array is used
    print("Too many edges to calculate for this Kruskal implementation")
    return 0
  sortedRoutes = []
  edgeList = [[]]
  for i in range(0,len(uRoute)-1):
    for k in range(i+1,len(uRoute)):
      sortedRoutes.append((uRoute[i][k],i,k))
  sortedRoutes = sorted(sortedRoutes)
  edgeList =[[(sortedRoutes[0][1],sortedRoutes[0][2])]]
  
  for r in range(0,len(sortedRoutes)):
    node1 = -1
    node2 = -1
#    print(r)
    for s in range(0,len(edgeList)):
      for t in range(0,len(edgeList[s])):
        if (sortedRoutes[r][1] in edgeList[s][t]) or (sortedRoutes[r][1] in edgeList[s][t]) :
          node1 = s
        if (sortedRoutes[r][2] in edgeList[s]) or (sortedRoutes[r][2] in edgeList[s]):
          node2 = s
      if(node1 == node2) and (node1 > -1):
        break
      elif(node1 > -1):
        edgeList[node1].append((sortedRoutes[r][1],sortedRoutes[r][2]))
        if (node2 > -1):
          edgeList[node1].extend(edgeList[node2])
          del edgeList[node2]
      elif(node2 > -1):
        edgeList[node2].append((sortedRoutes[r][1],sortedRoutes[r][2]))
      else:
        edgeList.append([(sortedRoutes[r][1],sortedRoutes[r][2])])

  print(edgeList)
Kruskal(routeList,routeMarkers)