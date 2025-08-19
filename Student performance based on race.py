#test evalutaion based on race/ethnicity
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

        #this will remove the apostrophes because they interact with the code
        df2 = df["race/ethnicity"].str.replace("'","", regex=False)
        #add the new column with the apostrophe removed
        df["race/ethnicity"]= df2

#  Assign unique numbers to each string
        df['num'] = df['race/ethnicity'].astype('category').cat.codes
#  Get indices for each string
categories = df['race/ethnicity'].unique().tolist()
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
    df["pass"]= df[tests[t]].apply(passing_grade) #apply the equation on the dataframe
    
# Count number of passed/failed students per parental education level
    grouped_counts = df.groupby(['race/ethnicity', 'pass']).size().reset_index(name='count')
# Sort categories for consistent order (optional)
    order = df['race/ethnicity'].value_counts().index.tolist()

    test_eval.append(grouped_counts)
combined_tests = pd.concat(test_eval, ignore_index=True)



item = categories.pop(2)
categories.insert(0, item)

# Set up subplot grid
rows = len(tests)
cols = len(categories)
fig, axs = plt.subplots(rows, cols, figsize=(4.5 * cols, 4.5 * rows))

# Ensure axs is always 2D for consistent indexing
if rows == 1:
    axs = [axs]
if cols == 1:
    axs = [[ax] for ax in axs]

# Define parameters
pass_threshold = 60
# Loop through each test and each education category
for test_idx, test in enumerate(tests):
    # Add 'pass' column temporarily for this test
    df['pass'] = df[test].apply(lambda x: 'passed' if x >= pass_threshold else 'failed')
    
    for cat_idx, category in enumerate(categories):
        ax = axs[test_idx][cat_idx]
        
        category_data = df[df['race/ethnicity'] == category]
        pass_fail_counts = category_data['pass'].value_counts()
        
        sizes = [pass_fail_counts.get('passed', 0), pass_fail_counts.get('failed', 0)]
        labels = ['Passed', 'Failed']
        colors = ['#2ecc71', '#e74c3c']

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
               colors=colors, wedgeprops={'edgecolor': 'black'})
        
        if test_idx == 0:
            ax.set_title(category, fontsize=10, fontweight='bold')
        
        if cat_idx == 0:
            ax.text(0, 0, test.capitalize(), fontsize=12, fontweight='bold', color='darkblue',
                    verticalalignment='center', horizontalalignment='right', transform=ax.transAxes)

# Clean up
df.drop(columns='pass', inplace=True)
plt.suptitle("Pass vs Fail by race/ethnicity for Each Test", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[1, 0, 1, 0.96])
plt.show()


#_______________________________________________________________________________________________________
# Step 1: Group and sum the data
grouped = combined_tests.groupby(['race/ethnicity', 'pass'])['count'].sum().unstack(fill_value=0)

# Step 2: Calculate percentages
grouped['total'] = grouped['passed'] + grouped['failed']
grouped['pass_percent'] = (grouped['passed'] / grouped['total']) * 100
grouped['fail_percent'] = 100 - grouped['pass_percent']

# Step 3: Sort by pass % descending
grouped = grouped.sort_values(by='pass_percent', ascending=False)

# Step 4: Plot bar chart
plt.figure(figsize=(8, len(grouped) * 0.6))  # height based on number of education levels

bars_pass = plt.barh(grouped.index, grouped['pass_percent'], color='green', label='Passed')
bars_fail = plt.barh(grouped.index, grouped['fail_percent'], left=grouped['pass_percent'], color='red', label='Failed')

# Step 5: Add percentage labels to the bars
for i, (p, f) in enumerate(zip(grouped['pass_percent'], grouped['fail_percent'])):
    plt.text(p / 2, i, f'{p:.1f}%', va='center', ha='center', color='white', fontsize=10)
    plt.text(p + f / 2, i, f'{f:.1f}%', va='center', ha='center', color='white', fontsize=10)

# Final formatting
plt.xlabel('Percentage of Students')
plt.title('Student Performance by race/ethnicity')
plt.xlim(0, 100)
plt.gca().invert_yaxis()  # Best-performing at the top
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()
#_______________________________________________________________________________________________________