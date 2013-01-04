# Basic loop to allow user to choose from several FitBit API calls at the command line
# Should be merged into the ultimate final script and it's output passed to the FitBit ApiCall routine.
DEBUG = False

calls = ['/1/user/-/profile.xml', '/1/user/-/devices.xml', '/1/user/-/activities/steps/date/today/7d.xml'] # profile data, device data, last 7 days steps
desc = ['User profile data.', 'Device data (incl. last upload).', 'Last 7 days\' steps.']

if DEBUG:
    print 'Call =  %s. Description: %s' % (calls[0], desc[0])

for i in range(len(desc)):
    e = desc[i]
    print '%i. %s' % (i+1, e)
   
prompt = raw_input('Select an API call by number:')

if DEBUG:
    print calls[int(prompt)-1]

#return the string from the calls list.