# Modified by Alyssa Woulfe to automate the authentication workflow
import fitbit, webbrowser
f=fitbit.FitBit()
auth_url, auth_token = f.GetRequestToken()
webbrowser.open(auth_url)
PIN = raw_input("Please paste the PIN that is returned from Fitbit [ENTER]: ")
access_token = f.GetAccessToken(PIN, auth_token)
apistring = f.PickApiCall() 
response = f.ApiCall(access_token, apistring)
print response #for debugging
