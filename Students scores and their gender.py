#Test performaces based on Gender
import kagglehub
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Download latest version
path = kagglehub.dataset_download("spscientist/students-performance-in-exams")

for fname in os.listdir(path):
    #print(fname)
    if fname.endswith(".csv"):
        df = pd.read_csv(os.path.join(path, fname))
# 1. Assign unique numbers to each string
        df['num'] = df['gender'].astype('category').cat.codes
# 2. Get indices for each string
categories = df['gender'].unique().tolist()
num_categories = len(categories)

#counts of passing and failing students
def passing_grade(score):
    if score >=60:
        return "passed"
    else:
        return "failed"
# Apply grade classification to the DataFrame

tests=['math score', 'reading score', 'writing score']
Tests_grade = [test.replace('score', 'grade') for test in tests]

test_eval=[]
for t in range(0,len(tests)): #loop over each test
    df["eval"]= df[tests[t]].apply(passing_grade) #apply the equation on the dataframe

    gender_pass_counts = df.groupby(['gender', 'eval']).size().unstack(fill_value=0)
    test_eval.append(gender_pass_counts)
combined_tests = pd.concat(test_eval, ignore_index=True)

combined_tests['gender']=['female','male']*3

result = [x for x in tests for _ in range(2)]
combined_tests['tests']=result
#combined_tests = pd.concat(test_eval, ignore_index=True)

plt.scatter(df["math score"], df["writing score"],color='green',label='Math vs Writing')
plt.scatter(df["math score"], df["reading score"],color='blue',label='Math vs reading')
plt.scatter(df["writing score"], df["reading score"],color='red',label='writing  vs reading')
plt.title("Visualizing Regressions Among Tests")
plt.xlabel("Student Scores")
plt.ylabel("Student Scores")
plt.legend()
plt.show()

# Select only relevant columns
scores = df[['math score', 'reading score', 'writing score']]

# Plot heatmap
sns.heatmap(scores.corr(), annot=True, cmap='coolwarm', center=0)
plt.title("Correlation Between Test Scores")
plt.show()
#_________________________________________________________________________________________


# Combine gender and test labels for the x-axis
combined_tests['label'] = combined_tests['gender'] + ' — ' + combined_tests['tests']

# Prepare positions on the x-axis
x = np.arange(len(combined_tests))
width = 0.35  # width of each bar

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, combined_tests['failed'], width, label='failed', color='red')
ax.bar(x + width/2, combined_tests['passed'], width, label='Passed', color='green')

#this adds numbers on the bars showing values
for container in ax.containers:
    ax.bar_label(container)

# Formatting the plot
ax.set_xticks(x)
ax.set_xticklabels(combined_tests['label'], rotation=45, ha='right')
ax.set_ylabel('Score')
ax.set_title("Evaluation Outcomes by Gender and Tests", fontsize=12,fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

#________________________________________________________________________________

# Step 3: Sort by pass % descending

total_pass= combined_tests.groupby(combined_tests['gender'])['passed'].sum().tolist()
total_fail= combined_tests.groupby(combined_tests['gender'])['failed'].sum().tolist()

per_pass_female= (total_pass[0]/(total_pass[0]+total_pass[1]))*100
per_pass_male= (total_pass[1]/(total_pass[0]+total_pass[1]))*100

per_f_female= (total_fail[0]/(total_fail[0]+total_fail[1]))*100
per_f_male= (total_fail[1]/(total_fail[0]+total_fail[1]))*100


fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].pie([per_pass_female, per_pass_male], labels=['Female', 'Male'], autopct='%1.1f%%', startangle=140, colors=["#66ff78", "#56b3d8"])
axs[0].set_title('Pass Percentage')
axs[0].axis('equal')

axs[1].pie([per_f_female, per_f_male], labels=['Female', 'Male'], autopct='%1.1f%%', startangle=140, colors=["#66ff78", "#56b3d8"])
axs[1].set_title('Fail Percentage')
axs[1].axis('equal')

plt.suptitle("Gender-Based Comparison of Student Performance in All Tests", fontweight='bold')
plt.tight_layout()
plt.show()
#______________________________________________________
