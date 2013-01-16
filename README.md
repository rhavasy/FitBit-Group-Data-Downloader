fitbit-python
=============

Python console application for FitBit data gathering. Includes the fitbit.py library with the fitbit class module which contains the necessary methods for completing the FitBit OAuth authentication, as well as methods for querying the FitBit API. Also contains the fitbit_authenticate.py script which walks a user through the authentication and data retreival process as outlined below.

# Heritage

Based on the fitbit.py library originally found at https://github.com/jplattel/FitBit.py.git and modified for Oauth2 use at https://github.com/jflasher/FitBit.py/blob/master/fitbit.py.

# Use

The fitbit.py library provides the necessary Oauth functions to complete the "Oauth Dance." This includes methods for retreiving the request and access tokens.

*Note:* This library is designed to use FitBit's "desktop" app authentication using a PIN, rather than a callback URL. Therefore, the user will be required to manually visit the Authorize URL during the GetAccessToken part and manually add the PIN value obtained to the script.

## Basic Sequence of Events for Using fitbit_authenticate.py Script

1. Register an app with FitBit and obtain Cunsumer Key and Consumer Secret.
2. Add the Consumer Key and Consumer Secret values to the fitbit.py library in the appropriate place near the top of the file.
3. Execute the fitbit_authenticate.py script which will:
	1. Check if a file called username_access_token.txt exists in the application directory.
	2. If yes, will prompt user to select one of several FitBit API calls and will write resulting data to a file called username_results.xml in the application directory.
	3. If no, will call GetRequestToken and obtain the Authorization URL and Authorization Token value via fitbit.py class module.
	4. Open the user's default web browser and require authentication to the FitBit authorization page.
	5. Request that the user paste the resulting PIN into the console.
	6. Call GetAccessToken using PIN and the Authorize Token obtained in step 3. Write the resulting token to the username_access_token.txt file in the application directory.
	7. Call APICall using the AccessToken obtained in step 6 and will write resulting data to a file called username_results.xml in the application directory.
	
#Known Issues

fitbit_authenticate.py currently checks only for the presence of an access_token.txt file in the application path. If a file exists, it assumes that the token is valid. There is currently no error handling for an invalid token.

#Help

Modifications made by Rob Havasy and Alyssa Woulfe at the Center for Connected Health, Boston, MA.
For help (best effort only) or information contact:

rhavasy@partners.org
awoulfe@partners.org

Center for Connected Health
25 New Chardon St.
Suite 300
Boston, MA 02114
http://www.connected-health.org/

