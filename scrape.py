# Web Scraping IMRA Website
# From Medium & Towards Data Science Web Scraping Tutorials 
# https://medium.com/@kaustumbhjaiswal7/learn-woeb-scraping-using-python-in-under-5-minutes-36a7d4d6e1e7
# https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd

url = "https://www.imra.ie/events/"
page = requests.get(url, verify=False)					# ignore verifying the SSL certficate (verify=False)
doc = lh.fromstring(page.content)					# Store the contents of the website under doc using lxml

soup = BeautifulSoup(page.text, 'html.parser')				# BeautifulSoup used to view page html code
table = soup.find(class_="listing table")				# Selecting IMRA events table html code 


tr_elements = doc.xpath('//tr')						# Parse data that are stored between <tr>..</tr> of HTML (table data)

# Parse Table Header
col=[]									# table header row / column names 
i=0
for t in tr_elements[0]:
	i+=1
	name=t.text_content()
#	print('%d:%s' %(i, name))
	col.append((name,[]))

# creating pandas dataframe
for j in range(1,len(tr_elements)):
	T=tr_elements[j]						# T is our j'th row
	if len(T)!=8:							# If row is not of size 8, the //tr data is not from our table 
		break
	i=0								# i is the index of our column
	for t in T.iterchildren():					# Iterate through each element of the row
		data=t.text_content() 
		if i>0:							# Check if row is empty
			try:						# Convert any numerical value to integers
                		data=int(data)
			except:
				pass
		col[i][1].append(data)					# Append the data to the empty list of the i'th column 
		i+=1							# Increment i for the next column

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

df['Climb'] = df['Climb'].str.replace(r'\D','').astype(int)		# removing meters (m) and updating to intergers
df['Dist.'] = df['Dist.'].str.replace(r'\D','').astype(int)		# removing kilometers (km) and updating to intergers


df.to_csv('IMRA_Events.csv')





