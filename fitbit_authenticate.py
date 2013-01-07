import fitbit
f=fitbit.FitBit()
PIN = 'vk8o91i4littme6aik65uermtu'

auth_url, auth_token = f.GetRequestToken()

access_token = f.GetAccessToken(PIN, auth_token)

response = f.ApiCall(access_token, apiCall='/1/user/-/activities/log/steps/date/today/7d.json')
