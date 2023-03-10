# -*- coding: utf-8 -*-
"""DiseasePrediction_SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j7C_g_1z04HM4HQ45xvQZyX3DcXl84ND
"""

# all the important imports
import warnings
warnings.filterwarnings('ignore')
import numpy as np  ## data manipulation
import pandas as pd   ## data frames
import seaborn as sns
from sklearn.preprocessing import LabelEncoder # encoding the categorical datas
import matplotlib.pyplot as plt ## for plotting the graphs
from sklearn.svm import SVC ## for Support Vector Machine Algo
from sklearn.naive_bayes import GaussianNB ## for Naive Bayes 
from sklearn.ensemble import RandomForestClassifier ## for Random Forest
from sklearn import linear_model ## for Multiple Linear Regression
from sklearn.linear_model import LogisticRegression ## for Logistic Regression
from sklearn.neighbors import KNeighborsClassifier ## for KNN
from sklearn.metrics import accuracy_score, confusion_matrix # for accuracy_score and confusion_matrix

# loading the training and testing datasets
training_data = pd.read_csv("Training.csv")
testing_data = pd.read_csv("Testing.csv")

# getting the dimensions of the datafram 
#training_data.shape (4920, 134)
#testing_data.shape (42, 133)

# updating the training set by dropping the "unnamed: 133" column
training_data = training_data.drop("Unnamed: 133", axis="columns")

disease_counts = training_data['prognosis'].value_counts()

temp_df = pd.DataFrame({
    "Disease": disease_counts.index,
    "Counts": disease_counts.values
})
plt.figure(figsize = (10,5))
sns.barplot(x = "Disease", y = "Counts", data = temp_df)
plt.xticks(rotation=90)
plt.show()

# the training data is balanced :)

## encoding the target categorical values
encoder = LabelEncoder()
training_data["prognosis"] = encoder.fit_transform(training_data["prognosis"])
training_data["prognosis"].value_counts() # shows the encoded value corresponding to each diagnosed disease(42)

testing_data["prognosis"] = encoder.fit_transform(testing_data["prognosis"])
testing_data["prognosis"].value_counts()

# splitting the training_data and testing_data into target values and features
training_data_features = training_data.iloc[:, : -1]
training_data_target = training_data.iloc[:,-1]
testing_data_features = testing_data.iloc[:, : -1]
testing_data_target = testing_data.iloc[:, -1]

# applying SVM 
svm_model = SVC()
svm_model.fit(training_data_features, training_data_target)
preds = svm_model.predict(testing_data_features)

print(f"Accuracy on train data by SVM Classifier\
: {accuracy_score(training_data_target, svm_model.predict(training_data_features))*100}")
 
print(f"Accuracy on test data by SVM Classifier\
: {accuracy_score(testing_data_target, preds)*100}")
cf_matrix = confusion_matrix(testing_data["prognosis"], preds)
plt.figure(figsize=(15,10))
sns.heatmap(cf_matrix, annot=True)
plt.title("Confusion Matrix for SVM Classifier on Test Data")
plt.show()

# applying Naive Bayes Classifier
nb_model = GaussianNB()
nb_model.fit(training_data_features, training_data_target)
preds = nb_model.predict(testing_data_features)

print(f"Accuracy on train data by Naive Bayes Classifier\
: {accuracy_score(training_data_target, nb_model.predict(training_data_features))*100}")
 
print(f"Accuracy on test data by Naive Bayes Classifier\
: {accuracy_score(testing_data_target, preds)*100}")
cf_matrix = confusion_matrix(testing_data["prognosis"], preds)
plt.figure(figsize=(12,8))
sns.heatmap(cf_matrix, annot=True)
plt.title("Confusion Matrix for Naive Bayes Classifier on Test Data")
plt.show()

# Random Forest Classifier
rf_model = RandomForestClassifier(random_state=18)
rf_model.fit(training_data_features, training_data_target)
preds = rf_model.predict(testing_data_features)

print(f"Accuracy on train data by Random Forest Classifier\
: {accuracy_score(training_data_target, rf_model.predict(training_data_features))*100}")
 
print(f"Accuracy on test data by Random Forest Classifier\
: {accuracy_score(testing_data_target, preds)*100}")
 
cf_matrix = confusion_matrix(testing_data["prognosis"], preds)
plt.figure(figsize=(12,8))
sns.heatmap(cf_matrix, annot=True)
plt.title("Confusion Matrix for Random Forest Classifier on Test Data")
plt.show()

# Multiple Linear Regression
regr = linear_model.LinearRegression()
regr.fit(training_data_features, training_data_target)

# type([testing_data_features.iloc[0, :]]) -> List

