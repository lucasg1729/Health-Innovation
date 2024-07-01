from Execute_Function import execute, execute_all
from Exit_dates import write_excel

###Takes in the CIK ID, location of master excel on computer, location of where the first excel would be saved, location of where the second excel would be saved
# execute(ID='1587143', master_location="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
#         newdata_location="/Users/lucasg17/Downloads/convertcsv.xlsx", newdata_copy_location="/Users/lucasg17/Downloads/convertcsv (1).xlsx")
execute_all(ID_list=['1231756', '1865991', '1587143', '1346824'], 
            master_loc="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
            newdata_loc="/Users/lucasg17/Downloads/convertcsv.xlsx", 
            newdata_copy_loc="/Users/lucasg17/Downloads/convertcsv (1).xlsx")
# write_excel(raw_data="/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx", 
#             excel_path='/Users/lucasg17/Documents/GitHub/Health-Innovation/Testing.xlsx', 
#             raw_sheet='SV Health Investors, LLC', 
#             new_sheet='Master_SV1', 
#             start_col=1)