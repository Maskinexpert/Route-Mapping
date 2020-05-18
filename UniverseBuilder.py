from random import seed
from random import randint
seed()
import math
#TODO: 
# Delete print_graph

class Vertex:
  def __init__(self, n, p, *m):
    self.name = n
    self.parent = p
    if not m:
      self.isMoon = False
    else:
      self.isMoon = True

class RouteMapper:
  celBodies = {}
  routes = []
  route_marker = {}
  
  def addCelBody(self,celBody):
    if isinstance(celBody,Vertex) and celBody.name not in self.celBodies:
      self.celBodies[celBody.name] = celBody
      for row in self.routes:
        row.append(0)
      self.routes.append([0]*(len(self.routes)+1))
      self.route_marker[celBody.name] = len(self.route_marker)
      return True
    else:
      return False
    
  def addRoute(self,u,v,baseLength = 30000):
    if u in self.celBodies and v in self.celBodies:
      if (r.celBodies[v].isMoon != True and r.celBodies[u].isMoon != True) or r.route_marker[r.celBodies[u].parent] == r.route_marker[v]:
        self.routes[self.route_marker[u]][self.route_marker[v]] = baseLength
        self.routes[self.route_marker[v]][self.route_marker[u]] = baseLength
      elif r.celBodies[u].isMoon != True:
        self.routes[self.route_marker[u]][self.route_marker[v]] = self.routes[self.route_marker[u]][self.route_marker[self.celBodies[v].parent]]+self.routes[self.route_marker[v]][self.route_marker[self.celBodies[v].parent]]
        self.routes[self.route_marker[v]][self.route_marker[u]] = self.routes[self.route_marker[u]][self.route_marker[self.celBodies[v].parent]]
      elif r.celBodies[v].isMoon != True:
        self.routes[self.route_marker[v]][self.route_marker[u]] = self.routes[self.route_marker[v]][self.route_marker[self.celBodies[u].parent]]+self.routes[self.route_marker[u]][self.route_marker[self.celBodies[u].parent]]
        self.routes[self.route_marker[u]][self.route_marker[v]] = self.routes[self.route_marker[v]][self.route_marker[self.celBodies[u].parent]]
      else:
        self.routes[self.route_marker[v]][self.route_marker[u]] = self.routes[self.route_marker[v]][self.route_marker[self.celBodies[u].parent]]+self.routes[self.route_marker[u]][self.route_marker[self.celBodies[u].parent]]
        self.routes[self.route_marker[u]][self.route_marker[v]] = self.routes[self.route_marker[u]][self.route_marker[self.celBodies[v].parent]]+self.routes[self.route_marker[v]][self.route_marker[self.celBodies[v].parent]]
      return True
    else:
      return False
  #Delete from here
  def print_graph(self):
    topArray = []
    for v,i in self.route_marker.items():
      topArray.append(v)
    print('0000',end='')
    for k in range(len(topArray)):
      print(topArray[k].rjust(6,' ')+' ',end='')
    print(' ')
    for v, i in self.route_marker.items():
      print(v.rjust(4,' ')+' ', end='')
      for j in range(len(self.routes)):
        print(str(self.routes[i][j]).rjust(6,' ')+' ',end='')
      print(' ')
  #To here

#x = distance from Wormhole/Parent Planet to old celBody
#v = distance from Wormhole/Parent planet to new celBody
#z = distance from Wormhole/Parent planet to angle anchor celBody
#y = distance from old celBody to angle anchor celBody
#w = distance from new celBody to angle anchor celBody
def lenCal(x,v,z,y,w):
  try:
    xAng = math.acos((y**2+z**2-x**2)/(2*y*z))
    vAng = math.acos((w**2+z**2-v**2)/(2*w*z))
    qLen = math.sqrt(y**2+w**2-(2*y*w*math.cos(vAng+xAng)))
    return math.floor(qLen)
  except:
    #print(x,v,z,y,w)
    #print((y**2+z**2-x**2)/(2*y*z))
    #print((w**2+z**2-v**2)/(2*w*z))
    return 1
  
