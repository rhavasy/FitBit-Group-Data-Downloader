# Modified by Alyssa Woulfe to automate the authentication workflow
import fitbit
f=fitbit.FitBit()
auth_url, auth_token = f.GetRequestToken()
print """
Please open your web browser and copy the following URL to obtain your pin:
%s
""" %auth_url
PIN = raw_input("Please copy the pin that is returned from Fitbit: ")
access_token = f.GetAccessToken(PIN, auth_token)
apistring = f.PickApiCall() 
response = f.ApiCall(access_token, apistring)
print response #for debugging