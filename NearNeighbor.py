### Takes UniverseBuilder[0],[1] as input ###
def nearNeighbour(uRoute, freshRouteKeys):
  unvisited = dict(freshRouteKeys)
  unvisited.pop("Pl0")
  finalRoute = ["Pl0"]
  totalDistance = 0
  location = 0
  for i in range(0,len(uRoute)):
    uMarkerLookupKeys = dict(freshRouteKeys)
    uRoute[location], uMarkerLookupKeys = [ list(tuple) for tuple in  zip(*sorted(zip(uRoute[location], uMarkerLookupKeys)))]
    for k in uMarkerLookupKeys:
      if k in unvisited:
        totalDistance += uRoute[location][freshRouteKeys[k]]
        location = freshRouteKeys[k]
        finalRoute.append(k)
        unvisited.pop(k)
        break
  #Distance from last planet directly to "Pl0"
  #totalDistance += uRoute[location][0]
  return (finalRoute, totalDistance)