def parentDifTol(x,y):
  difference = abs(r.routes[r.route_marker[x]][r.route_marker[r.celBodies[x].parent]] - r.routes[r.route_marker[y]][r.route_marker[r.celBodies[y].parent]])
  total = r.routes[r.route_marker[x]][r.route_marker[r.celBodies[x].parent]] + r.routes[r.route_marker[y]][r.route_marker[r.celBodies[y].parent]]
  return (difference,total)
  
def uniBuilder(s = 2):
  planetCount = 0
  for i in range(0,s):
    sysNum = Vertex('WH'+str(i),'')
    r.addCelBody(sysNum)
  for sunRow in range(len(r.celBodies)):
    for sunCol in range(len(r.celBodies)):
      if r.routes[sunRow][sunCol] == 0 and sunRow != sunCol:
        r.addRoute('WH'+str(sunRow+1), 'WH'+str(sunCol+1),1)
  for suns in list(r.celBodies):
    initialPlanetCount = planetCount
    a = Vertex('Pl'+str(planetCount),str(suns))
    b = Vertex('Pl'+str(planetCount+1),str(suns))
    r.addCelBody(a)
    r.addCelBody(b)
    QTRoutes = [['Pl'+str(planetCount),str(suns)],['Pl'+str(planetCount+1),str(suns)]]
    for i in range(2):
      plVariation = randint(15000,57000)
      r.addRoute(QTRoutes[i][0],QTRoutes[i][1],plVariation)
    plVariation = randint((15000+parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount+1))[0]),parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount+1))[1])
    r.addRoute('Pl'+str(planetCount),'Pl'+str(planetCount+1),plVariation)
    planetCount += 2
    
    plNum = randint(1,2)
    for i in range(plNum):
      plVariation = randint(15000,57000)
      c = Vertex('Pl'+str(planetCount),str(suns))
      r.addCelBody(c)
      r.addRoute('Pl'+str(planetCount),str(suns),plVariation)
      plVariation = randint((15000+parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount-1))[0]),parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount-1))[1])
      r.addRoute('Pl'+str(planetCount),'Pl'+str(planetCount-1),plVariation)
      for j in range(initialPlanetCount, planetCount-1):
        if r.celBodies['Pl'+str(planetCount)].parent == r.celBodies['Pl'+str(j)].parent: 
          r.addRoute('Pl'+str(planetCount),'Pl'+str(j),lenCal(r.routes[r.route_marker['Pl'+str(j)]][r.route_marker[r.celBodies['Pl'+str(j)].parent]],
                                                              r.routes[r.route_marker['Pl'+str(planetCount)]][r.route_marker[r.celBodies['Pl'+str(planetCount)].parent]],
                                                              r.routes[r.route_marker['Pl'+str(planetCount-1)]][r.route_marker[r.celBodies['Pl'+str(planetCount-1)].parent]],
                                                              r.routes[r.route_marker['Pl'+str(j)]][r.route_marker['Pl'+str(planetCount-1)]],
                                                              r.routes[r.route_marker['Pl'+str(planetCount)]][r.route_marker['Pl'+str(planetCount-1)]]))       
      planetCount += 1
  for k in range(planetCount):
    for l in range(planetCount):
      if r.routes[r.route_marker['Pl'+str(k)]][r.route_marker['Pl'+str(l)]] == 0 and k != l:
        r.addRoute('Pl'+str(k),'Pl'+str(l),(r.routes[r.route_marker['Pl'+str(k)]][r.route_marker[r.celBodies['Pl'+str(k)].parent]]+r.routes[r.route_marker['Pl'+str(l)]][r.route_marker[r.celBodies['Pl'+str(l)].parent]]))

