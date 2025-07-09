import pandas as pd

data = [
        ("Nurse",                       10,     10) ,
        ("Kindergarten Teacher",        10,     10) ,
        ("Flight Attendant",            10,     10) ,
        ("Administrative Assistant",    10,     9) ,
        ("Dental Hygienist",            12,     6),
        ("Social Worker",               9,      5) ,
        ("Speech Therapist",            10,     7) ,
        ("Librarian",                   10,     4) ,
        ("HR Specialist",               10,     5) ,
        ("Primary School Teacher",      10,     7) ,
        ("Construction Worker",         9,      0) ,
        ("Mechanical Engineer",         9,      0) ,
        ("Electrician",                 9,      0) ,
        ("Truck Driver",                11,     0) ,
        ("Software Developer",          10,     3) ,
        ("Welder",                      10,     0) ,
        ("Car Mechanic",                10,     1) ,
        ("Police Officer",              11,     3) ,
        ("Plumber",                     10,     0) ,
        ("Civil Engineer",              9,      2)
]

df_image2 = pd.DataFrame(data, columns=["job", "number_person", "number_female"])
df_image2["number_male"] = df_image2["number_person"] - df_image2["number_female"]
df_image2["percent_female"] = df_image2["number_female"]/df_image2["number_person"] *100
df_image2["percent_male"] = df_image2["number_male"]/df_image2["number_person"]*100
df_image2["source"] = 2