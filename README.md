FitBit Group Data Downloader
=============

A Python console application for FitBit data gathering. Includes the fitbit.py library with fitbit class module, which contains the necessary methods for completing the FitBit OAuth authentication and for querying the FitBit API. Also contains the fitbit_authenticate.py script which walks a user through the authentication and data retrieval process as outlined below.

# Heritage

Based on the fitbit.py library originally found at https://github.com/jplattel/FitBit.py.git and modified for Oauth2 use at https://github.com/jflasher/FitBit.py/blob/master/fitbit.py.

# Design
This script was designed to allow the retrieval of FitBit data for a list of users, outputting each user to an individual XML file. The script will work as well for a single user as for a whole list. We haven't tested the upper limit of users, though FitBot does enforce an API rate limit.

# Use

The fitbit.py library provides the necessary Oauth functions to complete the "Oauth Dance." This includes methods for retrieving request and access tokens. 
Fitbit_authenicate.py will allow a user to pick from a menu of FitBit API call options to generate an XML file of the output from the call. The script reads and
writes access tokens to a CSV file so that the API call can loop through a group of users to access Fitbit data.
 
**Note:** This library is designed to use FitBit's "desktop" app authentication using a PIN, rather than a callback URL. Therefore, the user will be required to manually visit the Authorize URL during the GetAccessToken sequence and manually add the PIN value obtained to the script.

## Basic Sequence of Events for Using fitbit_authenticate.py Script

1. Register an app with FitBit and obtain Cunsumer Key and Consumer Secret. **Note:** the app must be registered as a desktop app, not a web app.
2. Add the Consumer Key and Consumer secret values to the fitbit_config.ini file.
3. Create a CSV file with a single or list if names in the first column (no headings).
4. Complete the remaining configurations in the fitbit_config.ini file, by adding the name of the file you just created for the user names. You only need to put the file name prefix in the .ini file, not the file extension. The script will add the necessary extension to the name. For example, if you created a file called USERNAMES.csv, enter USERNAMES in the .ini file. It is critical that you ensure the file name you create matches the file prefix in the Config file.
5. The script is set to use the Excel dialect of CSV file. If you create a CSV file using any other tool, you may have to change the following line in fitbit_authenticate.py: ```python
csvreader = csv.reader(read_token, dialect='excel', quotechar="'", delimiter=',') ```
6. Install Oauth 2 (use easy_install, pip install, or installation tool of your choice).
7. Execute the fitbit_authenticate.py script which will:
	1. Prompt user to select if they would like to get the same data for all users and will present several FitBit API call options to select. 
	2. Check if an access token exists for a user or list of users from the CSV file.
	3. If yes, will make the API call and will write resulting data to a file called USERNAME_FILENAME.xml in the application directory.
	4. If no, will call GetRequestToken and obtain the Authorization URL and Authorization Token value via fitbit.py class module.
		1. Open the user's default web browser and require authentication to the FitBit authorization page.
		2. Request that the user paste the resulting PIN into the console.
		3. Call GetAccessToken using PIN and the Authorize Token. Write the resulting token to a temporary file in the application directory.
		4. Call APICall using the AccessToken obtained in step 4 and will write resulting data to a file called username_results.xml in the application directory.
	
#Known Issues
- There is no control over the order for which the script reads names and tokens from the CSV file
- Did not account for all errors occuring for obtaining the PIN.
- PIN appears to have 25 or 26 characters, but we have not accounted for all possibilities.

#Help

Modifications made by Rob Havasy, Alyssa Woulfe, and Ahnissa Beaupre at the Center for Connected Health, Boston, MA.
For help (best effort only) or information contact:

rhavasy@partners.org, awoulfe@partners.org, or abeaupre@partners.org

Center for Connected Health
25 New Chardon St.
Suite 300
Boston, MA 02114

http://www.connected-health.org/
