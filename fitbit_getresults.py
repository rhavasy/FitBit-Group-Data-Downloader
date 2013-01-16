import fitbit, webbrowser, os.path, csv
f=fitbit.FitBit()

def MakeApiCall(access_token):
    apistring = f.PickApiCall() 
    response = f.ApiCall(access_token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

import csv
csvreader = csv.reader(file('MGH_scholars_access_token.csv','r'), dialect='excel', quotechar="'", delimiter=',')
accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
Names = accesstokensfile.keys()
NamesList = Names
for values in NamesList:
    FileName = values
accesstokenslist = accesstokensfile.values()
TokensList= accesstokenslist
for values in TokensList:
    access_token = values

MakeApiCall(access_token)
    
    
#removed else statement for now since it is a one-time process. This new
#workflow assumes there will only be 1 files with access tokens.
