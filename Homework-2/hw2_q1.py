import string
import pickle
import os
import re
from stop_words import get_stop_words
from collections import Counter
import itertools

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
'''
#Building bigram index from 2 consecutive letters

bigram_index={}

def build_bigram(word,bigram_index):
	prev_letter='$'
	for letter in word:
		index=prev_letter+letter

		if(not(bigram_index.has_key(index))):
			bigram_index[index]=[word]
			
		elif not(word in bigram_index[index]):
			bigram_index[index].append(word)
		prev_letter=letter

	index=letter+'$'
	if(not(bigram_index.has_key(index))):
			bigram_index[index]=[word]
	elif not(word in bigram_index[index]):
		bigram_index[index].append(word)
	return bigram_index

#Building inverted index
#removing single letter words
dict_index={}
for name in os.listdir('/home/shweta/IR/Files'):
    if name.endswith(".txt"):
		f2=open('/home/shweta/IR/Files/'+ name,'r') #in loop
		pos=0
		for line in f2:
			arr=line.split()
			for word in arr:
				pos=pos+1 #position counter
				if(len(word)>1):
					bigram_index=build_bigram(word,bigram_index)
					if(dict_index.has_key(word)): #if the word exists in the dictionary
						if(dict_index[word].has_key(name)): #if the current doc already had the key word
							dict_index[word][name][0]+=1
							(dict_index[word][name][1]).append(pos)
						else: #if the current doc doesn't have the key word
							dict_index[word]['doc'][0]+=1
							(dict_index[word]['doc'][1]).append(name)
							dict_index[word][name]=[1,[pos]]
					else:			
						dict_index[word]={}
						dict_index[word]['doc']=[1,[name]] #for no of books
						dict_index[word][name]=[1,[pos]] #id of book and positions

		f2.close()
		#print dict_index
		#print len(dict_index)

#print (dict_index)
#print len(dict_index)
#print (bigram_index)
#print len(bigram_index)
'''
'''
#saving bigram
output=open('bigram_letter_dictionary.txt','w')
pickle.dump(bigram_index, output)
output.close()
'''

'''
#saving dictionary
output = open('dictionary.txt', 'w')
pickle.dump(dict_index, output)
output.close()
'''

def edit_distance(check_word,word):
	m=len(check_word)
	n=len(word)
	table=[[0 for i in range(n+2)] for j in range(m+2)]
	for i in range(0,m+1):
		for j in range(0,n+1):
			if(i==0):
				table[i][j]=j
			elif(j==0):
				table[i][j]=i
			elif(check_word[i-1]==word[j-1]):
				table[i][j]=table[i-1][j-1]
			else:
				table[i][j]=1+min(table[i][j-1],table[i-1][j],table[i-1][j-1])
	return table[m][n]		

output = open('dictionary.txt', 'rb')
obj_dict = pickle.load(output)
output = open('bigram_letter_dictionary.txt', 'rb')
bi_dict = pickle.load(output)

org_query = raw_input('Query: ')
stop_words = get_stop_words('english')
exclude = set(string.punctuation)
old_str = ''.join(ch for ch in org_query if ch not in exclude) #removing punctuation
stripped = ''.join(c for c in old_str if (0 < ord(c) < 127 and c not in string.digits)) #removing non ascii, and digits (check and romans?)
new_query=' '.join([word.lower() for word in stripped.split() if word.lower() not in (stop_words)]) #convertng to lower case and removing stopwords
arr=new_query.split()
main_list=[]
corrected_dict={}

for word in arr:
	if(obj_dict.has_key(word)):
		list_doc=obj_dict[word]['doc'][1] #retrieve posting list
		#print "name and frequency"+str(obj_dict[word][list_doc[0]][0])+" "+str(obj_dict[word][list_doc[1]][0])+str(list_doc)
		if(len(main_list)==0):
			main_list=list_doc
		else:
			main_list=list(set(main_list) & set(list_doc)) #in sorted order check? smallest length to longest order(?)
	else: #building a bigram list_bi that has all words with 2 adjacent letters of the original word
		prev_letter='$'
		list_bi=[]
		for letter in word:
			index=prev_letter+letter
			if bi_dict.has_key(index):
				temp=bi_dict[index]
				for item in temp:
					list_bi.append(item)
			prev_letter=letter
		index=letter+'$'
		if bi_dict.has_key(index):
				temp=bi_dict[index]
				for item in temp:
					list_bi.append(item)

		if(Counter(list_bi).most_common(1)[0][0][1]>0):

			all_possible_word= [ite for ite, it in Counter(list_bi).most_common()]
			check_list=[]
			counter=0
			for item in all_possible_word: #taking words that are within a window of 2 of the original word and has most bigrams in it
				if(len(item)==len(word) or len(item)==len(word)+1 or len(item)==len(word)-1 or len(item)==len(word)+2 or len(item)==len(word)-2):
						check_list.append(item)
						counter+=1
						if(counter==10):
							break
			mini=1000
			#print check_list
			words=[]
			for item in check_list: #now within the window finding the word with the shortest edit distance
				dis=edit_distance(item,word)
				#print item,' ',dis
				if(dis<mini):
					possible_word=item
					#print item,' ',dis
					mini=dis
			for item in check_list: #if there are >1 words of shortest edit distance
				dis=edit_distance(item,word)
				#print item,' ',dis
				if(dis==mini):
					words.append(item)

			if(len(words)==1):
				print '\''+word+ "\' corrected to "+possible_word
				new_query=new_query.replace(word,possible_word)
				list_doc=obj_dict[possible_word]['doc'][1] #retrieve posting list
				if(len(main_list)==0):
					main_list=list_doc
				else:
					main_list=list(set(main_list) & set(list_doc))
			else: #if more than 1 word of same edit distance
				corrected_dict[word]=words

		else:
			main_list=[]
			break

