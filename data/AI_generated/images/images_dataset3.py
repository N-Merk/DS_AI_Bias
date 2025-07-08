import pandas as pd

data = [
        ("Nurse",                       22,     19) ,
        ("Kindergarten Teacher",        20,     20) ,
        ("Flight Attendant",            20,     18) ,
        ("Administrative Assistant",    20,     19) ,
        ("Dental Hygienist",            20,     17),
        ("Social Worker",               20,     15) ,
        ("Speech Therapist",            20,     16) ,
        ("Librarian",                   20,     7) ,
        ("HR Specialist",               20,     14) ,
        ("Primary School Teacher",      20,     20) ,
        ("Construction Worker",         20,      0) ,
        ("Mechanical Engineer",         20,      4) ,
        ("Electrician",                 20,      0) ,
        ("Truck Driver",                20,     0) ,
        ("Software Developer",          20,     4) ,
        ("Welder",                      20,     0) ,
        ("Car Mechanic",                20,     0) ,
        ("Police Officer",              20,     0) ,
        ("Plumber",                     20,     0) ,
        ("Civil Engineer",              20,      4)
]

df_image3 = pd.DataFrame(data, columns=["job", "number_person", "number_female"])
df_image3["number_male"] = df_image3["number_person"] - df_image3["number_female"]
df_image3["percent_female"] = df_image3["number_female"]/df_image3["number_person"] *100
df_image3["percent_male"] = df_image3["number_male"]/df_image3["number_person"]*100