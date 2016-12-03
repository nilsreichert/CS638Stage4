import py_stringmatching as sm
import pandas as pd
from py_stringmatching import utils
#incomplete list of necessary imports
#we will need to import the necessary scikit learn packages when we get there

#Initialize the q-gram tokenizer
qg3_tok_set = sm.QgramTokenizer(qval=3, return_set=True)

#Initialize similarity score calculators
jac = sm.Jaccard()
oc = sm.OverlapCoefficient()

#read in the CSV into a DataFrame
gold_raw_data = pd.read_csv('gold.csv', low_memory=False)

#Extract the gold labels from the DataFrame
#This becomes an input into our Learning Algs
gold_labels = gold_raw_data['Match?']

#This is our feature vector table
#Another input into our Learning Algs.
#We add feature vectors from with in the for
#loop that iterates over the DataFrame 
feature_vector_table = []

for index, row in gold_raw_data.iterrows():
    #Note: access Attributes as row['attributename']

    #initialize the feature vector
    feature_vector = []
    
    #Do all necessary work to build the feature vector


    #Calculate the VIN Similarity Score
    VIN_Score = 0
    eVIN = row['Eastvin']
    wVIN = row['Westvin']
    if(not(eVIN==None) and not(eVIN=="")  and (isinstance(eVIN, str))):
        if(not(wVIN==None) and not(wVIN=="")  and (isinstance(wVIN, str))):
            eVIN_tok = qg3_tok_set.tokenize(eVIN)
            wVIN_tok = qg3_tok_set.tokenize(wVIN)
            j = jac.get_raw_score(eVIN_tok, wVIN_tok)
            o = oc.get_sim_score(eVIN_tok, wVIN_tok)
            VIN_Score = ((j+o)/2)
    feature_vector.append(VIN_Score)


    #Calculate the Title Similarity Score
    Title_Score = 0
    eTitle = row['Easttitle']
    wTitle = row['Westtitle']
    if(not(eTitle==None) and not(eTitle=="") and (isinstance(eTitle, str)) ):
        if(not(wTitle==None) and not(wTitle=="") and (isinstance(wTitle, str)) ):
            eTitle_tok = qg3_tok_set.tokenize(eTitle)
            wTitle_tok = qg3_tok_set.tokenize(wTitle)
            j = jac.get_raw_score(eTitle_tok, wTitle_tok)
            o = oc.get_sim_score(eTitle_tok, wTitle_tok)
            Title_Score = ((j+o)/2)
    feature_vector.append(Title_Score)

    #Calculate the Make Model Similarity Score
    MakeModel_Score = row['MatchScore']
    feature_vector.append(MakeModel_Score)
    

    #Add feature vector to the feature vector table
    feature_vector_table.append(feature_vector)

#Run Tree Algs using feature_vector_table and gold_labels