import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijc2OTVkNWM0MWExZjRiZjliODQxMDRlYzliZDZmNmNlIiwiaCI6Im11cm11cjY0In0="
url = "https://api.openrouteservice.org/v2/directions/driving-car"
headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
body = {"coordinates": [[78.4867, 17.3850], [78.4900, 17.3900]], "geometry_format": "geojson"}

try:
    response = requests.post(url, json=body, headers=headers)
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(e)
