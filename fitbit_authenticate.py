import fitbit, webbrowser, os, csv
f=fitbit.FitBit()

def MakeApiCall(token):
    apistring = f.PickApiCall()
    response = f.ApiCall(token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

mainfile= '%s.csv' % f.TOKENFILENAME #Read from .ini file by fitbit module
tmpfile= '%s.tmp.csv' % f.TOKENFILENAME
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
    FileName = value #this is where to test for blank access token.
    print value
    print access_token[n]
    try:
        MakeApiCall(access_token[n])
        csvwriter.writerow([value, access_token[n]]) 
    except ValueError:
        #print "Stored access token '" + access_token[n] + "' not accepted for user '" + value + "'"
        print "Stored access token %s not accepted for user %s. Reauthenticating. \n" % (access_token[n], value)
        auth_url, auth_token = f.GetRequestToken()
        webbrowser.open(auth_url)
        PIN = raw_input("\n Please paste the PIN that is returned from Fitbit [ENTER]: ")
        access_token_new = f.GetAccessToken(PIN, auth_token) #need to trap a value error if pasted the wrong value
        csvwriter.writerow([value, access_token_new])
        print "For user %s new access token = %s.\n" % (value, access_token_new)
        #print access_token_new
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
    except WindowsError: #this isn't a standard error - should build a better trap
        if mainfile_new == mainfile:
            print "Unable to access file '" + mainfile_new + "', please make sure that this file is NOT open on your computer"
            choice = raw_input("Press 1 to retry access to '" + mainfile_new + "', or press any other key to write to a new file: ")
            if choice in ('1',''):
                continue
        mainfile_new = str(i) + '.' + mainfile
        i += 1
