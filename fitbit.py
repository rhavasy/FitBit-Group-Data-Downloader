"""
A Python library for accessing the FitBit API.

This library provides a wrapper to the FitBit API and does not provide storage of tokens or caching if that is required.

Most of the code has been adapted from: https://groups.google.com/group/fitbit-api/browse_thread/thread/0a45d0ebed3ebccb
"""
import httplib, time, ConfigParser, sys
import oauth2 as oauth

class FitBit():
    #Read global values from config file
    config = ConfigParser.RawConfigParser()
    try:
        cf=open('fitbit_config.ini')
    except IOError:
        sys.exit("Missing or corrupt fitbit_config.ini file in program path! Terminating execution.")
    config.readfp(cf)
    cf.close()
    APP_NAME = config.get('Globals', 'AppName')
    CONSUMER_KEY = config.get('Globals', 'ConsumerKey') 
    CONSUMER_SECRET = config.get('Globals', 'ConsumerSecret') 
    SERVER = config.get('Globals', 'Server')
    REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % SERVER 
    ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % SERVER 
    AUTHORIZATION_URL = 'http://%s/oauth/authorize' % SERVER
    TOKENFILENAME = config.get('FileData', 'OutputFilePrefix')
    
    def FetchResponse(self, oauth_request, connection, url): #added URL as config. parameter
        connection.request(oauth_request.method, url, headers=oauth_request.to_header()) #added headers to pass parameters
        response = connection.getresponse()
        s=response.read()
        return s
            
    def GetRequestToken(self): 
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, consumer, None)
        resp = self.FetchResponse(oauth_request, connection, self.REQUEST_TOKEN_URL) #passing in explicit url
        auth_token = oauth.Token.from_string(resp) 
        auth_url = "%s?oauth_token=%s" % (self.AUTHORIZATION_URL, auth_token.key) #build the URL
        return auth_url, auth_token
   
    def GetAccessToken(self, access_code, auth_token):
        oauth_verifier = access_code
        connection = httplib.HTTPSConnection(self.SERVER) 
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET) 
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, token=auth_token, http_url=self.ACCESS_TOKEN_URL, parameters={'oauth_verifier': oauth_verifier})
        oauth_request.sign_request(signature_method, consumer, auth_token)
        # now the token we get back is an access token
        access_token = oauth.Token.from_string(self.FetchResponse(oauth_request,connection, self.ACCESS_TOKEN_URL)) # parse the response into an OAuthToken object / passingin explicit url
        # store the access token when returning it
        access_token = access_token.to_string()
        return access_token
   
    def ApiCall(self, access_token, apiCall): #removed original hardcoded api call in favor of string passed from PickApiCall()
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        connection = httplib.HTTPSConnection(self.SERVER) 
        #build the access token from a string
        access_token = oauth.Token.from_string(access_token)
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        final_url = 'http://' + self.SERVER + apiCall
        oauth_request = oauth.Request.from_consumer_and_token(consumer, token=access_token, http_url=final_url)
        oauth_request.sign_request(signature_method, consumer, access_token)
        headers = oauth_request.to_header(realm='api.fitbit.com') 
        connection.request('GET', apiCall, headers=headers) 
        resp = connection.getresponse() 
        response = resp.read() 
        return response
    
    def PickApiCall(self):
        """Presents user with options and returns specific FitBit API string selected as a string. See FitBit API docs for specific call syntax."""      
        calls = ['/1/user/-/profile.xml', '/1/user/-/devices.xml', '/1/user/-/activities/steps/date/today/7d.xml', 'built dynamically'] # profile data, device data, last 7 days steps
        desc = ['User profile data.', 'Device data (incl. last upload).', 'Last 7 days\' steps.', 'Steps for specific date range.']
        for i in range(len(desc)):
            e = desc[i]
            print '%i. %s' % (i+1, e) # i+1 makes the list appear 1,2,3 to user rather than 0-based index 
        prompt = ""
        while True: #ensures integer is selected
            try:
                prompt = int(raw_input('Select an API call by number:'))
                if int(prompt) < 1 or int(prompt) > len(desc):
                    print 'Invalid selection. Last 7 days steps selected by default.'
                    prompt = 3 #if out of bounds default to last 7 days data
                break
            except ValueError:
                print 'Please select a valid number from the list. Try again ...'
        if prompt == 4: # Should change this to verify string rather than index in case list changes.
            while True:
                try: #Checks is string can be formatted as a time - ie is it in correct format
                    startdate = time.strptime(raw_input('Enter desired start date (mm/dd/yyyy): '), "%m/%d/%Y")
                    enddate = time.strptime(raw_input('Enter desired end date (mm/dd/yyyy): '), "%m/%d/%Y")
                    #THIS TEST REFORMATS startdate & enddate AS A struc_time OBJECT. MUST CONVERT BACK TO STRING FOR USE IN API CALL.
                    break
                except ValueError:
                    print 'Entered date does not match mm/dd/yyyy format. Try again.'
            apistring = '/1/user/-/activities/steps/date/' + time.strftime("%Y-%m-%d",startdate) + '/' + time.strftime("%Y-%m-%d",enddate) + '.xml' #time.strftime converts struc_time back to string in proper format
        else:
            apistring = calls[int(prompt)-1] # -1 brings the chosen base-1 index back to base-0 of list
        return apistring
