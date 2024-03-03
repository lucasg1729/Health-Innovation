from Execute_Function_Updated import execute, execute_all

###Takes in the CIK ID, location of master excel on computer, location of where the first excel would be saved, location of where the second excel would be saved
# execute(ID='1587143', master_location="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
#         newdata_location="/Users/lucasg17/Downloads/convertcsv.xlsx", newdata_copy_location="/Users/lucasg17/Downloads/convertcsv (1).xlsx")
# execute_all(ID_list=['1231756', '1865991', '1587143', '1346824'], master_loc="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
#         newdata_loc="/Users/lucasg17/Downloads/convertcsv.xlsx", newdata_copy_loc="/Users/lucasg17/Downloads/convertcsv (1).xlsx")
execute(ID='1587143', master_location="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
        newdata_location="/Users/lucasg17/Downloads/result.xlsx", newdata_copy_location="/Users/lucasg17/Downloads/result (1).xlsx")