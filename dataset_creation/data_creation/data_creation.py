import os
import random

out_path = "out"
in_path = "input"
outfile = "data.csv"

names = list(open(os.path.join(in_path, "names.txt")))
surnames = list(open(os.path.join(in_path, "surnames.txt")))
birth_dates = list(open(os.path.join(in_path, "birthdates.txt")))
birth_places = list(open(os.path.join(in_path, "birthplaces.txt")))
issue_dates = list(open(os.path.join(in_path, "issue_date.txt")))

print(random.choice(names))
with open(os.path.join(out_path, outfile), "w") as csv_file:
    for i in range(1500):
        name_sex = random.choice(names).split(',')
        surname = random.choice(surnames).upper().strip()
        name = name_sex[0].upper().strip()
        cittadinanza = "ITALIANA"
        birth_date = random.choice(birth_dates).strip()
        sex = name_sex[1].upper().strip()
        issue_date = random.choice(issue_dates).strip()
        
        exp_date = issue_date.strip()
        splitted_exp_date = exp_date.split("/")
        year = splitted_exp_date[2]
        year = list(year)
        year[2] = str(int(year[2]) + 1)
        exp_date = splitted_exp_date[0] + "/" + splitted_exp_date[1] + "/" + ''.join(year)

        #list(exp_date.split("/")[2])[2] = str(int(list(issue_date.split("/")[2])[2]) + 1)
        #exp_date = str(exp_date)
        birth_place = random.choice(birth_places).upper().strip()

        csv_file.write(surname + "," + name + "," + cittadinanza + "," + birth_date + "," + sex + "," + issue_date + "," + exp_date + "," + birth_place + "\n")