# for i in range(testing_data_features.shape[0])
preds = []
for i in range(testing_data_features.shape[0]):
  prediction = regr.predict([testing_data_features.iloc[i,:]])
  prediction = int(np.round(prediction))
  preds.append(prediction)
# preds  # shows the predicted values in list rounding off to the nearest target value

length = len(testing_data_target)
correct = 0
for i in range(length):
  if(testing_data_target[i] == preds[i]):
    correct += 1
print("The Score of Multiple Linear Regression is : ", correct/length)
cm = confusion_matrix(testing_data_target, preds)
print("\nConfusion Matrix\n")
plt.figure(figsize=(15,10))
sns.heatmap(cm, annot=True)
plt.title("Confusion Matrix for Mulitple Linear Regression on Test Data")
plt.show()

# Logistic Regression

lreg= LogisticRegression()
lreg.fit(training_data_features, training_data_target)

y_predicted = lreg.predict(testing_data_features)

# Accuracy Score and Confusion Matrix
score = lreg.score(testing_data_features, testing_data_target)*100
cm = confusion_matrix(testing_data_target, y_predicted)
print("The Accuracy of the Logistic Regression is : ", score)
print("\nConfusion Matrix\n")
plt.figure(figsize=(15,10))
sns.heatmap(cm, annot=True)
plt.title("Confusion Matrix for Logistic Regression on Test Data")
plt.show()

# K-Nearest Neighbour
train_accuracy = []
test_accuracy = []

# testing the k values in the range (1,11)
neighbors = np.arange(1, 11)
for i in range(1,11):
  knn = KNeighborsClassifier(n_neighbors=i)
  knn.fit(training_data_features, training_data_target)
      
  # Compute training and test data accuracy
  train_accuracy.append(knn.score(training_data_features, training_data_target))
  test_accuracy.append(knn.score(testing_data_features, testing_data_target))

# Generate plot
plt.plot(neighbors, test_accuracy, label = 'Testing dataset Accuracy')
plt.plot(neighbors, train_accuracy, label = 'Training dataset Accuracy')
  
plt.legend()
plt.xlabel('n_neighbors')
plt.ylabel('Accuracy')
plt.show()


# we can use any k value, since it's giving accuracy of 1 at each value of k

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(training_data_features, training_data_target)

predsKNN = knn.predict(testing_data_features)

correctKNN = 0
for i in range(len(preds)):
  if(testing_data_target[i] == preds[i]):
    correctKNN += 1
print("The Accuracy of the KNN is : ", correctKNN/len(preds))

cmKNN = confusion_matrix(testing_data_target, predsKNN)
print("\nConfusion Matrix\n")
plt.figure(figsize=(15,10))
sns.heatmap(cmKNN, annot=True)
plt.title("Confusion Matrix for KNN on Test Data")
plt.show()

# Desicion Tree 

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

d = pd.read_csv("Training.csv")
# d.describe()

d.drop('Unnamed: 133', axis=1, inplace=True)
# d.columns

#splitting the data frame
a = d.drop('prognosis', axis=1) #dropping the prognosis column
b = d['prognosis'] #just the prognosis column
x_train, x_test, y_train, y_test = train_test_split(a, b, test_size=0.5, random_state=42)
#half the data for testing, half for training : splitting this way helps evaluate the performance, and avoids overfitting

tree = DecisionTreeClassifier()
visual_tree = DecisionTreeClassifier(max_depth = 10, random_state = 42)
#setting max depth to 10 to visualize this sample tree
tree.fit(x_train, y_train)
visual_tree.fit(x_train, y_train)
#creating the tree, fitting the training data

#visualizing the visual_tree with max depth = 10

from sklearn.tree import export_graphviz
import graphviz

dot_data = export_graphviz(visual_tree, out_file=None, 
                           feature_names=a.columns,  
                           class_names=b.unique(),  
                           filled=True, rounded=True,  
                           special_characters=True)

pred = tree.predict(x_test)
acc = tree.score(x_test, y_test)

print("accuracy = {:.2f}%".format(acc*100))

# Testing
new_data = pd.read_csv("/content/Testing.csv")

# Separate the features and target variable from the new dataset
X_new = new_data.drop('prognosis', axis=1)
y_new = new_data['prognosis']

y_pred = tree.predict(X_new)

accuracy = accuracy_score(y_new, y_pred)

cmDecisionTree = confusion_matrix(y_new, y_pred)

plt.figure(figsize=(20, 10))

sns.heatmap(cmDecisionTree, annot=True, cmap="YlGnBu" ,fmt='g')

print("Accuracy on new dataset: {:.2f}%".format(accuracy * 100))
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix of Decision Tree')

plt.show()