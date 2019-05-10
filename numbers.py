import csv

filename = 'C:/Users/tabbass/Desktop/New folder/in_mitel2.csv'
filename_2 = 'C:/Users/tabbass/Desktop/New folder/available.csv'

#Open and use the list of numbers (exported from mitel) in csv doc.
with open(filename, 'r') as f_obj:
    in_mitel2 = f_obj.readlines()

#Open and use the list of possible available numbers in csv doc.    
with open(filename_2, 'r') as f_obj:
    available = f_obj.readlines()


for in_mitel in in_mitel2:
    if in_mitel in available:
       print(in_mitel)