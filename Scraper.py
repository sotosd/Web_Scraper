from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

#excel fine name
filename = "restaurants.csv"

#open file with write restriction
f = open(filename, "w")

#prepare columns' headers
headers = "Restaurant_Name,Cuisine,Price,Rating\n"

#write headers into file
f.write(headers)

#my_url='https://www.tripadvisor.com/Restaurants-g189415-Chania_Town_Chania_Prefecture_Crete.html'
my_url='https://www.tripadvisor.com/Restaurants-g189415-oa00-Chania_Town_Chania_Prefecture_Crete.html#EATERY_LIST_CONTENTS'

while True: 
	#open my_url and store it to a variable (like "downloading" the web page)
	uClient = uReq(my_url)

	#read the web page and store its data to a variable
	page_html = uClient.read()

	#I am done with the open connection to internet so the connection should be closed
	#Closing the connection
	uClient.close()

	#parsing the web page using beautiful soup as html parser, and store it to a variable
	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grab all restaurants' listings
	listings = page_soup.findAll("div", {'class': lambda x: x and 'listing' in x.split()})

	#loop extracting name,cuisine,price and rating for each reasturant
	for listing in listings:
		#find and store restaurant's name
		name=listing.find('div',{'class':'ui_columns'}).div.div.a
		restaurant_name = name.text.strip('\n')

		#create an array for keeping different types of restaurant's cuisine
		cuisine=[]

		#find all types od cuisines adn store them
		item_cuisine = listing.findAll('a',{'class':'item cuisine'})
		for i in range(len(item_cuisine)):
			cuisine.append(item_cuisine[i].text.strip('Options'))

		try:
			#find and store restaurant's price tag
			price = listing.find('span',{'class':'item price'}).text
		except:
			price = '-'
		
		try:
			#find and stor restaurant's rating
			rating = listing.find('div',{'class':'rating rebrand'}).span['alt']
		except:
			rating = '-'

		#print in console
		print ("Name : "+restaurant_name)
		print ("Cuisine : " +','.join(cuisine))
		print ("Price : "+price )
		print ("Rating : "+rating)
		print ("")

		#write extracted data into file
		f.write(restaurant_name.replace(",", "-")+","+ ' | '.join(cuisine) +","+price+","+rating +"\n" )
	try:	
		#find the next page in order to get its url and extract its data
		link = page_soup.find(attrs={"class":"nav next rndBtn ui_button primary taLnk"});	
		_link=link.get('href');

		my_url='https://www.tripadvisor.com'+_link;
	except:
		break;	

#close file
f.close()


