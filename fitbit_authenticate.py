import fitbit
import webbrowser
import os
import csv

f=fitbit.FitBit()

def MakeApiCall(token, apistring):
    if apistring is None:
        apistring = f.PickApiCall()
    response = f.ApiCall(token, apistring)
    fo=open(FileName+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

def Reauthenticate(bad_token, name):
    """Called if the currently stored token is not accepted for a user OR if token is missing. Receives the old token which may be null and the user name. Returns new valid token."""
    print "Stored access token %s not accepted for user %s. Reauthenticating. \n" % (bad_token, name)
    auth_url, auth_token = f.GetRequestToken()
    webbrowser.open(auth_url)
    PIN = raw_input("\n Please paste the PIN that is returned from Fitbit [ENTER]: ")
    #if the PIN is not 26 characters, prompt user - in testing all PINs have been 25 or 26 characters
    if len(PIN) < 25:
        PIN = raw_input("\n Please confirm that you have entered the correct PIN returned from the Fitbit website and repaste here.[ENTER]: ")
    try:
        access_token_new = f.GetAccessToken(PIN, auth_token) #This traps error if PIN isn't pasted correctly. In testing some users typed a number & hit ENTER and bad PIN caused error.
    except ValueError:
        Reauthenticate(bad_token, name) #If bad PIN try again
    return access_token_new

mainfile= '%s.csv' % f.TOKENFILENAME #Read from .ini file by fitbit module
tmpfile= '%s.tmp.csv' % f.TOKENFILENAME
read_token=open(mainfile,'rU')
csvreader = csv.reader(read_token, dialect='excel', quotechar="'", delimiter=',')
try:
    accesstokensfile = {rows[0]:rows[1] for rows in csvreader}
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
except OSError:
    ## Do nothing - if the tmp file doesn't exist we are happy
    pass

reportselection = ['Yes', 'No']
for i in range(len(reportselection)):
    e = reportselection[i]
    print '%i. %s' % (i+1, e)
prompt = ""
while True:
    try:
        prompt = int(raw_input('\n Would you like to get the same data report for all users? \n Please select 1 for Yes or 2 for No: '))
        if int(prompt) < 1 or int(prompt) > len(reportselection):
            print '\n Invalid selection. Yes is selected by default.'
            prompt = 1
        break
    except ValueError:
        print '\n Please select a valid response. Try again... \n'
if prompt == 1:
    print '\n Which report would you like to get for all users on your list? \n'
    APISTRING = f.PickApiCall()
if prompt == 2:
    APISTRING = None
 
n=0
#fieldnames = ['value', 'access_token']
write_token = open(tmpfile, 'wb')
csvwriter = csv.writer(write_token)
for value in NamesList:
    FileName = value
    print value
    print access_token[n] #this is where to test for blank access token. If blank reauthenticate before throwing error.
    try:
        MakeApiCall(access_token[n], APISTRING)
        csvwriter.writerow([value, access_token[n]]) 
    except ValueError:
        new_token = Reauthenticate(access_token[n], value)
        print "For user %s new access token = %s." % (value, new_token)
        MakeApiCall(new_token, APISTRING)
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
    except OSError:
        if mainfile_new == mainfile:
            print "Unable to access file '" + mainfile_new + "', please make sure that this file is NOT open on your computer"
            choice = raw_input("Press 1 to retry access to '" + mainfile_new + "', or press any other key to write to a new file: ")
            if choice in ('1',''):
                continue
        mainfile_new = str(i) + '.' + mainfile
        i += 1
