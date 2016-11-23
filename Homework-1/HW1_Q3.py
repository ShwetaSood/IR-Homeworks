import string
import pickle
import os
import re
from stop_words import get_stop_words

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

#Building inverted index
#removing single letter words
'''
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

print (dict_index)
print len(dict_index)

#saving dictionary
output = open('dictionary.txt', 'w')

pickle.dump(dict_index, output)
output.close()
'''
output = open('dictionary.txt', 'rb')
obj_dict = pickle.load(output)

#print obj_dict
#print len(obj_dict)
#check sorted dictionary (?)

org_query = raw_input('Query: ')
stop_words = get_stop_words('english')
exclude = set(string.punctuation)
old_str = ''.join(ch for ch in org_query if ch not in exclude) #removing punctuation
stripped = ''.join(c for c in old_str if (0 < ord(c) < 127 and c not in string.digits)) #removing non ascii, and digits (check and romans?)
new_query=' '.join([word.lower() for word in stripped.split() if word.lower() not in (stop_words)]) #convertng to lower case and removing stopwords
arr=new_query.split()

main_list=[]
for word in arr:
	if(obj_dict.has_key(word)):
		list_doc=obj_dict[word]['doc'][1] #retrieve posting list
		#print "name and frequency"+str(obj_dict[word][list_doc[0]][0])+" "+str(obj_dict[word][list_doc[1]][0])+str(list_doc)
		if(len(main_list)==0):
			main_list=list_doc
		else:
			main_list=list(set(main_list) & set(list_doc)) #in sorted order check? smallest length to longest order(?)
	
	else:
		main_list=[]
		break

if(len(main_list)>0):
	print "Books containing this query are: ",
	check=0
	for element in main_list: #main_list contains all words in query occuring in the same doc and not necessarily as an exact phrase
		f=open('/home/shweta/IR/'+element)
		line_no=0
		for line in f:
			line_no+=1
			if(len(re.findall('\\b'+org_query+'\\b', line))>0): #exact query match for 1 of the books in the main_list
				print element," at line number - "+str(line_no)
				#f.close()
				check=1
				#break
		f.close()
	if(check==0): #no exact query match though all words of query were there in some doc
		print "No book found"
else: #no word in index
	print "Books containing this query are: No book found"