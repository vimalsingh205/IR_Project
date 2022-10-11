from bs4 import BeautifulSoup
import pandas as pd_search_eng
import numpy
import csv
import string
import requests

from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer
ps=PorterStemmer()


def searchEngine(SearchKeyword):

  ## List to hold the information from the URL for research school_of_economics_output.
  containerlist_search_eng = []

  page = range(0,13)

  ## lopping all the pages and fill the variable.
  for pages in page:
      seed = 'https://pureportal.coventry.ac.uk/en/organisations/school-of-economics-finance-and-accounting/publications/?page={}'.format(pages)
      QueueVal_search_eng = [seed]
      countVal_search_eng = 0
      while(countVal_search_eng < 25 and QueueVal_search_eng!=[]):
        countVal_search_eng +=1
        url = QueueVal_search_eng.pop(0)
        
        response_val_search_eng = requests.get(url)
        economics_BeautiSoup_search_eng = BeautifulSoup(response_val_search_eng.text, 'html.parser')
        result_Link_search_eng = economics_BeautiSoup_search_eng.findAll('div', {'class':'result-container'})

        for tags_search_eng in result_Link_search_eng:
          try:
            collections_search_eng = {
              'link':tags_search_eng.find('a',{'class':'link'})['href'],
              'author link':tags_search_eng.find('a',{'class':'link person'})['href'],
              'author':tags_search_eng.find('a',{'class':'link person'}).text,
              'title':tags_search_eng.find('a',{'class':'link'}).text,
              'date':tags_search_eng.find('span',{'class':'date'}).text,            
              }
          except TypeError:
            collections_search_eng = {
                'link':tags_search_eng.find('a',{'class':'link'})['href'],
                'author link':None,
                'author':' ',
                'title':tags_search_eng.find('a',{'class':'link'}).text,
                'date':tags_search_eng.find('span',{'class':'date'}).text
              }
          if(collections_search_eng not in containerlist_search_eng):
            containerlist_search_eng.append(collections_search_eng)

  df_search_eng = pd_search_eng.DataFrame(containerlist_search_eng)
  print(df_search_eng)

  df_search_eng.to_csv('collections_search_eng.csv')
  df_search_eng1=pd_search_eng.DataFrame()

  df_search_eng1['text']= df_search_eng['title']+ '' +df_search_eng['author']
  print(df_search_eng1)

  with open('collections_search_eng.csv') as csvfile:

    reader = csv.DictReader(csvfile)

  df_search_eng.date=pd_search_eng.to_datetime(df_search_eng.date)

  result = string.punctuation
  school_of_economics_output = df_search_eng.replace(result,"")

  sw = stopwords.words('english')

  school_of_economics_output.drop(["link", "author link", "date"],axis=1,inplace=True)

  school_of_economics_output.to_csv('school_of_economics_output_results',index=False)

  ##print(school_of_economics_output)
  ##  cat collections_search_eng.csv

  ## Data Preprocessing
  def text_preprocess(text):
      nltk_english_stopwords = stopwords.words('english')
      trans = str.maketrans('', '', string.punctuation)

      text = text.translate(trans)
      text = text.lower()
      cleaned_text = ""
      
      for word in text.split():

          if word not in nltk_english_stopwords:

              cleaned_text += word + " "

      return cleaned_text

  df_search_eng["title"] = df_search_eng["title"].apply(text_preprocess)
  with open('collections_search_eng.csv',encoding = "utf8") as csvfile:
    search_eng_csvreader = csv.DictReader(csvfile)

    ## to store the data in the list and use it to extract the data when user tried in search engine
    search_eng_count = 0
    Author = []
    publishDate = []
    new = [] 
    
    ## Loop to collect all the title Author and date Total 638 records available
    for csv_row in search_eng_csvreader:
        search_eng_count = search_eng_count + 1
        print (csv_row['title'])
        new.append(csv_row['title'])
        Author.append(csv_row['author'])
        publishDate.append(csv_row['date'])
        if search_eng_count > 640:
            break
            
  ## Print the data on the Screen to verify the title vs Author.          
  ##print(new)
  ##print(Author)
  ##print(publishDate)

  ## Used for inverted Index framework.
  search_eng_inverted_index = {}
  for increment, search_eng_doc in enumerate(new):
    for search_eng_term in search_eng_doc.split():
        if search_eng_term in search_eng_inverted_index:
            search_eng_inverted_index[search_eng_term].add(increment)
        else: search_eng_inverted_index[search_eng_term] = {increment}
  search_eng_inverted_index  

  def query_page_no(value):     
                      searchout3 = []
                      searchout4 = []
                      valuelist = value.split();                   
                      for increment, val in enumerate(valuelist):                          
                          for increment, search_eng_doc in enumerate(new):                            
                              for search_eng_term in search_eng_doc.split():
                                ##print(doc)                       
                                if search_eng_term == val:
                                    searchout3 = increment
                                    searchout4.append(searchout3)
                          
                          ## Loop for Author Value
                          for increment, search_eng_doc in enumerate(Author):                            
                              for search_eng_term in search_eng_doc.split():                                                  
                                if search_eng_term == val:
                                    searchout3 = increment
                                    searchout4.append(searchout3)

                          ## Loop for Date Value
                          for increment, search_eng_doc in enumerate(publishDate):                            
                              for search_eng_term in search_eng_doc.split():                                                  
                                if search_eng_term == val:
                                    searchout3 = increment
                                    searchout4.append(searchout3)

                          return searchout4

  def query_result():
      school_of_economics_output1 = []
      for search_eng_term in out:
        v= search_eng_term + 1
        school_of_economics_output = df_search_eng.iloc[int(search_eng_term):int(v),:].values
        school_of_economics_output1.append(school_of_economics_output)
      return school_of_economics_output1

  value = SearchKeyword
  out=query_page_no(value)
  finaloutput = query_result()
  
  return finaloutput

    ##print(query_result())
