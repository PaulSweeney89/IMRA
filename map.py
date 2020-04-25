# Plotting map of IMRA Events

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv("IMRA_Events.csv")
df2 = pd.read_csv("County Coordinates.csv")

# append events df1 dataframe with county coordinates 

df1['Lat'] = df1['County'].map(df2.set_index('CountyName')['Lat'])
df1['Long'] = df1['County'].map(df2.set_index('CountyName')['Long'])

# New data frame with number of events per County

df3 = df1['County'].value_counts().rename_axis('County').reset_index(name='Number')
df3['Lat'] = df3['County'].map(df2.set_index('CountyName')['Lat'])
df3['Long'] = df3['County'].map(df2.set_index('CountyName')['Long'])
print(df3)

# Basemap Plot

Long = df3['Long'].values
Lat = df3['Lat'].values
County = df3['County']
Events = df3['Number']

fig, ax = plt.subplots()
map = Basemap(projection='merc',
    resolution = 'i', area_thresh = 0.05,
    llcrnrlon=-10.59, llcrnrlat=51.27,
    urcrnrlon=-5.33, urcrnrlat=55.45)
map.drawcoastlines(linewidth = 0.2, zorder = 0)
map.drawmapboundary(fill_color='lightblue') 
map.fillcontinents(color='tan', lake_color='lightblue')
map.drawcountries()
map.drawrivers(linewidth=0.5, linestyle='solid', color='lightblue')

fig.suptitle("IMRA EVENTS")

xpt,ypt = map(Long, Lat)

for x, y, e in zip(xpt,ypt, Events):
    # markersize is scale down by /125
    map.plot(x, y, 'ro', markersize=2)
    plt.text(x, y, e, fontsize=7, verticalalignment='bottom', horizontalalignment='center', fontweight='bold')

for w, z, c in zip(xpt,ypt, County):
    plt.text(w, z, c, fontsize=7, verticalalignment='top', horizontalalignment='center')

plt.show()
		
