import re
import sys
import json
import pickle
import math

#Argumen check
if len(sys.argv) !=3 :
	print ("\n\\Use python \n\t tf-idf.py [data.json] [output]\n")
	sys.exit(1)


#data argumen
input_data = sys.argv[1]
output_data = sys.argv[2]
print('input data = ', input_data)
print('output data = ', output_data)

data = open(input_data).read()
list_data = data.split("\n")
# list data = [anime1, anime2 .... ]
# anime n = {judul ...}
sw = open("stopword.txt").read().split("\n")
# sw = kata kata yang tidak diperlukan

content=[]
for x in list_data :
	try:
		content.append(json.loads(x))
	except:
		continue
# print(content)
# content [
#     {'anime1'},
#     {'anime2'}
# ]

# Clean string function
def clean_str(text) :
	text = (text.encode('ascii', 'ignore')).decode("utf-8")
	text = re.sub("&.*?;", "", text)
	text = re.sub(">", "", text)    
	text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
	text = re.sub("-", " ", text)
	text = re.sub("\.+", "", text)
	text = re.sub("^\s+","" ,text)
	text = text.lower()
	return text



df_data={}
tf_data={}
idf_data={}

i=0
for data in content :
	tf={} 
	#clean and list word
	clean_title = clean_str(data['judul'])
	# clean_title = clean_str(data['book_title'])
	list_word = clean_title.split(" ")
	
	for word in list_word :
		if word in sw:
			continue
		
		#tf term frequency
		if word in tf :
			tf[word] += 1
		else :
			tf[word] = 1

		#df document frequency
		if word in df_data :
			df_data[word] += 1
		else :
			df_data[word] = 1

	tf_data[data['link']] = tf
    # tf data = {'link':tf}
	# tf_data[data['url']] = tf




# Calculate Idf
for x in df_data :
    # df data = {'kata1':3, 'kata2':8}
   idf_data[x] = 1 + math.log10(len(tf_data)/df_data[x])
    # idf_data['kata1'] = 1+ math.log10(len(tf_data)/df_data[kata1])
# print(idf_data)
# idf_data= {'kata1':2.023 ...}
tf_idf = {}

# pemberian bobot
for word in df_data:
	list_doc = []
	for data in content:
		tf_value = 0

		if word in tf_data[data['link']] :
			tf_value = tf_data[data['link']][word]

		weight = tf_value * idf_data[word]

		doc = {
			'link' : data['link'],
			'judul' : data['judul'],
			'img' : data['img'],
			'sinopsis' : data['sinopsis'],
			'genre':data['genre'],
			'score' : weight
		}

		if doc['score'] != 0 :
			if doc not in list_doc:
				list_doc.append(doc)
		
		
	tf_idf[word] = list_doc

# Write dictionary to file
with open(output_data, 'wb') as file:
     pickle.dump(tf_idf, file)