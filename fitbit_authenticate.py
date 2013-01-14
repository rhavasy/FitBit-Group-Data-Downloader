import fitbit, webbrowser, os.path
f=fitbit.FitBit()
response = ""
Name = 'Alyssa'

def MakeApiCall(access_token):
    apistring = f.PickApiCall() 
    response = f.ApiCall(access_token, apistring)
    fo=open(Name+'_results.xml', 'w') #Write results to file
    fo.write(response)
    fo.close()

if os.path.isfile(Name+'_access_token.txt'): #First check if file exists
    fo = open(Name+'_access_token.txt', 'r') #If yes, read token from file
    access_token=fo.read()
    fo.close()
    MakeApiCall(access_token) #Call for data
else: #Otherwise, do Oauth dance and reauthenticate
    auth_url, auth_token = f.GetRequestToken()
    webbrowser.open(auth_url)
    PIN = raw_input("Please paste the PIN that is returned from Fitbit [ENTER]: ")
    access_token = f.GetAccessToken(PIN, auth_token)
    fo = open(Name+'_access_token.txt', 'w') #write token to file
    fo.write(access_token)
    fo.close()
    MakeApiCall(access_token)

from xml.etree import ElementTree
with open(Name+'_results.xml', 'rt') as fo:
        tree = ElementTree.parse(fo)
for node in tree.iter('user'):
    name = node.attrib.get('fullname')
    print name