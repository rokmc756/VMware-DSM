import json
s = '''
{
   "listingReducer":{
      "selectedListing":{
         "id":2234588,
         "has_video":0,
         "refresh":1625551240,
         "category":6,
         "ketchen":1,
         "lift":1,
         "livings":1,
         "maid":null,
         "meter_price":null,
         "playground":null,
         "location":{
            "lat":26.378031,
            "lng":50.124866
         },
         "views":6075
      }
   }
}
'''

d = json.loads(s)
print(f"ID: {d['listingReducer']['selectedListing']['id']}")
print(f"all: {d['listingReducer']}")
