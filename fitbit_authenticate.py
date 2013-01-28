import fitbit, webbrowser, os, csv
f=fitbit.FitBit()

def MakeApiCall(token):
    apistring = f.PickApiCall()
    response = f.ApiCall(token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

def Reauthenticate(access_token, name):
    print "Stored access token %s not accepted for user %s. Reauthenticating. \n" % (access_token, name)
    auth_url, auth_token = f.GetRequestToken()
    webbrowser.open(auth_url)
    PIN = raw_input("\n Please paste the PIN that is returned from Fitbit [ENTER]: ")
    #if the PIN is not 26 characters, prompt user
    if len(PIN) != 26:
        PIN = raw_input("\n Please confirm that you have entered the correct PIN returned from the Fitbit website and repaste here.[ENTER]: ")
    elif len(PIN)== 26:
        return PIN
    try:
        access_token_new = f.GetAccessToken(PIN, auth_token)
    except ValueError:
        Reauthenticate(access_token, value)
    return access_token_new

mainfile= '%s.csv' % f.TOKENFILENAME #Read from .ini file by fitbit module
tmpfile= '%s.tmp.csv' % f.TOKENFILENAME
read_token=open(mainfile,'rU')
csvreader = csv.reader(read_token, dialect='excel', quotechar="'", delimiter=',')
try:
    accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
    print 'ok'
except IndexError:
    ## Need to file read position or else we miss the first input
    read_token.seek(0)
    accesstokensfile = {rows[0]:rows[0] for rows in csvreader}
    ## Assign blank values to all missing keys
    for key in accesstokensfile.keys():
        accesstokensfile[key] = ''
NamesList = accesstokensfile.keys()
access_token = accesstokensfile.values()
## Remove temporary csv file if it exists
try:
    os.remove(tmpfile)
except WindowsError:
    ## Do nothing - if the tmp file doesn't exist we are happy
    pass
 
n=0
#fieldnames = ['value', 'access_token']
write_token = open(tmpfile, 'wb')
csvwriter = csv.writer(write_token)
for value in NamesList:
    FileName = value
    print value
    print access_token[n] #this is where to test for blank access token. If blank reauthenticate before throwing error.
    try:
        MakeApiCall(access_token[n])
        csvwriter.writerow([value, access_token[n]]) 
    except ValueError:
        new_token = Reauthenticate(access_token[n], value)
        print "For user %s new access token = %s.\n Select data again. \n" % (value, new_token)
        MakeApiCall(new_token)
        csvwriter.writerow([value, new_token])
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
