from random import seed
from random import randint

seed()
import math
### Nodes/Celestial bodies will for the most part be described as celBody(celBodies) (shortened from celestial bodies which is used as a blanket descriptor) ###

# The attributes of each celBody describing their type(sun, planet, moon), with a parent attribute used to calculate indirect routes.
class celBodyNode:
  def __init__(self, n, p, *m):
    self.name = n
    self.parent = p
    if not m:
      self.isMoon = False
    else:
      self.isMoon = True
# The RouteMapper object where everything that has to do with the vertices, routes, and handling of universe matrix is being handled
class RouteMapper:
  # celBodies is where all celestial body vertices are being stored in generation order
  celBodies = {}
  # routes is the route matrix that stores every route 
  routes = []
  # routeMarker stores the position of each routeMarker in the routes matrix (useful for finding the position of 'Mn0' for instance) 
  routeMarker = {}
  
  # Adds a celBody to the matrix
  def addCelBody(self,celBody):
    # First making sure the celBody has the correct attributes and that they don't already exist, then adds the celBody to the celBodies dictionary;
    # and then prepares new empty routes from the celBody to each pre-existing celBody. (No route can be of length 0 so non-existing ones are decribed this way)
    if isinstance(celBody,celBodyNode) and celBody.name not in self.celBodies:
      self.celBodies[celBody.name] = celBody
      for row in self.routes:
        row.append(0)
      self.routes.append([0]*(len(self.routes)+1))
      self.routeMarker[celBody.name] = len(self.routeMarker)
      return True
    else:
      return False
  # Adds a new route to the route matrix.
  def addRoute(self,u,v,baseLength = 30000):
    # First checks to see if both ends of the route are celBodies and then checks which relation the celBodies have
    if u in self.celBodies and v in self.celBodies:
      # If both celBodies are planets of the same star system, if one is a parent celBody of the other (Planet => Moon, Star => Planet), or if both celBodies are moons with the same parent
      if (r.celBodies[v].isMoon != True and r.celBodies[u].isMoon != True) or r.routeMarker[r.celBodies[u].parent] == r.routeMarker[v] or r.routeMarker[r.celBodies[u].parent] == r.routeMarker[r.celBodies[v].parent]:
        self.routes[self.routeMarker[u]][self.routeMarker[v]] = baseLength
        self.routes[self.routeMarker[v]][self.routeMarker[u]] = baseLength
      # If only one of the celBodies are a moon (but not within the same planet sector)
      elif r.celBodies[u].isMoon != True:
        self.routes[self.routeMarker[u]][self.routeMarker[v]] = self.routes[self.routeMarker[u]][self.routeMarker[self.celBodies[v].parent]]+self.routes[self.routeMarker[v]][self.routeMarker[self.celBodies[v].parent]]
        self.routes[self.routeMarker[v]][self.routeMarker[u]] = self.routes[self.routeMarker[u]][self.routeMarker[self.celBodies[v].parent]]
      elif r.celBodies[v].isMoon != True:
        self.routes[self.routeMarker[v]][self.routeMarker[u]] = self.routes[self.routeMarker[v]][self.routeMarker[self.celBodies[u].parent]]+self.routes[self.routeMarker[u]][self.routeMarker[self.celBodies[u].parent]]
        self.routes[self.routeMarker[u]][self.routeMarker[v]] = self.routes[self.routeMarker[v]][self.routeMarker[self.celBodies[u].parent]]
      # Or if both celBodies are moons but the different parents
      else:
        self.routes[self.routeMarker[v]][self.routeMarker[u]] = self.routes[self.routeMarker[v]][self.routeMarker[self.celBodies[u].parent]]+self.routes[self.routeMarker[u]][self.routeMarker[self.celBodies[u].parent]]
        self.routes[self.routeMarker[u]][self.routeMarker[v]] = self.routes[self.routeMarker[u]][self.routeMarker[self.celBodies[v].parent]]+self.routes[self.routeMarker[v]][self.routeMarker[self.celBodies[v].parent]]
      return True
    else:
      return False
# lenCal is used to correctly calculate the distance between existing celBodies and a newly added celBody for the 3rd celBody and up
  # (besides the previosly added celBody which serves as the angle anchor celBody)
#x = distance from Wormhole/Parent Planet to existing celBody
#v = distance from Wormhole/Parent planet to new celBody
#z = distance from Wormhole/Parent planet to angle anchor celBody
#y = distance from existing celBody to angle anchor celBody
#w = distance from new celBody to angle anchor celBody
def lenCal(x,v,z,y,w):
  try:
    xAng = math.acos((y**2+z**2-x**2)/(2*y*z))
    vAng = math.acos((w**2+z**2-v**2)/(2*w*z))
    qLen = math.sqrt(y**2+w**2-(2*y*w*math.cos(vAng+xAng)))
    return math.floor(qLen)
  except:
    return 1
