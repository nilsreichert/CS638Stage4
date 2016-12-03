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
    
    #price
    priceData = abs(row['Eastprice'] - row['Westprice'])
    if priceData  < 2005:
    	price = 1
    elif priceData < 5000:
    	price =.75
    elif priceDataq < 9905:
        price = .5
    else:
        price = 0
    feature_vector.append(price)

    #odometer feature vector building
    east_od = row['Eastodometer']
    west_od = row['Westodometer']
    abs_diff = abs(east_od - west_od)
    odom_feat = 1
    if 0 <= abs_diff < 15936:
        odom_feat = 1
    elif 15936 <= abs_diff < 36177:
        odom_feat = .75
    elif 36177 <= abs_diff < 66189:
        odom_feat = .5
    else:
        odom_feat = 0
    feature_vector.append(odom_feat)

    #color

    if row['Eastpaint_color'] == row['Westpaint_color']:
    	color = 1
    else:
        color = 0
    feature_vector.append(color)

    #size
    if row['Eastsize'] == row ['Westsize']:
    	size = 1
    else:
    	size = 0
    feature_vector.append(color)

    #fuel
    if row['Eastfuel'] == row['WestFuel']:
    	fuel = 1
    else:
    	fuel = 0
    feature_vector.append(fuel)

    #cylinders
    if row['Eastylinders'] == row['westcylinders']:
    	cyl = 1
    else:
        cyl = 0
    feature_vector.append(cyl)
>>>>>>> e1fc1d07dc47d7e00c2b832c3c9864f69e8e0b2d

    #Add feature vector to the feature vector table
    feature_vector_table.append(feature_vector)

#Run Tree Algs using feature_vector_table and gold_labels
