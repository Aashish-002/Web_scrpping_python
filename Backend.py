from flask import Flask, render_template
import pandas as pd
import requests
import pandas as pd
import bs4
import json
import numpy
import matplotlib
import matplotlib.pyplot as plt
from fake_headers import Headers
import threading
import os
from wordcloud import WordCloud,STOPWORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
matplotlib.use('agg')
def Search(x):
    Data=[]
    t1=threading.Thread(target=flipkartSearch,args=(x,Data,))
    t2=threading.Thread(target=amazonSearch,args=(x,Data,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # product_name=x
    # for i in range(1,3):
    #     url1 = "https://www.flipkart.com/search?q={0}&page={1}"
    #     url1 = url1.format(product_name,i)
    #     url2 = "https://www.amazon.in/s?k={0}&page={1}"
    #     url2=url2.format(product_name,i)
    #     ## getting the reponse from the page using get method of requests module
    #     page1 = requests.get(url1, headers=Headers(os='win',browser='chrome',headers=True).generate())
    #     page2 = requests.get(url2, headers=Headers(os='win',browser='chrome',headers=True).generate())

    #     ## storing the content of the page in a variable
    #     html1 = page1.content
    #     html2 = page2.content
    #     ## creating BeautifulSoup object
    #     page_soup1 = bs4.BeautifulSoup(html1, "html.parser")
    #     page_soup2 = bs4.BeautifulSoup(html2,"html.parser")
    #     l=0
    #     l1=len(page_soup1.findAll('div',class_='_13oc-S'))
    #     l2=len(page_soup2.findAll('div', attrs={'data-component-type': 's-search-result'}))
    #     if(l1>l2):
    #         l=l1
    #     else:
    #         l=l2
    #     flipkart=page_soup1.findAll('div',class_='_13oc-S')
    #     amazon=page_soup2.findAll('div', attrs={'data-component-type': 's-search-result'})
    #     for count in range(l):
    #         if(count<l1):
    #             d={}
    #             ft=flipkart[count]
    #             n=ft.find('a', attrs={'class':'IRpwTa'})
    #             p=ft.find('div', attrs={'class':'_30jeq3'})
    #             # rating=containers.find('div', attrs={'class':'hGSR34'})
    #             # specification = containers.find('div', {'class':'_1rcHFq'})
    #             l=ft.find('a',class_='_2UzuFa')
    #             i=ft.find('img',class_='_2r_T1I')
    #             b=ft.find('div',attrs={'class':'_2WkVRV'})
    #             if(n!=None and p!=None and b!=None and i!=None and l!=None):
    #                 d["Name"]=n.text
    #                 d["Price"]=p.text
    #                 d["Brand"]=b.text
    #                 d["Image"]=i.get('src')
    #                 d["ProductLink"]="https://www.flipkart.com"+l.get('href')
    #                 url1=d['ProductLink']
    #                 page1= requests.get(url1, headers=Headers(os='win',browser='chrome',headers=True).generate())
    #                 page1_soup=bs4.BeautifulSoup(page1.content,"html.parser")
    #                 r=page1_soup.find('div',class_='_3LWZlK _3uSWvT')
    #                 if(r==None):
    #                     d["Rating"]="Nill"
    #                 else:
    #                     d["Rating"]=r.text
    #                 d["FA"]="Flipkart"
    #                 Data.append(d)
    #         if(count<l2):
    #             d={}
    #             at=amazon[count]
    #             b=at.find('span', attrs={'class':'a-size-base-plus a-color-base'})
    #             p=at.find('span', attrs={'class':'a-price-whole'})
    #             rating=at.find('span', attrs={'class':'a-icon-alt'})
    #             # specification = containers.find('div', {'class':'_1rcHFq'})
    #             i=at.find('img',class_='s-image')
    #             n=at.find('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
    #             l=at.find('a',class_='a-link-normal s-no-outline')
    #             if(n!=None and p!=None and b!=None and i!=None and l!=None):
    #                 d['Name']=n.text
    #                 d['Price']="₹"+p.text
    #                 d['Brand']=b.text
    #                 d['Image']=i.get('src')
    #                 # ratings.append(rating.text)
    #                 d['ProductLink']='https://amazon.in/'+l.get('href')
    #                 if(rating==None):
    #                     d["Rating"]="Nill"
    #                 else:
    #                     nr=(rating.text).split(" ")
    #                     d["Rating"]=nr[0]
    #                 d['FA']="Amazon"
    #                 Data.append(d)
   
    # # Save the dataframe to a CSV file
    # csv_filename = "products.json"
    # df.to_json(csv_filename, index=False)
    with open("Data.json","w") as f:
        json.dump(Data,f)
# search(input("Enetr product: "))
# with open("Data.json","w") as f:
#     json.dump(Data,f)

def amazonSearch(x,Data):
    for i in range(1,3):
        url = "https://www.amazon.in/s?k={0}&page={1}"
        url=url.format(x,i)
        page = requests.get(url, headers=Headers(os='win',browser='chrome',headers=True).generate())
        html = page.content
        page_soup = bs4.BeautifulSoup(html,"html.parser")
        amazon=page_soup.findAll('div', attrs={'data-component-type': 's-search-result'})
        for div in amazon:
            d={}
            b=div.find('span', attrs={'class':'a-size-base-plus a-color-base'})
            p=div.find('span', attrs={'class':'a-price-whole'})
            rating=div.find('span', attrs={'class':'a-icon-alt'})
                        # specification = containers.find('div', {'class':'_1rcHFq'})
            i=div.find('img',class_='s-image')
            n=div.find('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
            l=div.find('a',class_='a-link-normal s-no-outline')
            if(n!=None and p!=None and b!=None and i!=None and l!=None):
                d['Name']=n.text
                d['Price']="₹"+p.text
                d['Brand']=b.text
                d['Image']=i.get('src')
                # ratings.append(rating.text)
                d['ProductLink']='https://amazon.in/'+l.get('href')
                if(rating==None):
                    d["Rating"]=0.0
                else:
                    nr=(rating.text).split(" ")
                    d["Rating"]=float(nr[0])
                    d['FA']="Amazon"
                    Data.append(d)
                d['ID']=div['data-asin']

def flipkartSearch(x,Data):
    for i in range(1,3):
        url = "https://www.flipkart.com/search?q={0}&page={1}"
        url = url.format(x,i)
        page = requests.get(url, headers=Headers(os='win',browser='chrome',headers=True).generate())
        html = page.content
        page_soup = bs4.BeautifulSoup(html, "html.parser")
        flipkart=page_soup.findAll('div',class_='_13oc-S')
        for div in flipkart:
            d={}
            n=div.find('a', attrs={'class':'IRpwTa'})
            p=div.find('div', attrs={'class':'_30jeq3'})
                # rating=containers.find('div', attrs={'class':'hGSR34'})
                # specification = containers.find('div', {'class':'_1rcHFq'})
            l=div.find('a',class_='_2UzuFa')
            i=div.find('img',class_='_2r_T1I')
            b=div.find('div',attrs={'class':'_2WkVRV'})
            if(n!=None and p!=None and b!=None and i!=None and l!=None):
                d["Name"]=n.text
                d["Price"]=p.text
                d["Brand"]=b.text
                d["Image"]=i.get('src')
                d["ProductLink"]="https://www.flipkart.com"+l.get('href')
                url1=d['ProductLink']
                page1= requests.get(url1, headers=Headers(os='win',browser='chrome',headers=True).generate())
                page1_soup=bs4.BeautifulSoup(page1.content,"html.parser")
                r=page1_soup.find('div',class_='_3LWZlK _3uSWvT')
                if(r==None):
                    d["Rating"]=0.0
                else:
                    d["Rating"]=float(r.text)
                d["FA"]="Flipkart"
                id=div.find('div')
                d["ID"]=id['data-id']
                Data.append(d)       

def Analyse():
    f=open("Data.json","r+")
    df=pd.read_json(f)
    folder="static/Page"
    for files in os.listdir(folder):
        fp=os.path.join(folder,files)
        if(os.path.exists(fp)):
            os.remove(fp)
    # fp="static/Page/Rate.png"
    # if(os.path.exists(fp)):
    #     os.remove(fp)
    plt.clf()
    df["Brand"].value_counts().plot.pie(autopct='%1.1f%%',startangle=90)
    plt.savefig("static/Page/Plot.png")
    plt.clf()
    df.groupby("Brand")["Rating"].sum().plot.bar()
    plt.savefig("static/Page/Rate.png")
    plt.clf()
    #     print("yes")
# analyse()

def amazonReviewAnalyse(ASIN):
    url1="https://www.amazon.in/product-reviews/"+ASIN+"?pageNumber=1&filterByStar=positive"
    url2="https://www.amazon.in/product-reviews/"+ASIN+"?pageNumber=1&filterByStar=critical"
    postive=requests.get(url1, headers=Headers(os='win',browser='chrome',headers=True).generate())
    critical=requests.get(url2, headers=Headers(os='win',browser='chrome',headers=True).generate())
    page_soup1=bs4.BeautifulSoup(postive.content,"html.parser")
    page_soup2=bs4.BeautifulSoup(critical.content,"html.parser")
    # p1=page_soup1.findAll('div',attrs={'data-hook':'review'})
    # p2=page_soup2.findAll('div',attrs={'data-hook':'review'})
    Words=""
    Positive=""
    Negative=""
    for i in page_soup1.findAll('div',attrs={'data-hook':'review'}):
        review=i.find('span',attrs={'data-hook':'review-body'})
        if(review!=None):
            Words+=review.text
            Positive+=review.text
    for i in page_soup2.findAll('div',attrs={'data-hook':'review'}):
        review=i.find('span',attrs={'data-hook':'review-body'})
        if(review!=None):
            Words+=review.text
            Negative+=review.text
    # print(Words)
    Positive=Positive.strip().split("\n")
    Negative=Negative.strip().split("\n")
    Sentiment=sentiment_scores(Words)
    if Sentiment['compound'] >= 0.05 :
        Overall="Positive"

    elif Sentiment['compound'] <= - 0.05 :
        Overall="Negative"
    d=sentiment_scores(Words)
    plt.clf()
    sizes=[Sentiment['pos'],Sentiment['neg'],Sentiment['neu']]
    labels = ['Positive', 'Negative', 'Neutral']
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.1, 0, 0)  
    fig1, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle
    # ax1.axis('equal')  
    plt.tight_layout()
    fp="static/Product/Reviewplot.png"
    if(os.path.exists(fp)):
        os.remove(fp)
    plt.savefig("static/Product/Reviewplot.png")
    #Word Cloud
    w=WordCloud(width=800,height=400).generate(Words)
    fp="static/Product/WordCloud.png"
    if(os.path.exists(fp)):
        os.remove(fp)
    w.to_file("static/Product/WordCloud.png")
    Comments=[Positive[0],Negative[0],Overall]
    return Comments

def flipkartReviewAnalyse(FSN):
    url1="https://www.flipkart.com/product/product-reviews/itme=?pid="+FSN+"&sortOrder=POSITIVE_FIRST"+"&page=1"
    url2="https://www.flipkart.com/product/product-reviews/itme=?pid="+FSN+"&sortOrder=NEGATIVE_FIRST"+"&page=1"
    postive=requests.get(url1, headers=Headers(os='win',browser='chrome',headers=True).generate())
    critical=requests.get(url2, headers=Headers(os='win',browser='chrome',headers=True).generate())
    page_soup1=bs4.BeautifulSoup(postive.content,"html.parser")
    page_soup2=bs4.BeautifulSoup(critical.content,"html.parser")
    Words=""
    Positive=""
    Negative=""
    for i in page_soup1.findAll('div',class_="_1AtVbE col-12-12"):
        review=i.find('div',class_='_6K-7Co')
        if(review!=None):
            Words+=review.text
            Positive+=review.text
        # print(review)
    for i in page_soup2.findAll('div',class_="_1AtVbE col-12-12"):
        review=i.find('div',class_='_6K-7Co')
        if(review!=None):
            Words+=review.text
            Negative+=review.text
    # print(Words)
    Positive=Positive.strip().split("\n")
    Negative=Negative.strip().split("\n")
    Sentiment=sentiment_scores(Words)
    if Sentiment['compound'] >= 0.05 :
        Overall="Positive"

    elif Sentiment['compound'] <= - 0.05 :
        Overall="Negative"
    plt.clf()
    sizes=[Sentiment['pos'],Sentiment['neg'],Sentiment['neu']]
    # Pie chart
    labels = ['Positive', 'Negative', 'Neutral']
    explode = (0.1, 0, 0)  
    fig1, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')  
    plt.tight_layout()
    fp="static/Product/Reviewplot.png"
    if(os.path.exists(fp)):
        os.remove(fp)
    plt.savefig("static/Product/Reviewplot.png")
    #Word Cloud
    w=WordCloud(width=800,height=400).generate(Words)
    fp="static/Product/WordCloud.png"
    if(os.path.exists(fp)):
        os.remove(fp)
    w.to_file("static/Product/WordCloud.png")
    Comments=[Positive[0],Negative[0],Overall]
    return Comments

def sentiment_scores(sentence):

	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# polarity_scores method of SentimentIntensityAnalyzer
	# object gives a sentiment dictionary.
	# which contains pos, neg, neu, and compound scores.
	sentiment_dict = sid_obj.polarity_scores(sentence)
	return sentiment_dict
	# print("Overall sentiment dictionary is : ", sentiment_dict)
	# print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
	# print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
	# print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

	# print("Sentence Overall Rated As", end = " ")

	# # decide sentiment as positive, negative and neutral
	# if sentiment_dict['compound'] >= 0.05 :
	# 	print("Positive")

	# elif sentiment_dict['compound'] <= - 0.05 :
	# 	print("Negative")

	# else :
	# 	print("Neutral")
    
def flipkart(url,c):
    page = requests.get(url, headers=Headers(os='win',browser='chrome',headers=True).generate())
    page_soup = bs4.BeautifulSoup(page.content,"html.parser")
    table={}
    if(page_soup.find('div',class_='X3BRps')):
        details=page_soup.find('div',class_='X3BRps')
        for row in details.findAll('div',class_='row'):
            l=row.findAll('div')
            table[l[0].text]=l[1].text
    elif(page_soup.find('table',class_='_14cfVK')):
        details=page_soup.findAll('tr',class_="_1s_Smc row")
        for row in details:
            table[row.find('td').text]=row.find('li').text
    with open('Data'+str(c)+'.json','w') as f:
        json.dump(table,f)
def amazon(url,c):
    page = requests.get(url, headers=Headers(os='win',browser='chrome',headers=True).generate())
    page_soup = bs4.BeautifulSoup(page.content,"html.parser")
    table={}
    if(page_soup.find('table',id='productDetails_techSpec_section_1')):
        details=page_soup.find('table',id='productDetails_techSpec_section_1')
        for row in details.findAll('tr'):
            value=row.find('td').text.strip()
            strencode=value.encode("ascii","ignore")
            table[row.find('th').text.replace('\n','')]=strencode.decode()
    elif(page_soup.find('div',id='detailBullets_feature_div')):
        details=page_soup.find('div',id='detailBullets_feature_div')
        for row in details.findAll('span',class_='a-list-item'):
            l=row.findAll('span')
            s=l[0].text.strip().replace(' ','')
            s=s.replace('\n','')
            strencode=s.encode("ascii","ignore")
            table[strencode.decode()]=l[1].text.strip().replace(' ','')
    with open('Data'+str(c)+'.json','w') as f:
        json.dump(table,f)