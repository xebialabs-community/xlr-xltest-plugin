#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time, urllib
import ast
import com.xhaus.jyson.JysonCodec as json

RESPONSE_STATUS_CODE = 200
RESPONSE_SPECINFO_CODE = 422

if xltestServer is None:
    print "No server provided."
    sys.exit(1)

xltestUrl = xltestServer['url']

credentials = CredentialsFallback(xltestServer, username, password).getCredentials()

# Fetch test specification information
xltestAPIUrl = "%s/api/internal/testspecifications" % (xltestUrl)
#content = '{"id":"%s"}' % testSpecificationName
request = XLRequest(xltestAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json')
xltestResponse = request.send()
if xltestResponse.status == RESPONSE_STATUS_CODE:
    # Got a good response
    data = json.loads(xltestResponse.read())
    if data is not None:
        for testSpec in data:
            print testSpec['name']
            if testSpec is not None and testSpec['name'].startswith(testSpecificationName):
                if testSpec['result']:
                    print 'TestSpec %s qualified as PASSED' % testSpecificationName
                    sys.exit(0)
                else:
                    print 'TestSpec %s qualified as FAILED' % testSpecificationName
                    sys.exit(1)
        print 'TestSpec %s not found' % testSpecificationName
        sys.exit(1)

print 'XL Test did not return data'
sys.exit(1)
