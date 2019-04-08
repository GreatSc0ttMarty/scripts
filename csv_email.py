import csv
import re

email_list = []
part_two = []

filename = 'C:/Users/tabbass/Desktop/fefa.csv'
filename_2 = 'C:/Users/tabbass/Desktop/blacklist.txt'

inputfile = csv.reader(open(filename, 'r'))

for email in inputfile:
    email_list.append(email[0])

for emails in email_list:
    part_two.append(emails.split("@"))

number = int(len(part_two))
count = 0
email_list = []
while number != count:
    email_list.append(part_two[count][1])
    count += 1
    
part_two = []
for emails in email_list:
    part_two.append(emails.split(";"))

number = int(len(part_two))
count = 0
email_list = []
while count != number:
    email_list.append(part_two[count][0])
    count += 1

new_list = []
for email in email_list:
    new_list.append("*@" + email)

with open(filename_2,'w') as file:
    for new in new_list:
        file.write(new)
        file.write('\n')

for new in new_list:
    print(new)
