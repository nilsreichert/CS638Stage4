import py_stringmatching as sm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from py_stringmatching import utils
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
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

    #Calculate the Make Model Similarity Score
    MakeModel_Score = row['MatchScore']
    feature_vector.append(MakeModel_Score)

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
    #print(VIN_Score)
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

    
    
    #price
    priceData = abs(row['Eastprice'] - row['Westprice'])
    if priceData  < 2005:
        price = 1
    elif priceData < 5000:
        price =.66
    elif priceData < 9905:
        price = .33
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
        odom_feat = .66
    elif 36177 <= abs_diff < 66189:
        odom_feat = .33
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
    if row['Eastfuel'] == row['Westfuel']:
        fuel = 1
    else:
        fuel = 0
    feature_vector.append(fuel)

    #cylinders
    if row['Eastcylinders'] == row['Westcylinders']:
        cyl = 1
    else:
        cyl = 0
    feature_vector.append(cyl)

    #Add feature vector to the feature vector table
    feature_vector_table.append(feature_vector)

#Run Tree Algs using feature_vector_table and gold_labels

Data_Train, Data_Test, Gold_Train, Gold_Tests = train_test_split(feature_vector_table, gold_labels, test_size=0.25, random_state=0)

#initialize our decision tree
dtree = tree.DecisionTreeClassifier()
dtree_fit = dtree.fit(Data_Train, Gold_Train)
dtree_pred = dtree_fit.predict(Data_Test)
print(f1_score(Gold_Tests, dtree_pred , average="macro"))
print(precision_score(Gold_Tests, dtree_pred , average="macro"))
print(recall_score(Gold_Tests, dtree_pred , average="macro"))  
dtree_score = dtree_fit.score(Data_Test, Gold_Tests)
print(dtree_score)
print()


rforrest = RandomForestClassifier()
rforrest_fit = rforrest.fit(Data_Train, Gold_Train)
rforrest_score = rforrest_fit.score(Data_Train, Gold_Train)
rforrest_pred = rforrest_fit.predict(Data_Test)
print(f1_score(Gold_Tests, rforrest_pred , average="macro"))
print(precision_score(Gold_Tests, rforrest_pred , average="macro"))
print(recall_score(Gold_Tests, rforrest_pred , average="macro"))  
print(rforrest_score)
print()




lreg = LogisticRegression()
lreg_fit = lreg.fit(Data_Train, Gold_Train)
lreg_score = lreg_fit.score(Data_Train, Gold_Train)
lreg_pred = lreg_fit.predict(Data_Test)
print(f1_score(Gold_Tests, lreg_pred , average="macro"))
print(precision_score(Gold_Tests, lreg_pred , average="macro"))
print(recall_score(Gold_Tests, lreg_pred , average="macro")) 
print(lreg_score)
print()


svc = SVC()
svc_fit = svc.fit(Data_Train, Gold_Train)
svc_score = svc_fit.score(Data_Train, Gold_Train)
sfc_pred = svc_fit.predict(Data_Test)
print(f1_score(Gold_Tests, sfc_pred , average="macro"))
print(precision_score(Gold_Tests, sfc_pred , average="macro"))
print(recall_score(Gold_Tests, sfc_pred , average="macro"))
print(svc_score)
print()


nb = GaussianNB()
nb_fit = nb.fit(Data_Train, Gold_Train)
nb_score = nb_fit.score(Data_Train, Gold_Train)
nb_pred = nb_fit.predict(Data_Test)
print(f1_score(Gold_Tests, sfc_pred , average="macro"))
print(precision_score(Gold_Tests, sfc_pred , average="macro"))
print(recall_score(Gold_Tests, sfc_pred , average="macro"))
print(nb_score)


