"""This is a script that will take 2 files
 (in this care csv), compares each listed
 item, and printes the ones that are different.
 Put this script in a folder with the 2 files."""

import csv

ad_list = []
email_list = []

filename = 'C:/Users/tabbass/Desktop/New folder/otherusers.csv'
filename_2 = 'C:/Users/tabbass/Desktop/New folder/Users.csv'

otherusers = csv.reader(open(filename, 'r'))
users = csv.reader(open(filename_2, 'r'))

for user in otherusers:
    for u in user:
        ad_list.append(u)

for user1 in users:
    for l in user1:
        email_list.append(l)

print("Users who appear in both lists:")
for email in sorted(email_list):
    if email in ad_list:
        print(email)