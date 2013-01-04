import fitbit
f=fitbit.FitBit()
PIN = 'pr8f78a3msncolh3lo8g86jqbv'

auth_url, auth_token = f.GetRequestToken()

access_token = f.GetAccessToken(PIN, auth_token)

response = f.ApiCall(access_token, apiCall='/1/user/-/activities/log/steps/date/today/7d.json')