# A way to both calculate the difference in distance between 2 celBodies and their parent celBody and the total of a route celBody1 => Parent => celBody2
# Makes some lines easier to read and functionally makes sure the random distance of the route celBody1 => celBody2 isn't longer than celBody1 => Parent => celBody2
def parentDifTol(x,y):
  difference = abs(r.routes[r.routeMarker[x]][r.routeMarker[r.celBodies[x].parent]] - r.routes[r.routeMarker[y]][r.routeMarker[r.celBodies[y].parent]])
  total = r.routes[r.routeMarker[x]][r.routeMarker[r.celBodies[x].parent]] + r.routes[r.routeMarker[y]][r.routeMarker[r.celBodies[y].parent]]
  return (difference,total)
# Builds the universe;
# First each star system is generated with only the star in place. 
# Since each star system is connected with wormholes near the center that takes the player's ship through at an instant, is their distance 1 in order to show a connection but making it almost insignificant.
# Then the 2 first planets are added to each sun and eachother with routes of a random distance whose range are based on the star maps made by the user LISCHE on the star citizen forums
def uniBuilder(s = 2):
  planetCount = 0
  # The stars/wormholes are added
  for i in range(0,s):
    sysNum = celBodyNode('WH'+str(i),'')
    r.addCelBody(sysNum)
  for sunRow in range(len(r.celBodies)):
    for sunCol in range(len(r.celBodies)):
      if r.routes[sunRow][sunCol] == 0 and sunRow != sunCol:
        r.addRoute('WH'+str(sunRow+1), 'WH'+str(sunCol+1),1)
  for suns in list(r.celBodies):
    initialPlanetCount = planetCount
    # 2 first planets for star system are added
    a = celBodyNode('Pl'+str(planetCount),str(suns))
    b = celBodyNode('Pl'+str(planetCount+1),str(suns))
    r.addCelBody(a)
    r.addCelBody(b)
    # With routes added between each planet and their star
    QTRoutes = [['Pl'+str(planetCount),str(suns)],['Pl'+str(planetCount+1),str(suns)]]
    for i in range(2):
      plVariation = randint(15000,57000)
      r.addRoute(QTRoutes[i][0],QTRoutes[i][1],plVariation)
    plVariation = randint((15000+parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount+1))[0]),parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount+1))[1])
    r.addRoute('Pl'+str(planetCount),'Pl'+str(planetCount+1),plVariation)
    planetCount += 2
    # 3 to 4 planets are added to each sun (4 being the amount of planets currently implemented and 3 being the amount rumored for the upcoming star system (As of May/2020)) 
    plNum = randint(1,2)
    for i in range(plNum):
      # The new planet first gets a route between it and its star, and between it and the previously added planet
      plVariation = randint(15000,57000)
      c = celBodyNode('Pl'+str(planetCount),str(suns))
      r.addCelBody(c)
      r.addRoute('Pl'+str(planetCount),str(suns),plVariation)
      plVariation = randint((15000+parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount-1))[0]),parentDifTol('Pl'+str(planetCount),'Pl'+str(planetCount-1))[1])
      r.addRoute('Pl'+str(planetCount),'Pl'+str(planetCount-1),plVariation)
      # A route between new planet and existing planets (minus the previously added planet) is calculated by first calculating the angle between each planet and an anchor planet
      # then calculating the distance using this angle
      for j in range(initialPlanetCount, planetCount-1):
        if r.celBodies['Pl'+str(planetCount)].parent == r.celBodies['Pl'+str(j)].parent: 
          r.addRoute('Pl'+str(planetCount),'Pl'+str(j),lenCal(r.routes[r.routeMarker['Pl'+str(j)]][r.routeMarker[r.celBodies['Pl'+str(j)].parent]],
                                                              r.routes[r.routeMarker['Pl'+str(planetCount)]][r.routeMarker[r.celBodies['Pl'+str(planetCount)].parent]],
                                                              r.routes[r.routeMarker['Pl'+str(planetCount-1)]][r.routeMarker[r.celBodies['Pl'+str(planetCount-1)].parent]],
                                                              r.routes[r.routeMarker['Pl'+str(j)]][r.routeMarker['Pl'+str(planetCount-1)]],
                                                              r.routes[r.routeMarker['Pl'+str(planetCount)]][r.routeMarker['Pl'+str(planetCount-1)]]))       
      planetCount += 1
  # After each route within each star system is calculated, is the distance between 2 planets in different star systems calculated as the route planet1 => star1 => star2 => planet2
  for k in range(planetCount):
    for l in range(planetCount):
      if r.routes[r.routeMarker['Pl'+str(k)]][r.routeMarker['Pl'+str(l)]] == 0 and k != l:
        r.addRoute('Pl'+str(k),'Pl'+str(l),(r.routes[r.routeMarker['Pl'+str(k)]][r.routeMarker[r.celBodies['Pl'+str(k)].parent]]+r.routes[r.routeMarker['Pl'+str(l)]][r.routeMarker[r.celBodies['Pl'+str(l)].parent]]))

