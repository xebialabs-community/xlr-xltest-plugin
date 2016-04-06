#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, ast, re
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

class XLTestViewClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpRequest(http_connection, username, password)

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return XLTestViewClient(http_connection, username, password)


    def cmp_version(self, version1, version2):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
        return cmp(normalize(version1), normalize(version2))

    def check_xltestview_version(self):
        xltestview_api_url = "/api/v1/info"
        info_response = self.http_request.get(xltestview_api_url, contentType='application/json')
        result = json.loads(info_response.getResponse())
        if self.cmp_version(result['version'],'1.4.0') < 0:
            print "Version %s not supported." % result['version']
            sys.exit(1)
        else:
            print "Version %s supported." % result['version']

    def get_project_id(self, project_name):
        # Fetch project information
        xltestview_api_url = "/api/v1/projects?title=%s" % project_name
        project_response = self.http_request.get(xltestview_api_url, contentType='application/json')
        data = json.loads(project_response.getResponse())
        if data is not None:
            for project in data:
                if project is not None and project['title'].startswith(project_name):
                    return project['id']
        return None


    def get_test_specification_id(self, test_specification_name, project_name):
        # Fetch test specification information
        project_id = self.get_project_id(project_name)
        xltestview_api_url = "/api/internal/projects/%s/testspecifications" % project_id
        test_specifications_response = self.http_request.get(xltestview_api_url, contentType='application/json')
        data = json.loads(test_specifications_response.getResponse())
        if data is not None:
            for test_spec in data:
                if test_spec is not None and test_spec['title'].startswith(test_specification_name):
                    return test_spec['name']
        return None

    def get_test_specification_qualification(self, test_specification_name, project_name):
        test_specification_id = self.get_test_specification_id(test_specification_name, project_name)
        xltestview_api_url = "/api/v1/qualifications?testSpecification=%s" % test_specification_id
        test_specification_response = self.http_request.get(xltestview_api_url, contentType='application/json')
        result = json.loads(test_specification_response.getResponse())
        if result['result']:
            print 'TestSpec %s qualified as PASSED' % test_specification_name
            return True
        else:
            print 'TestSpec %s qualified as FAILED' % test_specification_name
            print 'Reason: *%s*' % result['message']
            return False

    def is_test_specification_running(self, test_specification_name, project_name):
        # Checking and waiting until test is finished
        test_specification_id = self.get_test_specification_id(test_specification_name, project_name)
        xltestview_api_url = "/api/internal/projects/%s/status" % test_specification_id
        headers = {'Accept': 'text/event-stream', 'Content-Type': ''}
        test_specification_response = self.http_request.get(xltestview_api_url, headers = headers)
        if not test_specification_response.isSuccessful():
            raise Exception("Failed to get test specification state. Server return [%s], with content [%s]" % (test_specification_response.status, test_specification_response.response))
        if 'running' in test_specification_response.getResponse():
            print "Test Specification is running"
            return True
        else:
            print "Test Specification is not running"
            return False

    def execute_test_specification(self, test_specification_name, project_name):
        test_specification_id = self.get_test_specification_id(test_specification_name, project_name)
        xltestview_api_url = "/api/internal/execute/%s" % test_specification_id
        content = '{"id":"%s"}' % test_specification_id
        test_specification_response = self.http_request.post(xltestview_api_url, content, contentType='application/json')
        result = json.loads(test_specification_response.getResponse())
        return result['taskId']