#########################
# ## ## #### #### ##  # #
# # # # #  # #  # # # # #
# #   # #### #### #  ## #
#########################

  moonCount = 0
  for planet in (planet for planet in list(r.celBodies) if r.celBodies[planet].parent != ''):
    initialMoonCount = moonCount
    m = Vertex('Mn'+str(moonCount),str(planet),True)
    n = Vertex('Mn'+str(moonCount+1),str(planet),True)
    r.addCelBody(m)
    r.addCelBody(n)
    QTRoutes = [['Mn'+str(moonCount),str(planet)],['Mn'+str(moonCount+1),str(planet)]]
    for i in range(2):
      mnVariation = randint(52,1914)
      r.addRoute(QTRoutes[i][0],QTRoutes[i][1],mnVariation)
    mnVariation = randint((52+parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount+1))[0]),parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount+1))[1])
    r.addRoute('Mn'+str(moonCount),'Mn'+str(moonCount+1),mnVariation)
    moonCount += 2
    
    mnNum = randint(1,2)
    for i in range(mnNum):
      mnVariation = randint(52,1914)
      o = Vertex('Mn'+str(moonCount),str(planet),True)
      r.addCelBody(o)
      r.addRoute('Mn'+str(moonCount),str(planet),mnVariation)
      mnVariation = randint((52+parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount-1))[0]),parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount-1))[1])
      r.addRoute('Mn'+str(moonCount),'Mn'+str(moonCount-1),mnVariation)
      for j in range(initialMoonCount, moonCount-1):
        if r.celBodies['Mn'+str(moonCount)].parent == r.celBodies['Mn'+str(j)].parent: 
          r.addRoute('Mn'+str(moonCount),'Mn'+str(j),lenCal(r.routes[r.route_marker['Mn'+str(j)]][r.route_marker[r.celBodies['Mn'+str(j)].parent]],
                                                              r.routes[r.route_marker['Mn'+str(moonCount)]][r.route_marker[r.celBodies['Mn'+str(moonCount)].parent]],
                                                              r.routes[r.route_marker['Mn'+str(moonCount-1)]][r.route_marker[r.celBodies['Mn'+str(moonCount-1)].parent]],
                                                              r.routes[r.route_marker['Mn'+str(j)]][r.route_marker['Mn'+str(moonCount-1)]],
                                                              r.routes[r.route_marker['Mn'+str(moonCount)]][r.route_marker['Mn'+str(moonCount-1)]]))       
      moonCount += 1
  for k in range(planetCount):
    for l in range(moonCount):
      if r.routes[r.route_marker['Pl'+str(k)]][r.route_marker['Mn'+str(l)]] == 0:
        r.addRoute('Pl'+str(k),'Mn'+str(l))
  for d in range(moonCount):
    for e in range(moonCount):
      if r.routes[r.route_marker['Mn'+str(d)]][r.route_marker['Mn'+str(e)]] == 0 and d != e:
        r.addRoute('Mn'+str(d),'Mn'+str(e),(r.routes[r.route_marker['Mn'+str(d)]][r.route_marker[r.celBodies['Mn'+str(d)].parent]]+r.routes[r.route_marker['Mn'+str(e)]][r.route_marker[r.celBodies['Mn'+str(e)].parent]]))
  key_list = r.route_marker.keys()
  key_list_as_array = []
  for items in key_list:
    key_list_as_array.append(items)
  route_marker_return = r.route_marker
  route_list = r.routes
  for i in list(r.route_marker):
    if i.startswith("WH"):
      del route_list[0]
      route_marker_return.pop(i)
      key_list_as_array.remove(i)
    else:
      route_marker_return[i] = route_marker_return[i]-s
      for k in range(0,s):
        route_list[route_marker_return[i]].pop(0)
  celBodies_return = r.celBodies
  for i in list(r.celBodies):
    if i.startswith("WH"):
      celBodies_return.pop(i)
  return (route_list, key_list_as_array, route_marker_return, celBodies_return)
  
r = RouteMapper()

#print(uniBuilder()[0])

#To show the routes the ugly way
#print(uniBuilder()[0])

#To show the routes the pretty way
#r.print_graph()