import pandas as pd 
from pandas.api.types import is_numeric_dtype
import arff

data = pd.read_csv("/Users/tayanemoura/Documents/git/merge-effort-mining/result/output.csv", index_col=0) 

attributes = list(data) 
  
for i in attributes: 
	#selected_column = data[i]

	if(is_numeric_dtype(data[i])):
		column_withoutzero = data[i].loc[(data[i]!=0)]


		aux = column_withoutzero.to_frame()
		#print(aux.columns)
		aux.to_csv(i+'.csv')
		#arff.dump(i+'.arff'
		#		, aux.values
		#		, relation = 'relation name'
		#		, names= aux.columns)

		
