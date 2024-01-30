from Execute_Function import execute

###Takes in the CIK ID, location of master excel on computer, location of where the first excel would be saved, location of where the second excel would be saved
execute(ID='1346824', master_location="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
        newdata_location="/Users/lucasg17/Downloads/convertcsv.xlsx", newdata_copy_location="/Users/lucasg17/Downloads/convertcsv (1).xlsx")