# -*- coding: utf-8 -*-
from __future__ import division
import re
import string
import pickle
import os
import re
from stop_words import get_stop_words


def preprocess(line): #to do preprocessing
	stop_words = get_stop_words('english')
	if (line.strip()):
		#exclude = set(string.punctuation)
		#old_str = ''.join(ch for ch in line if ch not in exclude) #removing punctuation
		stripped = ''.join(c for c in line if (0 < ord(c) < 127 and c not in string.digits)) #removing non ascii, and digits (check and romans?)
		#new_string=' '.join([word.lower() for word in stripped.split() if word.lower() not in (stop_words)]) #convertng to lower case and removing stopwords
		return stripped
	return ''


def string_intersection(s1,s2): #finding a normalized score between a pair of sentences
	s1=set(s1.split(" "))
	s2=set(s2.split(" "))
	if(len(s1)+len(s2)==0):
		return 0
	else:
		avg=(len(s1)+len(s2))/2;
		return (len(s1.intersection(s2))/avg)

def text_to_para(text): #converting the document into paragraphs
	return text.split("\n\n")

#building the sentence dictionary that contains the key value pair. Key is sentence, value is its importance in the paragraph
def sentence_rank(text): 
	new_text=text.replace("\n",". ")
	new_text=new_text.split(". ")
	n=len(new_text)
	sentence_dic={}
	
	table=[[0 for i in range(n)] for j in range(n)]

	for i in range(0,n):
		for j in range(0,n):
			table[i][j]=string_intersection(new_text[i],new_text[j])

	for i in range(0,n):
		total=0
		for j in range(0,n):
			if(i!=j):
				total=total+table[i][j]

		sentence_dic[preprocess(new_text[i])]=total
	return sentence_dic

def best_sentence(para,sentence_dic): #finding the best sentence in the paragraph
	new_text=para.replace("\n",". ")
	list_sentence=new_text.split(". ")
	if(len(list_sentence)<=1):
	 	return ""
	ideal=""
	max=0
	for line in list_sentence:
	 	line=preprocess(line)
	 	if(line):
	 		if(sentence_dic[line]>max):
	 			max=sentence_dic[line]
	 			ideal=line
	return ideal

def build_summary(text, sentence_dic): #building the summary by appending best lines of each paragraph
	summary=[]
	paras=text_to_para(text)
	for p in paras:
		line=best_sentence(p,sentence_dic)
		line=line.strip()
		if(line):
			summary.append(line)

	summary=("\n").join(summary)
	return summary



if not os.path.exists('read_me.txt'):
	print "Document to summarize doesn't exist"
else:	
	f=open('read_me.txt','r')
	content=""
	for line in f:
		content=content+line
	#print content

	sentence_dic=sentence_rank(content)
	summary=build_summary(content,sentence_dic)

	#print sentence_dic
	print "Summary of the document is -\n",summary

	print "Original length ",len(content) 
	print "Summary length " ,len(summary)

	#Preprocessing and saving  updated file
'''
f = open('book5_georgesseurat.txt', 'r')
f2=open('./Files/updated_book5_georgesseurat.txt','w')
f3=open('inverted_index.txt','w')
stop_words = get_stop_words('english')
#print stop_words
for line in f:
	if (line.strip()):
		#print line,
		exclude = set(string.punctuation)
		old_str = ''.join(ch for ch in line if ch not in exclude) #removing punctuation
		stripped = ''.join(c for c in old_str if (0 < ord(c) < 127 and c not in string.digits)) #removing non ascii, and digits (check and romans?)
		new_string=' '.join([word.lower() for word in stripped.split() if word.lower() not in (stop_words)]) #convertng to lower case and removing stopwords
		print new_string
		if(len(new_string)>1):
			f2.write(new_string)
			f2.write('\n')
f2.close()
'''

#Building bigram inverted index

'''
bigram_dict_index={}
file_names=['book1.txt','book2.txt','book3.txt','book4.txt','book5.txt']
for name in file_names:
    if name.endswith(".txt"):
		f2=open('/home/shweta/IR/'+ name,'r') #in loop
		line_no=0
		for line in f2:
			arr=line.split()
			line_no+=1
			if (line.strip()):
				line=preprocess(line)
				for iteration in range(0,len(arr)-1):
					index=arr[iteration]+" "+arr[iteration+1]
					if(bigram_dict_index.has_key(index)):
						if(bigram_dict_index[index].has_key(name)):
							bigram_dict_index[index][name][0]+=1
							bigram_dict_index[index][name][1].append(line_no)
						else:
							bigram_dict_index[index]['doc'][0]+=1
							bigram_dict_index[index]['doc'][1].append(name)
							bigram_dict_index[index][name]=[1,[line_no]]
					else:
						bigram_dict_index[index]={}
						bigram_dict_index[index]['doc']=[1,[name]] #for no of books
						bigram_dict_index[index][name]=[1,[line_no]] #id of book and positions
		f2.close()

#Building unigram inverted index
#removing single letter words

dict_index={}
for name in file_names:
    if name.endswith(".txt"):
		f2=open('/home/shweta/IR/'+ name,'r') #in loop
		line_no=0
		for line in f2:
			line_no=line_no+1
			line=preprocess(line)
			arr=line.split()
			for word in arr:
				if(len(word)>1):
					if(dict_index.has_key(word)): #if the word exists in the dictionary
						if(dict_index[word].has_key(name)): #if the current doc already had the key word
							dict_index[word][name][0]+=1
							(dict_index[word][name][1]).append(line_no)
						else: #if the current doc doesn't have the key word
							dict_index[word]['doc'][0]+=1
							(dict_index[word]['doc'][1]).append(name)
							dict_index[word][name]=[1,[line_no]]
					else:
						dict_index[word]={}
						dict_index[word]['doc']=[1,[name]] #for no of books
						dict_index[word][name]=[1,[line_no]] #id of book and positions

		f2.close()
		#print dict_index
		#print len(dict_index)

'''