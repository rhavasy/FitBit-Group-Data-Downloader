fitbit-python
=============

Python desktop client for FitBit data gathering.

# Heritage

A desktop client application, written in Python, for retreiving data from the FitBit API. Based on the fitbit.py library originally found at https://github.com/jplattel/FitBit.py.git and modified for Oauth2 use at https://github.com/jflasher/FitBit.py/blob/master/fitbit.py.

# Use

The fitbit.py library provides the necessary Oauth functions to complete the "Oauth Dance." This includes methids for retreiving the request and access tokens.

*Note:* This library is designed to use FitBit's "desktop" app authentication using a PIN, rather than a callback URL. Therefore, the user will be required to manually visit the Authorize URL during the GetAccessToken part and manually add the PIN value obtained to the script.

## Basic Sequence of Events

1. Register an app with FitBit and obtain Cunsumer Key and Consumer Secret.
2. Add the Consumer Key and Consumer Secret values to the fitbit.py library in the appropriate place.
3. Call GetRequestToken and obtain the Authorization URL and Authorization Token value.
4. Manually go to Authorize URL and obtain PIN.
5. Copy PIN into script.
6. Call GetAccessToken using PIN and the Authorize Token obtained in step 3.
7. Call APICall using the AccessToken obtained in step 6.

The fitbit-authenticate.py script contains the basic steps outlined above.