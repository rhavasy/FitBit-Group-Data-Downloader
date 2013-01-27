import fitbit, webbrowser, os, csv
f=fitbit.FitBit()

def MakeApiCall(token):
    apistring = f.PickApiCall()
    response = f.ApiCall(token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

mainfile='MGH_scholars_access_token.csv'
tmpfile='MGH_scholars_access_token.tmp.csv'
read_token=open(mainfile,'rt')
csvreader = csv.reader(read_token, dialect='excel', quotechar="'", delimiter=',')
accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
access_token = accesstokensfile.values()
NamesList = accesstokensfile.keys()
 
n=0
#fieldnames = ['value', 'access_token']
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
        access_token_new = f.GetAccessToken(PIN, auth_token) #need to trap a value error if pasted the wrong value
        csvwriter.writerow([value, access_token_new])
        print value
        print access_token_new
        MakeApiCall(access_token_new)
    n=n+1

write_token.flush()
write_token.close()
read_token.close()

i=0
mainfile_new = mainfile
while True :
    try:
        if mainfile == mainfile_new:
            os.remove(mainfile_new)
        os.rename(tmpfile,mainfile_new)
        if mainfile != mainfile_new:
            print "New file '" + mainfile_new + "' has been created!"
        break
    except WindowsError:
        if mainfile_new == mainfile:
            print "Unable to access file '" + mainfile_new + "', please make sure that this file is NOT open on your computer"
            choice = raw_input("Press 1 to retry access to '" + mainfile_new + "', or press any other key to write to a new file: ")
            if choice in ('1',''):
                continue
        mainfile_new = str(i) + '.' + mainfile
        i += 1
