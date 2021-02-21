# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 21:27:05 2020

@author: shruti
"""

from bs4 import BeautifulSoup
import requests
import json
base_url="https://www.amazon.com/"

def repalceAllBadCharacter(testString):
            badChars=['\n','\t','\r',',']
            testString = ''.join(i for i in testString if not i in badChars)
            return testString

input_data = input("Enter the product name you would like to search.")

def amazon_url_of_search_input(search_input):
    search_value_list=[value for value in search_input.split(" ")]
    search_data=''
    for search_value in range(0,len(search_value_list)):
        if(search_value==0):
            search_data=search_data+search_value_list[search_value]
        else:
            search_data=search_data+"+"+search_value_list[search_value]
    return base_url+"s?k="+search_data
parent_url= amazon_url_of_search_input(input_data)  
#print(parent_url) 

def find_no_of_pages(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    r = r.text
    soup=BeautifulSoup(r,"lxml")
    soup.prettify()
    pages=soup.find("ul",attrs={'class':'a-pagination'})
    if(pages!=None):
        no_of_pages = pages.select(".a-disabled")
        if(len(no_of_pages)>1):
            no_of_pages=no_of_pages[-1].get_text()
            no_of_pages=int(no_of_pages)
        else:
            no_of_pages=no_of_pages.get_text()
            no_of_pages=int(no_of_pages)
        #print(no_of_pages)
    else:
        no_of_pages=0
    return no_of_pages
no_of_pages=find_no_of_pages(parent_url)
#print(no_of_pages)

def get_data(pageNo):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
    url=amazon_url_of_search_input(input_data)+'&page='+str(pageNo)+'&qid=1597315874&ref=sr_pg_'+str(pageNo)
    url=str(url)
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    r = r.text
    soup=BeautifulSoup(r,"lxml")
    soup.prettify()
    result={}
    result['product_details']= []
    #name= soup.find("h2",attrs={'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})
    search_page_data= soup.find("div",attrs={'class':'s-main-slot s-result-list s-search-results sg-row'})
    #print(search_page_data)
    data={}

    if(search_page_data!=None):
        for search_page_data_main_category_item in search_page_data.find_all('div',attrs={'class':'a-section a-spacing-medium'}):
            search_data_main_category_item_img = search_page_data_main_category_item.find('img')
            if(search_data_main_category_item_img!=None):
                search_data_main_category_item_img = search_data_main_category_item_img.get('src')
                data['img']= search_data_main_category_item_img
            else:
                search_data_main_category_item_img= None
            #print(search_data_main_category_item_img)
            search_data_main_category_item_url = search_page_data_main_category_item.find('a')
            if search_data_main_category_item_url.has_attr('href'):
                search_data_main_category_item_url= base_url+search_data_main_category_item_url['href']
                #print(search_data_main_category_item_url)
                data['url']= search_data_main_category_item_url
            else:
                search_data_main_category_item_url=None
            search_data_main_category_item_title= search_page_data_main_category_item.find('img',alt=True)
            if(search_data_main_category_item_title!=None):
                search_data_main_category_item_title= search_data_main_category_item_title['alt']
                data['title']= search_data_main_category_item_title
            else:
                search_data_main_category_item_title=search_page_data_main_category_item.find('span',class_='a-size-medium a-color-base a-text-normal')
                if(search_data_main_category_item_title!= None):
                    search_data_main_category_item_title= search_data_main_category_item_title.get_text()
                    data['title']= search_data_main_category_item_title
                else:
                    search_data_main_category_item_title= None
                    
            #print(search_data_main_category_item_title)
            search_data_main_category_item_price= search_page_data_main_category_item.find('span',class_="a-price")
            if(search_data_main_category_item_price!=None):
                search_data_main_category_item_price= search_data_main_category_item_price.find('span',class_="a-offscreen").get_text()
                data['price']= search_data_main_category_item_price
            else:
                search_data_main_category_item_price= None
            #print(search_data_main_category_item_price)
            search_data_main_category_item_extra_availability_info= search_page_data_main_category_item.find('div',class_='a-row a-size-base a-color-secondary')
            if(search_data_main_category_item_extra_availability_info!=None):
                search_data_main_category_item_extra_availability_info= search_data_main_category_item_extra_availability_info.find('span')
                if(search_data_main_category_item_extra_availability_info.has_attr('aria-label')):
                    search_data_main_category_item_extra_availability_info= search_data_main_category_item_extra_availability_info['aria-label']
                    data['availability_info']= search_data_main_category_item_extra_availability_info
                else:
                    search_data_main_category_item_extra_availability_info= None
            else:
                search_data_main_category_item_extra_availability_info= None
            #print(search_data_main_category_item_extra_availability_info)
            
            search_data_main_category_item_rating_and_review= search_page_data_main_category_item.find(class_="a-section a-spacing-none a-spacing-top-micro")
            if(search_data_main_category_item_rating_and_review!=None):
                search_data_main_category_item_rating= search_data_main_category_item_rating_and_review.find('span',attrs={'aria-label':"4.4 out of 5 stars"})
                #print(search_data_main_category_item_rating)
                if(search_data_main_category_item_rating!= None):
                    search_data_main_category_item_rating= search_data_main_category_item_rating.find('span',attrs={'class':"a-icon-alt"}).get_text()
                    search_data_main_category_item_ratings=[]
                    search_data_main_category_item_ratings=search_data_main_category_item_rating.split(" ")
                    search_data_main_category_item_rating= float(search_data_main_category_item_ratings[0])
                    data['rating']= search_data_main_category_item_rating
                    #print(search_data_main_category_item_rating)
                else:
                    search_data_main_category_item_rating= 0.0
                search_data_main_category_item_no_of_review = search_data_main_category_item_rating_and_review.find("span",attrs={'class':"a-size-base"})
                #print(search_data_main_category_item_rating)
                if(search_data_main_category_item_no_of_review!=None):
                    search_data_main_category_item_no_of_review=search_data_main_category_item_no_of_review.get_text()
                    #search_data_main_category_item_no_of_reviews=[]
                    #search_data_main_category_item_no_of_reviews= search_data_main_category_item_no_of_review.split(" ")
                    #search_data_main_category_item_no_of_review = search_data_main_category_item_no_of_reviews[0]
                    search_data_main_category_item_no_of_review= int(repalceAllBadCharacter(search_data_main_category_item_no_of_review))
                    #print(search_data_main_category_item_no_of_review)
                    data['no_of_review']= search_data_main_category_item_no_of_review
                else:
                    search_data_main_category_item_no_of_review=0
            else:
                search_data_main_category_item_rating= 0.0
                search_data_main_category_item_no_of_review= 0
            result['product_details'].append(data)
    return result 
            
                
        
        
                
    #title=soup.find_all('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
    #print(title)
output={}
output['page_wise_product_details']=[]
for item in range(1,no_of_pages+1):
    output['page_wise_product_details'].append(get_data(item))
with open('out.json','w') as f:
    json.dump(output,f)
f.close()

    


        
