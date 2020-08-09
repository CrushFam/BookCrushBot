from datetime import date
import requests
import xml.etree.ElementTree as ET
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/14KPDYzQFJnRyZkZpA-DMxdPYU74wovyb0l1dHceTgpg/edit#gid=0')
sheet = sh.get_worksheet(0)
api =  "KJNH0y47MJOPEDtEIBGlow" #Goodreads api

user = input("\nEnter the name under which you wanna input: ")
while True:
	g_id = input("\nEnter Goodreads id of your book: ")
	genre = input("\nEnter it's genre seperated by comma: ")
	url = "https://www.goodreads.com/book/show?id="+g_id+"&format=xml&key="+api
	r = requests.get(url)
	root = ET.fromstring(r.content)
	data = {}
	data['authors'] = ""
	data['rating'] = root.find('./book/average_rating').text
	data['publisher'] = root.find('./book/publisher').text
	data['pages'] = root.find('./book/num_pages').text
	authors = root.find('./book/authors')
	for author in authors.findall('author'):
		data['authors']+= author.find('name').text + ", "
	try:
		data['year'] = root.find('./book/work/original_publication_year').text
		data['title'] = root.find('./book/work/original_title').text
		if data['title'] == None:
			raise TypeError
	except:
		data['year'] = root.find('./book/publication_year').text
		data['title'] = root.find('./book/title').text

	today = date.today()
	today = today.strftime("%d/%m/%Y")

	row = ['',data['title'],data['authors'],genre,'',data['rating'],data['publisher'],data['pages'],data['year'],today,'',user]
	index = len(sheet.get_all_values())+1
	sheet.insert_row(row,index=index,value_input_option='USER_ENTERED')
	print("--------------------------------------------------------------------------------------")
	print("Added",data['title'],"by",data['authors'],"to the roulette")
	print("\n ___Press Ctrl+C to Exit___\n")