#########################
# ## ## #### #### ##  # #
# # # # #  # #  # # # # #
# #   # #### #### #  ## #
#########################
  # For moons are the same logic used as for planets but with stars replaced with planets and planets replaced with moons
  moonCount = 0
  for planet in (planet for planet in list(r.celBodies) if r.celBodies[planet].parent != ''):
    initialMoonCount = moonCount
    # The first 2 moons are added to the planet
    m = celBodyNode('Mn'+str(moonCount),str(planet),True)
    n = celBodyNode('Mn'+str(moonCount+1),str(planet),True)
    r.addCelBody(m)
    r.addCelBody(n)
    # With routes added between each moon and the planet
    QTRoutes = [['Mn'+str(moonCount),str(planet)],['Mn'+str(moonCount+1),str(planet)]]
    for i in range(2):
      mnVariation = randint(52,1914)
      r.addRoute(QTRoutes[i][0],QTRoutes[i][1],mnVariation)
    mnVariation = randint((52+parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount+1))[0]),parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount+1))[1])
    r.addRoute('Mn'+str(moonCount),'Mn'+str(moonCount+1),mnVariation)
    moonCount += 2
    # 3 to 4 moons are added to each planet (numbers based on the range of moons currently implemented in the game)
    mnNum = randint(1,2)
    for i in range(mnNum):
      # The moon first gets a route between it and its parent planet and the previously added moon
      mnVariation = randint(52,1914)
      o = celBodyNode('Mn'+str(moonCount),str(planet),True)
      r.addCelBody(o)
      r.addRoute('Mn'+str(moonCount),str(planet),mnVariation)
      mnVariation = randint((52+parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount-1))[0]),parentDifTol('Mn'+str(moonCount),'Mn'+str(moonCount-1))[1])
      r.addRoute('Mn'+str(moonCount),'Mn'+str(moonCount-1),mnVariation)
      # A route between new moon and existing moons (minus the previously added moon) is calculated by first calculating the angle between each moon and an anchor moon
      # then calculating the distance using this angle
      for j in range(initialMoonCount, moonCount-1):
        if r.celBodies['Mn'+str(moonCount)].parent == r.celBodies['Mn'+str(j)].parent: 
          r.addRoute('Mn'+str(moonCount),'Mn'+str(j),lenCal(r.routes[r.routeMarker['Mn'+str(j)]][r.routeMarker[r.celBodies['Mn'+str(j)].parent]],
                                                              r.routes[r.routeMarker['Mn'+str(moonCount)]][r.routeMarker[r.celBodies['Mn'+str(moonCount)].parent]],
                                                              r.routes[r.routeMarker['Mn'+str(moonCount-1)]][r.routeMarker[r.celBodies['Mn'+str(moonCount-1)].parent]],
                                                              r.routes[r.routeMarker['Mn'+str(j)]][r.routeMarker['Mn'+str(moonCount-1)]],
                                                              r.routes[r.routeMarker['Mn'+str(moonCount)]][r.routeMarker['Mn'+str(moonCount-1)]]))       
      moonCount += 1
  # After each route within each planet sector is calculated, is the distance between a moon and a planet from different sectors calculated
  # and 2 moons in different sectors calculated as the route moon1 => planet2 => moon2
  for k in range(planetCount):
    for l in range(moonCount):
      if r.routes[r.routeMarker['Pl'+str(k)]][r.routeMarker['Mn'+str(l)]] == 0:
        r.addRoute('Pl'+str(k),'Mn'+str(l))
  for d in range(moonCount):
    for e in range(moonCount):
      if r.routes[r.routeMarker['Mn'+str(d)]][r.routeMarker['Mn'+str(e)]] == 0 and d != e:
        r.addRoute('Mn'+str(d),'Mn'+str(e),(r.routes[r.routeMarker['Mn'+str(d)]][r.routeMarker[r.celBodies['Mn'+str(d)].parent]]+r.routes[r.routeMarker['Mn'+str(e)]][r.routeMarker[r.celBodies['Mn'+str(e)].parent]]))
  # Last are the stars are removed from every list/dictionary since they are not needed for the algorithms to work
  # and remaining of each list/dictionary is returned to be used by the algorithms
  routeMarkerReturn = r.routeMarker
  routeList = r.routes
  for i in list(r.routeMarker):
    if i.startswith("WH"):
      del routeList[0]
      routeMarkerReturn.pop(i)
    else:
      routeMarkerReturn[i] = routeMarkerReturn[i]-s
      for k in range(0,s):
        routeList[routeMarkerReturn[i]].pop(0)
  celBodiesReturn = r.celBodies
  for i in list(r.celBodies):
    if i.startswith("WH"):
      celBodiesReturn.pop(i)
  return (routeList, routeMarkerReturn, celBodiesReturn)
  
r = RouteMapper()