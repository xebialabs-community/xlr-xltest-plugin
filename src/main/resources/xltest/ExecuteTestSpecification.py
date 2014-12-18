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

def pollTestSpecificationRun(xltestUrl, taskId, credentials):
    # Checking and waiting until test is finished
    running = True
    uri = "%s/test/%s" % (xltestUrl,taskId)
    time.sleep(10)
    while(running):
        xltestResponse = XLRequest(uri, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()

        if xltestResponse.status == RESPONSE_STATUS_CODE:
            data = xltestResponse.read()
            if "event: close" in data:
                running = False
                print "XLTest execution finished on %s." % (uri)
                if "\"qualification\":false" in data:
                    print "The test run is qualified as: FAILED."
                    sys.exit(1)
                elif "\"qualification\":true" in data:
                    print "The test run is qualified as: PASSED."
                else:
                    print "Could not find qualification result"
                    sys.exit(1)
            else:
                time.sleep(2)
        else:
            print "Failed to execute test on XL Test"
            xltestResponse.errorDump()
            sys.exit(1)

def fetchTaskIdFromResponse(xltestResponse):
    data = json.loads(xltestResponse.read())
    taskId = data["taskId"]
    return taskId

if xltestServer is None:
    print "No server provided."
    sys.exit(1)

xltestUrl = xltestServer['url']

credentials = CredentialsFallback(xltestServer, username, password).getCredentials()

# Fetch test specification information
xltestAPIUrl = "%s/execute/%s" % (xltestUrl, testSpecificationName)
content = '{"id":"%s"}' % testSpecificationName
request = XLRequest(xltestAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json')
xltestResponse = request.send()
if xltestResponse.status == RESPONSE_SPECINFO_CODE:
    data = json.loads(xltestResponse.read())
    commandLine = data["commandLine"]
    parameters = data["parameters"]
elif xltestResponse.status == RESPONSE_STATUS_CODE:
    # If the specification has no params, it will be directly executed
    taskId = fetchTaskIdFromResponse(xltestResponse)
    print "XLTest execution running on %s with taskId: %s." % (xltestUrl,taskId)
    pollTestSpecificationRun(xltestUrl, taskId, credentials)
    sys.exit(0)
else:
    print "Failed to fetch test specification information from XL Test at url: '%s'" % request.uri
    xltestResponse.errorDump()
    sys.exit(1)

if command:
    commandLine = command

paramDict = {}
propertyDict = {}
if properties:
    propertyDict = dict(ast.literal_eval(properties))

for parameter in parameters:
    name = parameter["name"]
    value = parameter["value"]
    if name in propertyDict:
        value = propertyDict[name]
    paramDict[name] = value

xltestAPIUrl = "%s/execute/%s" % (xltestUrl, testSpecificationName)
content = '{"commandLine":%s,"parameters":%s}' % (json.dumps(commandLine), json.dumps(paramDict))
print content
xltestResponse = XLRequest(xltestAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

taskId = None
if xltestResponse.status == RESPONSE_STATUS_CODE:
    taskId = fetchTaskIdFromResponse(xltestResponse)
    print "XLTest execution running on %s with taskId: %s." % (xltestUrl,taskId)
else:
    print "Failed to execute test on XL Test"
    xltestResponse.errorDump()
    sys.exit(1)

pollTestSpecificationRun(xltestUrl, taskId, credentials)