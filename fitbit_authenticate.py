import fitbit, webbrowser, os.path, os, csv
f=fitbit.FitBit()



def MakeApiCall(access_token):
    apistring = f.PickApiCall()
    response = f.ApiCall(access_token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

mainfile='MGH_scholars_access_token.csv'
tmpfile='MGH_scholars_access_token.tmp.csv'
read_token=open(mainfile,'r')
csvreader = csv.reader(read_token, dialect='excel', quotechar="'", delimiter=',')
accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
access_token = accesstokensfile.values()
NamesList = accesstokensfile.keys()
 
n=0
fieldnames = ['value', 'access_token']
write_token = open(tmpfile, 'wb')
csvwriter = csv.writer(write_token)
for value in NamesList:
    FileName = value
    print value
    print access_token[n]
    try:
        MakeApiCall(access_token[n])
        csvwriter.writerow([value, access_token[n]]) 
    except ValueError:
        print "Stored access token '" + access_token[n] + "' not accepted for user '" + value + "'"
        auth_url, auth_token = f.GetRequestToken()
        webbrowser.open(auth_url)
        PIN = raw_input("Please paste the PIN that is returned from Fitbit [ENTER]: ")
        access_token = f.GetAccessToken(PIN, auth_token)
        csvwriter.writerow([value, access_token])
        print value
        print access_token
        MakeApiCall(access_token)
    n=n+1

write_token.flush()
write_token.close()
read_token.close()
os.remove(mainfile)
os.rename(tmpfile,mainfile)
