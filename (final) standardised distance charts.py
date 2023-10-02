#!/usr/bin/env python
# coding: utf-8

# #### In 2023, I was the analyst helping consult a client on their compensation structure. I was given a set of employees, their salaries, and the salary bands they were members of (labelled A, B, C, etc.). A band was made of the minimum possible salary an employee could have in it, the maximum, and the midpoint. Plan 1 was the set of salaries bands the firm originally had, plan 2 was what we proposed. I was asked to create a single visual showing where the employees moved before and after, relative to their min/mid/max. 
# #### 
# #### A z-score is typically used to normalise differing figures. That was not possible here since I only had the three min/mid/max figures as opposed to a mean and standard deviation needed for that. 
# #### 
# #### I calculated a score as distances from the min/mid/max. Min = 100%, mid = 200%, max = 300%. E.g., if a salary is 70, and the min is 100, then the score is 70%. Or if a salary is 400, the min is 200, and the mid is 600, then being halfway between min and mid makes a score of 150%.
# #### 
# #### The chart itself is derived from a candlestick chart used for stock prices, which I made to show blocks going from 100-200-300. 
# #### 
# #### The names, bands, and salaries in this document are fabricated and do not reflect that of any real persons or organisations.
# 

# In[1]:


import plotly.graph_objects as go
import pandas as pd

# this retrieves and stores the actual salary data of employees
salary_data = {"names" : [],
              "salaries" : [],
              "band_of_staffer" : [],
              "plan" : []}
df = pd.read_excel("salary_data.xlsx")


# for each employee, this adds in two duplicate rows, one for each plan
for i in range(len(df)):
    for j in range(2):
        salary_data["names"].append(df["names"][i])
        salary_data["salaries"].append(df["salaries"][i])
        salary_data["band_of_staffer"].append(df["band_of_staffer"][i])
        salary_data["plan"].append(f"plan {j + 1}")

       
# this retrieves and stores the salary bands that employees are subject to
band_data_plan_1 = {"band_of_policy" : [],
                    "min" : [],
                    "mid" : [],
                    "max" : []}
df = pd.read_excel("band_data_plan_1.xlsx")
band_data_plan_1["band_of_policy"] = [df["band_of_policy"][i] for i in range(len(df))]
band_data_plan_1["min"] = [df["min"][i] for i in range(len(df))]
band_data_plan_1["mid"] = [df["mid"][i] for i in range(len(df))]
band_data_plan_1["max"] = [df["max"][i] for i in range(len(df))]

band_data_plan_2 = {"band_of_policy" : [],
                    "min" : [],
                    "mid" : [],
                    "max" : []}
df = pd.read_excel("band_data_plan_2.xlsx")
band_data_plan_2["band_of_policy"] = [df["band_of_policy"][i] for i in range(len(df))]
band_data_plan_2["min"] = [df["min"][i] for i in range(len(df))]
band_data_plan_2["mid"] = [df["mid"][i] for i in range(len(df))]
band_data_plan_2["max"] = [df["max"][i] for i in range(len(df))]

    
# the positions of the employees on the charts are stored here
employee_scores = {"plan":[],
                   "name":[],
                   "only":[]}


# this loop calculates the score, i.e., the positioning of the employees on the charts
salary_data_index = 0
for i in salary_data["names"]:    

    band_data_index = 0
    
    if salary_data["plan"][salary_data_index] == "plan 1":
        band_data = band_data_plan_1
    else:
        band_data = band_data_plan_2
        
    # loops through the bands until it reaches the same as the current employee
    # so the correct band_data_index is identified    
    for j in band_data["band_of_policy"]:
        if band_data["band_of_policy"][band_data_index] == salary_data["band_of_staffer"][salary_data_index]:
            break
        band_data_index += 1
    
    # calculates score for figures above max
    if salary_data["salaries"][salary_data_index] >= band_data["max"][band_data_index]:
        score = salary_data["salaries"][salary_data_index] / band_data["max"][band_data_index]
        employee_scores["plan"].append(salary_data["plan"][salary_data_index])
        employee_scores["name"].append(salary_data["names"][salary_data_index])
        employee_scores["only"].append((score + 2) * 100)
  
    # calculates score for figures between mid and max
    elif salary_data["salaries"][salary_data_index] >= band_data["mid"][band_data_index]:
        diff = salary_data["salaries"][salary_data_index] - band_data["mid"][band_data_index]
        score = diff / (band_data["max"][band_data_index] - band_data["mid"][band_data_index])
        employee_scores["plan"].append(salary_data["plan"][salary_data_index])
        employee_scores["name"].append(salary_data["names"][salary_data_index])
        employee_scores["only"].append((score + 2) * 100)

    # calculates score for figures between min and mid 
    elif salary_data["salaries"][salary_data_index] >= band_data["min"][band_data_index]:
        diff = salary_data["salaries"][salary_data_index] - band_data["min"][band_data_index]
        score = diff / (band_data["mid"][band_data_index] - band_data["min"][band_data_index])
        employee_scores["plan"].append(salary_data["plan"][salary_data_index])
        employee_scores["name"].append(salary_data["names"][salary_data_index])
        employee_scores["only"].append((score + 1) * 100)   

    else: # calculates score for figures below min
        score = salary_data["salaries"][salary_data_index] / band_data["min"][band_data_index]
        employee_scores["plan"].append(salary_data["plan"][salary_data_index])
        employee_scores["name"].append(salary_data["names"][salary_data_index])
        employee_scores["only"].append((score * 100))
    
    salary_data_index += 1

# this draws the candlesticks from 100-300
data = {"plan":["plan 1","plan 1","plan 2","plan 2"],
        "max":[300,200,300,200],
        "min":[200,100,200,100]}
df = pd.DataFrame(data)
fig = go.Figure(data = [go.Candlestick(x = df['plan'],
                open = df['min'],
                high = df['max'],
                low = df['min'],
                close = df['max'],
                name = "min = 100, max = 300",
                increasing_line_color = "#4a5d6e",
                decreasing_line_color = "#4a5d6e",
                increasing_fillcolor = "#4a5d6e",
                decreasing_fillcolor = "#4a5d6e")])

# this marks the mid point by sketching a 1D candlestick to function as a line
x_axis = {"plan":["plan 1","plan 2"],
        "mid":[200,200],
        "name":["mid = 200","mid = 200"]}
for i in range(1,3):
    fig.add_trace(go.Candlestick(x = [f"plan {i}"],
                                 open = [200],
                                 high = [200],
                                 low = [200],
                                 close = [200],
                                 name = "mid = 200",
                                 increasing_line_color = '#77a1a2', 
                                 decreasing_line_color = '#77a1a2'))

# a line for each score
for i in range(len(employee_scores['plan'])):
    fig.add_trace(go.Candlestick(x = [employee_scores['plan'][i]],
                                 open = [employee_scores['only'][i]],
                                 high = [employee_scores['only'][i]],
                                 low = [employee_scores['only'][i]],
                                 close = [employee_scores['only'][i]],
                                 name = employee_scores['name'][i],
                                 increasing_line_color = '#C00000', 
                                 decreasing_line_color = '#C00000'))

# this generates the graph
fig.update_layout(
    xaxis_rangeslider_visible = False,
    title = 'Clays ltd.',
    titlefont = dict(family = "Work Sans", size = 30, color = "#77a1a2"),
    yaxis_title = 'Score',
    yaxis = dict(dtick = 10),
    xaxis_gridcolor = "#DDDDDD",
    yaxis_gridcolor = "#DDDDDD",
    plot_bgcolor = 'white')
            
fig.show()

