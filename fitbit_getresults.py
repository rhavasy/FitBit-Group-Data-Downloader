import fitbit, csv
f=fitbit.FitBit()

def MakeApiCall(access_token):
    apistring = f.PickApiCall() 
    response = f.ApiCall(access_token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

csvreader = csv.reader(file('MGH_scholars_access_token.csv','r'), dialect='excel', quotechar="'", delimiter=',')
accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
NamesList = accesstokensfile.keys()
n=0
for value in NamesList:
    FileName = NamesList[n]
    print value
    access_token = accesstokensfile.values()
    print access_token[n]    
    MakeApiCall(access_token[n])
    n=n+1