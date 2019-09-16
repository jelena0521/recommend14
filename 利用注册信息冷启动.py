#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:39:39 2019

@author: liujun
"""
import matplotlib.pyplot as plt
import numpy as np
import json

class UserShow:
    def __init__(self):
        self.file_user='BX-Users.csv'
        self.file_book='BX-Books.csv'
        self.file_rate='BX-Book-Ratings.csv'
        self.user_dict=self.load_user_data()
        self.book_dict=self.load_book_data()
        self.book_rating=self.load_book_rating_data()

        
    def load_user_data(self):
       user_dict={}
       for line in open(self.file_user,'r',encoding='ISO-8859-1').readlines():
           if line.startswith("\"User-ID\""):
               continue
           if len(line.split(';')) !=3:
               continue
           userid,addr,age=[one.replace('\"','') for one in line.strip().split(';')]
           if age=='NULL' or int(age) not in range(0,120): #默认年龄在120之间
               continue
           user_dict.setdefault(userid,{})
           user_dict[userid]['age']=int(age)
           if len(addr.split(','))<3:
               continue
           city,province,country=addr.split(',')[-3:]
           user_dict[userid]['country']=country
           user_dict[userid]['province']=province
           user_dict[userid]['city']=city
       print(list(user_dict.items())[:5])
       #json.dump(user_dict,open('user.json','w'))
       return user_dict
   
    def load_book_data(self):
        book_dict={}
        for line in open(self.file_book,'r',encoding='ISO-8859-1').readlines():
            if line.startswith('\'ISBN\''):
                continue
            isbn,book_name=line.strip().replace('\"','').split(';')[:2]
            book_dict[isbn]=book_name
        #json.dump(user_dict,open('book.json','w'))
        return book_dict
    
    def load_book_rating_data(self):
        book_rating={}
        for line in open(self.file_rate,'r',encoding='ISO-8859-1').readlines():
            if line.startswith('\"User-ID\"'):
                continue
            userid,isbn,rate=line.strip().replace('\"','').split(';')
            book_rating.setdefault(userid,[])
            if int(rate)>5:
                book_rating[userid].append(isbn)
          #json.dump(user_dict,open('book.json','w'))
        return book_rating
    
    def show(self,x,y,x_label,y_label='num'):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(np.arange(len(x)),x,rotation=90)
        for a,b in zip(np.arange(len(x)),y):
            plt.text(a,b,b,rotation=45)
        plt.bar(np.arange(len(x)),y)
        plt.show()
    
    def diffage(self):
        age_user={}
        for key in self.user_dict.keys():
            age_split=int(int(self.user_dict[key]['age'])/10)
            age_user.setdefault(age_split,0)
            age_user[age_split]=age_user[age_split]+1
        age_user_sort=sorted(age_user.items(),key=lambda x :x[0],reverse=False)
        x=[a[0] for a in age_user_sort]
        y=[a[1] for a in age_user_sort]
        print(age_user_sort)
        self.show(x,y,x_label='age')
        
    def diffpro(self):
       pro_user={}
       for key in self.user_dict.keys():
           if 'province' in self.user_dict[key].keys() and self.user_dict[key]['province']!=' n/a':
               pro_user.setdefault(self.user_dict[key]['province'],0)
               pro_user[self.user_dict[key]['province']]=pro_user[self.user_dict[key]['province']]+1
       pro_user_sort=sorted(pro_user.items(),key=lambda x :x[1],reverse=True)[:20]
       x=[a[0] for a in pro_user_sort]
       y=[a[1] for a in pro_user_sort]
       print(pro_user_sort)
       self.show(x,y,x_label='province')
    
    def diffuserage(self):
        age_books={}
        for user in self.user_dict.keys():
            if user not in self.book_rating.keys():
                continue
            if int(self.user_dict[user]['age']) in range (0,30):
                for book in self.book_rating[user]:
                    if book not in self.book_dict.keys():
                        continue
                    age_books.setdefault(book,0)
                    age_books[book]=age_books[book]+1
        print('30代用户最喜欢看的书为:')
        for one in sorted(age_books.items(),key=lambda x:x[1],reverse=True)[:10]:
            print(self.book_dict[one[0]])
        
            
       
       
      

if __name__=='__main__':
    usershow=UserShow()
    usershow.diffage()
    usershow.diffpro()
    usershow.diffuserage()