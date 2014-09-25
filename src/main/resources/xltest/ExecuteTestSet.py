#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

RESPONSE_STATUS_CODE = 200

if xltestServer is None:
    print "No server provided."
    sys.exit(1)

xltestUrl = xltestServer['url']

credentials = CredentialsFallback(xltestServer, username, password).getCredentials()
content = """{"testSetDefinition":"Configuration/TestSetDefinitions/%s","type":"%s","usedStores":[],"id":"","qualificationResult":true}
""" % (testSetDefinition, testSetType)

print "Sending content %s" % content

xltestAPIUrl = xltestUrl + '/test'

xltestResponse = XLRequest(xltestAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

pollingUri = None
uid = None
if xltestResponse.status == RESPONSE_STATUS_CODE:
    data = json.loads(xltestResponse.read())
    pollingUri = data["uri"]
    uid = data["id"]
    uid = uid.rpartition('/')[2]
    print "XLTest execution running on %s with uid: %s." % (pollingUri,uid)
else:
    print "Failed to execute test on XL Test"
    xltestResponse.errorDump()
    sys.exit(1)

# Checking and waiting until test is finished
running = True
while(running):
    xltestResponse = XLRequest(pollingUri, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()

    if xltestResponse.status == RESPONSE_STATUS_CODE:
        data = xltestResponse.read()
        if "event: close" in data:
            running = False
            print "XLTest execution finished on %s." % (pollingUri)
        else:
            time.sleep(2)
    else:
        print "Failed to execute test on XL Test"
        xltestResponse.errorDump()
        sys.exit(1)

# Check qualification result
xltestAPIUrl = xltestUrl + '/reports/' + uid + '/Configuration/Reports/qualification'

xltestResponse = XLRequest(xltestAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()
if xltestResponse.status == RESPONSE_STATUS_CODE:
    data = json.loads(xltestResponse.read())
    report = data["report"]
    uri = xltestUrl + "/#/testruns/" + uid
    if report is False:
        print "The test run is qualified as: FAILED."
        sys.exit(1)
    print "The test run is qualified as: PASSED."

else:
    print "Failed to execute test on XL Test"
    xltestResponse.errorDump()
    sys.exit(1)
