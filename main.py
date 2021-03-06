
import streamlit as st
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("Breast Cancer Dashboard")
st.write("""
# Explore different classifier 
which one is the best
""")
dataset_name=st.sidebar.selectbox("Select dataset",("Breast Cancer","Diabetes"))
classifier_name=st.sidebar.selectbox("Select classifier",("KNN","SVM","Random Forest"))

def get_dataset(dataset_name):
    if dataset_name=="Breast Cancer":
        data = datasets.load_breast_cancer()

    else:
        data=datasets.load_diabetes()
    x=data.data
    y=data.target
    return x,y
x,y= get_dataset(dataset_name)
st.write("shape of dataset",x.shape)
st.write("number of classes",len(np.unique(y)))

def add_parameter_ui(clf_name):
    params = dict()
    if clf_name =="KNN":
        K=st.sidebar.slider("K",1,15)
        params["K"]=K
    elif clf_name=="SVM":
         C=st.sidebar.slider("C",0.01,10.0)
         params["C"] = C
    else:
        max_depth=st.sidebar.slider("max_depth",2,15)
        n_estimators = st.sidebar.slider("n_estimators",1,100)
        params["max_depth"]= max_depth
        params["n_estimators"]=n_estimators
    return params

params = add_parameter_ui(classifier_name)

def get_classifier(clf_name, params):
    if clf_name =="KNN":
       clf=KNeighborsClassifier(n_neighbors=params["K"])
    elif clf_name=="SVM":
         clf=SVC(C=params["C"])


    else:

        clf=RandomForestClassifier(n_estimators=params["n_estimators"],
                                   max_depth=params["max_depth"],random_state=1234)
    return clf

clf=get_classifier(classifier_name,params)

# classification

X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=.2,random_state=1234)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test,y_pred)
st.write(f"classifier = {classifier_name}")
st.write(f"accuracy={acc}")

#plot
pca =PCA(2)
x_projected = pca.fit_transform(x)
x1=x_projected[:,0]
x2=x_projected[:,1]

fig=plt.figure()
plt.scatter(x1,x2,c=y,alpha=.8,cmap='viridis')
plt.xlabel("Principal Component 1")
plt.ylabel("principal component 2")
plt.colorbar()
st.pyplot(fig)




