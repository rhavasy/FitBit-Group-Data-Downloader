# Modified by Robert Havasy
# updated oauth to oauth2 based on https://github.com/jflasher/FitBit.py/blob/master/fitbit.py
"""
A Python library for accessing the FitBit API.

This library provides a wrapper to the FitBit API and does not provide storage of tokens or caching if that is required.

Most of the code has been adapted from: https://groups.google.com/group/fitbit-api/browse_thread/thread/0a45d0ebed3ebccb
"""
import os, httplib #was httplib
import oauth2 as oauth # was: from oauth import oauth


# pass oauth request to server (use httplib.connection passed in as param) 
# return response as a string 
class FitBit():
    # Application = 'CCH Data Feed'
    CONSUMER_KEY    = 'e52e981a10014a74893a1f4c2c8bb987' 
    CONSUMER_SECRET = '5cd1c526c6c348b79b76816e96034410' 
    SERVER = 'api.fitbit.com' 
    REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % SERVER 
    ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % SERVER 
    AUTHORIZATION_URL = 'http://%s/oauth/authorize' % SERVER 
    DEBUG = True
    
    def FetchResponse(self, oauth_request, connection, debug=DEBUG): 
        url = oauth_request.to_url() 
        connection.request(oauth_request.method,url) 
        response = connection.getresponse() 
        s=response.read() 
        if debug: 
            print 'requested URL: %s' % url 
            print 'server response: %s' % s 
        return s
   
    def GetRequestToken(self): 
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, consumer, None) 

        resp = self.FetchResponse(oauth_request, connection) 
        auth_token = oauth.Token.from_string(resp) 

        #build the URL
        authkey = str(auth_token.key) 
        authsecret = str(auth_token.secret) 
        auth_url = "%s?oauth_token=%s" % (self.AUTHORIZATION_URL, auth_token.key)
        print auth_url
        return auth_url, auth_token
   
    def GetAccessToken(self, access_code, auth_token):
        oauth_verifier = access_code
        connection = httplib.HTTPSConnection(self.SERVER) 
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET) 
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, token=auth_token, http_url=self.ACCESS_TOKEN_URL, parameters={'oauth_verifier': oauth_verifier})
        oauth_request.sign_request(signature_method, consumer, auth_token)
        # now the token we get back is an access token
        # parse the response into an OAuthToken object
        access_token = oauth.Token.from_string(self.FetchResponse(oauth_request,connection))
   
        # store the access token when returning it
        access_token = access_token.to_string()
        return access_token
   
    def ApiCall(self, access_token, apiCall='/1/user/-/profile.json'):
        #other API Calls possible, or read the FitBit documentation for the full list.
        #apiCall = '/1/user/-/devices.json' 
        #apiCall = '/1/user/-/profile.json' 
        #apiCall = '/1/user/-/activities/date/2011-06-17.json'
        
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
        json = resp.read() 
        return json
    
    def PickApiCall():
        """Presents user with options and returns specific FitBit API string selected as a string."""      
        # Add possible FitBit API call examples
        
        calls = ['/1/user/-/profile.xml', '/1/user/-/devices.xml', '/1/user/-/activities/steps/date/today/7d.xml'] # profile data, device data, last 7 days steps
        desc = ['User profile data.', 'Device data (incl. last upload).', 'Last 7 days\' steps.']
        
        if DEBUG:
            print 'Call =  %s. Description: %s' % (calls[0], desc[0])
        
        for i in range(len(desc)):
            e = desc[i]
            print '%i. %s' % (i+1, e) # i+1 makes the list appear 1,2,3 to user rather than o-based index 
        prompt = raw_input('Select an API call by number:')
        apistring = calls[int(prompt)-1] # -1 brings the chosen base-1 index back to base-0 of list
        
        if DEBUG:
            print apistring
        
        return apistring
