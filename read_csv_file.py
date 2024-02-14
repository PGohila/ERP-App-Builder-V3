excel_file_path='/media/ram/01D8F5B271022760/RamWorking/AppBuilder/ERPprojectfiles/Screenslist.csv'
with open(file=excel_file_path,mode='r') as excel_file:
    print('excel file',excel_file)
    csv_read = excel_file.read()
    # print('csv_read ',csv_read)

# split csv file in line
line = csv_read.split('\n')
print('line ',line)
i=0
for line in line:
    print(line)
    print('*****')
    if i ==50:
        break
    i+=1