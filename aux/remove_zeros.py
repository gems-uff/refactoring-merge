import pandas as pd 
from pandas.api.types import is_numeric_dtype
import arff


# dependendo do arquivo o index_col pode ser 0 ou 1
data = pd.read_csv("/Users/tayanemoura/Documents/git/merge-effort-mining/result/output_consolidado.csv", index_col=1) 

attributes = list(data) 
  
for i in attributes: 
	#selected_column = data[i]
	#print (i)

	if(is_numeric_dtype(data[i])):
		column_withoutzero = data[i].loc[(data[i]!=0)]
		#if(i == "has_conflict" or i== "conflict_files" or i=="conflict_chunks" ):
		aux = column_withoutzero.to_frame()
		#print(aux.columns)
		aux.to_csv(i+'.csv')
		#arff.dump(i+'.arff'
		#		, aux.values
		#		, relation = 'relation name'
		#		, names= aux.columns)

		
