import string
import pickle
import os
import re
from stop_words import get_stop_words

def preprocess(line):
	stop_words = get_stop_words('english')
	if (line.strip()):
		exclude = set(string.punctuation)
		old_str = ''.join(ch for ch in line if ch not in exclude) #removing punctuation
		stripped = ''.join(c for c in old_str if (0 < ord(c) < 127 and c not in string.digits)) #removing non ascii, and digits (check and romans?)
		new_string=' '.join([word.lower() for word in stripped.split() if word.lower() not in (stop_words)]) #convertng to lower case and removing stopwords
		return new_string
	return ''
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
'''
#saving dictionary
output = open('dictionary.txt', 'w')

pickle.dump(dict_index, output)
output.close()
'''
'''
output = open('bigram_dictionary.txt', 'w')

pickle.dump(bigram_dict_index, output)
output.close()
'''

org_query=raw_input('Query: ')
org_query=preprocess(org_query)
if(len(org_query.split())==1):
	#to do
	output = open('dictionary.txt', 'rb')
	obj_dict = pickle.load(output)
elif(len(org_query.split())>1):
	output = open('bigram_dictionary.txt', 'rb')
	obj_dict = pickle.load(output)

arr=org_query.split()
#print org_query
if(len(arr)==1): #use unigram
	main_list=[]
	if(obj_dict.has_key(arr[0])):
		index=arr[0]
		main_list=obj_dict[index]['doc'][1]
	if(len(main_list)>0):
		print "Books containing this query are: "
		for element in main_list:
				print element+" at line numbers - "+str(obj_dict[index][element][1])
	else:
		print "Books containing this query are: No book found"
elif (len(arr)>1): #use bigram
	main_list=[]
	for iteration in range(0,len(arr)-1):
		index=arr[iteration]+" "+arr[iteration+1]
		if(obj_dict.has_key(index)):
			list_doc=obj_dict[index]['doc'][1]
			if(len(main_list)==0):
				main_list=list_doc
			else:
				main_list=list(set(main_list) & set(list_doc))
		else:
			main_list=[]
			break
	line_no_list=[]
	if(len(main_list)>0):
		print "Books containing this query are: "
		line_no_list=[]
		for element in main_list:
			for iteration in range(0,len(arr)-1):
				index=arr[iteration]+" "+arr[iteration+1]
				if(obj_dict.has_key(index)):
					list_doc=obj_dict[index][element][1]
					if(len(line_no_list)==0):
						line_no_list=list_doc
					else:
						line_no_list=list(set(line_no_list) & set(list_doc))
			print element+" at line numbers - "+str(line_no_list[:])
	else:#no word in index
		print "Books containing this query are: No book found"
else:
	print "Books containing this query are: No book found"
