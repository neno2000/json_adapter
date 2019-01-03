import json, requests, time
class Client():
    def __init__(self, sess, url, content, action, sso):
        self.url     =  url
        self.content =  content
        self.action     =  action
        self.session = sess
        self.responseCode = ""
        self.content = ""
        self.json_content = ""
        self.sso = sso
    # Create based on class name:
    def call(self, data, anvandare, foretag):
        #return eval(type + "()")
        if self.action == "GET":
            if self.sso:
                pass
                #make a connection to the server")

            else:
                #make a get request

                r = self.session.get(self.url)
                self.responseCode = r.status_code
                if str(self.responseCode) == "200":
                    self.json_content= json.loads(r.content)
        elif self.action == "POST":
            if self.sso:
                req_open3 = requests.session()  # creating 2 sessions as a post will be needed
                a = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=10, max_retries=3)
                req_open3.mount('http://sapbep.collectum-out.local:59600/foretag/start.html', a)
                req_open3.post('http://sapbep.collectum-out.local:59600/foretag/start.html', auth=(anvandare, 'Farao_98765432'))
                time.sleep(2)
                r = req_open3.post(self.url, data=data)
                self.responseCode = r.status_code
                if str(self.responseCode) == "200":
                    self.json_content = json.loads(r.content)
                req_open3.post('http://sapdep.collectum-out.local:52600/foretag/start.html')
            else:
                #make a post request
                r = self.session.post(self.url, data=data)
                self.responseCode = r.status_code
                if str(self.responseCode) == "200":
                     self.json_content = json.loads(r.content)
        elif self.action == "PUT":
            #make a put request
            pass
        else:
            pass

    def getResponseCode(self):
        return self.responseCode
    def getJsonContent(self):
        return self.jsonContent



