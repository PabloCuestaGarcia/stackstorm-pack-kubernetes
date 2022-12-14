import json

from lib.k8s import K8sClient


class CreateNamespace(K8sClient):

    def run(self, body, pretty=None, config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['params'] = {}

        if config_override is not None:
            args['config_override'] = config_override

        if body is not None:
            args['body'] = body
        else:
            return (False, "body is a required parameter")

        if pretty is not None:
            args['params'].update({'pretty': pretty})
        if 'body' in args:
            args['data'] = args['body']
            args.pop('body')
        args['headers'] = {
            'Content-type': u'application/json', 
            'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'
        }  # noqa pylint: disable=line-too-long

        args['url'] = "api/v1/namespaces".format(body=body)
        args['method'] = "post"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code

        try:
            myresp['data'] = json.loads(self.resp.content.rstrip())
        except ValueError:
            myresp['data'] = self.resp.content

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)
