import folium
import requests

# Fetch earthquake data from USGS API
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
response = requests.get(url)
earthquake_data = response.json()

# Create a map centered on the US
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Function to determine marker color based on depth
def get_color(depth):
    if depth < 10:
        return 'lightgreen'
    elif depth < 30:
        return 'yellow'
    elif depth < 50:
        return 'orange'
    else:
        return 'red'

# Add earthquake markers to the map
for feature in earthquake_data['features']:
    coords = feature['geometry']['coordinates']
    magnitude = feature['properties']['mag']
    depth = coords[2]
    location = [coords[1], coords[0]]
    
    folium.CircleMarker(
        location=location,
        radius=magnitude * 2,
        popup=f"Magnitude: {magnitude}<br>Depth: {depth} km",
        color=get_color(depth),
        fill=True,
        fillColor=get_color(depth),
        fillOpacity=0.7
    ).add_to(m)

# Add a legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 220px; height: 120px; 
    border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
    ">&nbsp; <b>Earthquake Depth (km)</b> <br>
    &nbsp; <i class="fa fa-circle" style="color:lightgreen"></i> &lt; 10 <br>
    &nbsp; <i class="fa fa-circle" style="color:yellow"></i> 10-30 <br>
     &nbsp; <i class="fa fa-circle" style="color:orange"></i> 30-50 <br>
    &nbsp; <i class="fa fa-circle" style="color:red"></i> &gt; 50
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map
m.save("earthquake_map.html")

print("Earthquake map has been created and saved as 'earthquake_map.html'")
print(f"Number of earthquakes plotted: {len(earthquake_data['features'])}")