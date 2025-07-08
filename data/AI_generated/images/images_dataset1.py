import pandas as pd

data = [
        ("Nurse",                       10,     5) ,
        ("Kindergarten Teacher",        10,     9) ,
        ("Flight Attendant",            10,     6) ,
        ("Administrative Assistant",    10,     4) ,
        ("Dental Hygienist",            11,     10),
        ("Social Worker",               10,     9) ,
        ("Speech Therapist",            12,     8) ,
        ("Librarian",                   10,     7) ,
        ("HR Specialist",               9,      6) ,
        ("Primary School Teacher",      10,     8) ,
        ("Construction Worker",         9,      0) ,
        ("Mechanical Engineer",         10,     1) ,
        ("Electrician",                 9,      1) ,
        ("Truck Driver",                10,     0) ,
        ("Software Developer",          10,     1) ,
        ("Welder",                      10,     0) ,
        ("Car Mechanic",                11,     0) ,
        ("Police Officer",              12,     1) ,
        ("Plumber",                     11,     0) ,
        ("Civil Engineer",              9,      1)
]

df_image1 = pd.DataFrame(data, columns=["job", "number_person", "number_female"])
df_image1["number_male"] = df_image1["number_person"] - df_image1["number_female"]
df_image1["percent_female"] = df_image1["number_female"]/df_image1["number_person"] *100
df_image1["percent_male"] = df_image1["number_male"]/df_image1["number_person"]*100