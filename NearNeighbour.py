# Nearest Neighbour takes the full route list as input
# Throughout the program are comments containing time complexities (as Big O notation) for a certain section or operation. 
  # These only occur when a section have a time complexity that isn't constant, as it is only these that will be taken into account when discussing run time.
  # When discussing time complexity, n = total number of nodes
def nearNeighbour(uRouteInput):
  uRoute = []
  # The input list is copied so changes to the list does not affect the global route list (which is also used by the other algorithms)
  for items in range(0,len(uRouteInput)): # O(n^2)
    uRoute.append(list(uRouteInput[items])) # O(n)
  finalRoute = [0]
  totalDistance = 0
  location = 0
  # For each row in the list, the available routes are sorted in increasing order. Then it goes through this new sorted list until a unvisited node is found
  # This node is added to the final route and the original position of this node is the new row
  for i in range(0,len(uRoute)): # O(n^3)
    uMarkerLookupKeys = list(range(len(uRouteInput))) # O(n)
    uRoute[location], uMarkerLookupKeys = [ list(tuple) for tuple in  zip(*sorted(zip(uRoute[location], uMarkerLookupKeys)))] # O(n) (O(n) for zip, O(n log n) for sort, O(n) for zip, O(n) for list)
    for k in uMarkerLookupKeys: # O(n^2)
      if k not in finalRoute: # O(n) (worst case when all elements except 1 is in finalRoute)
        totalDistance += uRoute[location][k]
        location = k
        finalRoute.append(k)
        break
  # O(n^2) + O(n) + O(n^3) = O(n^3)
  return (finalRoute, totalDistance)



