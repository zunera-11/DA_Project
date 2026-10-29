import pandas as pd 

def calculate_average(marks):
    return sum(marks)/len(marks)

n= int(input("enter number of students:"))

names=[]
marks=[]
for i in range(n):
    name =input("Enter student name :")
    mark=float(input("Eneter marks:"))

    names.append(name)
    marks.append(mark)

df= pd.DataFrame({
    "Names":names,
    "Marks":marks
})

def result(mark):
    if mark>=75:
        return "Distinction"
    elif mark>=50:
        return "Pass"
    else:
        return "Fail"

df["Result"]=df["Marks"].apply(result)

print("\n Dataset:")
print(df)

print("\n Student Analysis:")
for mark in marks:
    if mark>=75:
        print(mark,"Distinction")
    elif mark >=50:
        print(mark,"Pass")
    else:
        print("mark","Fail")

print("\n Average Marks :",calculate_average(marks))
print("Highest Marks:",max(marks))
print("Lowest Marks:",min(marks))