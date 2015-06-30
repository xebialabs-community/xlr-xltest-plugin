#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from xltestview.XLTestViewClient import XLTestViewClient


class XLTestViewClientUtil(object):

    @staticmethod
    def create_XL_TestView_client(container, username, password):
        client = XLTestViewClient.create_client(container, username, password)
        return client