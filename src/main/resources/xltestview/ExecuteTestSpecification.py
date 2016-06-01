#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time
from xltestview.XLTestViewClientUtil import XLTestViewClientUtil

if xltestServer is None:
    print "No server provided."
    sys.exit(1)

xlt_client = XLTestViewClientUtil.create_XL_TestView_client(xltestServer, username, password)

xlt_client.check_xltestview_version()

task_id = xlt_client.execute_test_specification(testSpecificationName, projectName)

# Polling
time.sleep(10)
while xlt_client.is_test_specification_running(testSpecificationName, projectName):
    time.sleep(10)

qualification = xlt_client.get_test_specification_qualification(testSpecificationName, projectName)

if qualification:
    sys.exit(0)
else:
    sys.exit(1)