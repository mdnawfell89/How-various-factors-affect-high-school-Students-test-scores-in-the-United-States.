#Students performance based on preperation test course
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
# Assign unique numbers to each string
        df['num'] = df['test preparation course'].astype('category').cat.codes
# Get indices for each string
categories = df['test preparation course'].unique().tolist()
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
#loop over each test
for t in range(0,len(tests)):
    #apply the equation on the dataframe 
    df["eval"]= df[tests[t]].apply(passing_grade) 

    course_pass_counts = df.groupby(['test preparation course', 'eval']).size().unstack(fill_value=0)
    test_eval.append(course_pass_counts)
combined_tests = pd.concat(test_eval, ignore_index=True)

combined_tests['test preparation course']=['completed','none']*3


result = [x for x in tests for _ in range(2)]
combined_tests['tests']=result

# Combine test preparation course and test labels for the x-axis
combined_tests['label'] = combined_tests['test preparation course'] + ' — ' + combined_tests['tests']

# Prepare positions on the x-axis
x = np.arange(len(combined_tests))
width = 0.35  # width of each bar

#plottinf number of students failed/passed based on test prep course
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
ax.set_title("Student Outcomes Based on Test Prep Completion Across Different Tests")
ax.legend()
plt.tight_layout()
plt.show()

#________________________________________________________________________________

#finding overall performance of students completed the course vs those who did not.
total_pass= combined_tests.groupby(combined_tests['test preparation course'])['passed'].sum().tolist()
total_fail= combined_tests.groupby(combined_tests['test preparation course'])['failed'].sum().tolist()

per_pass_completed= (total_pass[0]/(total_pass[0]+total_pass[1]))*100
per_pass_none= (total_pass[1]/(total_pass[0]+total_pass[1]))*100

per_f_completed= (total_fail[0]/(total_fail[0]+total_fail[1]))*100
per_f_none= (total_fail[1]/(total_fail[0]+total_fail[1]))*100

#plotting the percentages
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].pie([per_pass_completed, per_pass_none], labels=['completed', 'none'], autopct='%1.1f%%', startangle=140, colors=["#66ff78", "#56b3d8"])
axs[0].set_title('Pass % by test preparation course')
axs[0].axis('equal')

axs[1].pie([per_f_completed, per_f_none], labels=['completed', 'none'], autopct='%1.1f%%', startangle=140, colors=["#66ff78", "#56b3d8"])
axs[1].set_title('Fail % by test preparation course')
axs[1].axis('equal')

fig.suptitle("Student Outcomes Based on Prep course Completion for All Tests", fontsize=16, fontweight='bold')

plt.tight_layout()
plt.show()
#______________________________________________________
