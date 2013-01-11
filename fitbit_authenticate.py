# Modified by Alyssa Woulfe to automate the authentication workflow & add file ops
# Mod by Rob Havasy to test for file existence
import fitbit, webbrowser, os.path
f=fitbit.FitBit()

def MakeApiCall(access_token):
    apistring = f.PickApiCall() 
    response = f.ApiCall(access_token, apistring)
    print response #for debugging
    file=open('results.xml', 'w') #Write results to file
    file.write(response)
    file.close()

Name = 'Alyssa'

if os.path.isfile(Name+'access_token.txt'): #First check if file exists
    file = open(Name+'access_token.txt', 'r') #If yes, read token from file
    access_token=file.read()
    file.close()
    MakeApiCall(access_token) #Call for data

else: #Otherwise, do Oauth dance and reauthenticate
    auth_url, auth_token = f.GetRequestToken()
    webbrowser.open(auth_url)
    PIN = raw_input("Please paste the PIN that is returned from Fitbit [ENTER]: ")
    access_token = f.GetAccessToken(PIN, auth_token)
    file = open(Name+' access_token.txt', 'w') #write token to file
    file.write(access_token)
    file.close()
    MakeApiCall(access_token)

from xml.etree import ElementTree
with open('results.xml', 'rt') as f:
        tree = ElementTree.parse(f)
for node in tree.iter('user'):
    name = node.attrib.get('fullname')
    print name