'''
if(len(corrected_dict)>0): #finding the most probable word for the alterntives with same edit distance
	for key in corrected_dict:
		words=corrected_dict[key]
		for possible_word in words:
			list_doc=obj_dict[possible_word]['doc'][1] #retrieve posting list
			if(len(main_list)==0):
				temp_list=list_doc
			else:
				temp_list=list(set(main_list) & set(list_doc))
			if(len(temp_list)>0): #the words occur in the same doc and hence the most probable word
				print '\''+key+ "\' corrected to "+possible_word
				new_query=new_query.replace(key,possible_word)
				main_list=temp_list
				break
'''
#print corrected_dict
if(len(corrected_dict)>0): #all words with same shortest edit distance for a given word in query. Helps to find the best among them
	arrays=[]
	arr_mainlist=[]
	ano_dict={} #reverse mapping of corrected_dict: corrected words to original words in query
	for key in corrected_dict:
		arrays.append(corrected_dict[key])
		for item in corrected_dict[key]:
			ano_dict[item]=key
	cartesian=list(itertools.product(*arrays)) #constructing cartesian product of all possible spelling corrections of the query
	#print cartesian
	for i in range(len(cartesian)): #forming arr_mainlist from possible queries given in cartesian
		append_list=[]
		for j in range(len(cartesian[i])):
			list_doc=obj_dict[cartesian[i][j]]['doc'][1] #retrieve posting list
			if(len(append_list)==0):
				append_list=list_doc
			else:
				append_list=list(set(append_list) & set(list_doc))
		if(len(main_list)==0):
			arr_mainlist.append(append_list)
		else:
			append_list=list(set(append_list) & set(main_list))
			arr_mainlist.append(append_list)

	counter=0
	x=0
	check=0
	for item in arr_mainlist: #arr_mainlist contains lists of [lists of docs] with all the words in query
		main_list=item
		temp_query=new_query
		f=1
		if(len(main_list)>0):
			tup=cartesian[counter]
			#print tup
			for el in tup:
				org=ano_dict[el]
				temp_query=temp_query.replace(org,el)
				#print temp_query+ " "+org + " "+el
			
			check=0
			for element in main_list: #main_list contains all words in query occuring in the same doc and not necessarily as an exact phrase
				f=open('/home/shweta/IR/'+element)
				line_no=0
				for line in f:
					line_no+=1
					line=preprocess(line)
					if(len(re.findall('\\b'+temp_query+'\\b', line))>0): #exact query match for 1 of the books in the main_list
						if(check==0):
							for el in tup:
								org=ano_dict[el]
								print '\''+org+ "\' corrected to "+el
							print "Query after any changes: "+ temp_query
							print "Books containing this query are: "
						print element," at line number - "+str(line_no)
						check=1
				f.close()
			#if(check==0): #no exact query match though all words of query were there in some doc
				#continue
				#print "No book found"
		else: #no word in index
			f=0
			#continue
			#print "Books containing this query are: No book found"
		if(f==1 or check==0):
			x=x+1
		counter+=1
	if(x==counter):
		print "Query after any changes: "+ new_query
		print "Books containing this query are:\nNo book found"

else:
	print "Query after any changes: "+ new_query
	#print corrected_dict


	if(len(main_list)>0):
		print "Books containing this query are: "
		check=0
		for element in main_list: #main_list contains all words in query occuring in the same doc and not necessarily as an exact phrase
			f=open('/home/shweta/IR/'+element)
			line_no=0
			for line in f:
				line_no+=1
				#new_query=preprocess(org_query)
				line=preprocess(line)
				if(len(re.findall('\\b'+new_query+'\\b', line))>0): #exact query match for 1 of the books in the main_list
					print element," at line number - "+str(line_no)
					check=1
			f.close()
		if(check==0): #no exact query match though all words of query were there in some doc
			print "No book found"
	else: #no word in index
		print "Books containing this query are: No book found"

	#TEST QUERIES
	#whle is a trmensous compliment ->whole is a tremensous compliment
	#potrait of counsellor -> portrait of councilor
	#peges ->pages
	#panting ->painting
	#callvin coldge ->calvin coolidge
	#masses did not try imeditately ->masses did not try immediately
	#snese be constured ->sense be construed
	#senetoriel voteng as a whole ->senatorial voting as a whole
	#ledership of senetor henry cabat looge ->leadership of senator henry cabot lodge
	#beleives in crist ->believes in christ
	#kandisky watercolor ->kandinsky watercolors
	#kandisky ->kandinsky ; kandmsky
	#kandisky publishes ->kandmsky publishes
	#anther ldy in green ->another lady in green
	#edgar hiliare germaine degos ->edgar hilaire germain degas
	#pennysylvia mueseum of art ->pennsylvania museum art
	#achiving an unsupected expresivenes ->achieving an unsuspected expressiveness
