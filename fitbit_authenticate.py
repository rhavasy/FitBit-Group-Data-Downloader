# Modified by Alyssa Woulfe to automate the authentication workflow


import fitbit
f=fitbit.FitBit()

auth_url, auth_token = f.GetRequestToken()

print 'Please open your web browser and go to the copy the following URL to obtain your pin: %s' %auth_url

PIN = raw_input("Please copy the pin that is returned from Fitbit: ")

access_token = f.GetAccessToken(PIN, auth_token)

response = f.ApiCall(access_token, apiCall='/1/user/-/activities/log/steps/date/today/7d.json')
print response
