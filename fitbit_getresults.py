import fitbit, webbrowser, os.path, csv
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
    FileName = value
    print value
    access_token = accesstokensfile.values()
    MakeApiCall(access_token[n])
    n=n+1
    
    
#removed else statement for now since it is a one-time process. This new
#workflow assumes there will only be 1 files with access tokens.
