import json, requests, time
from configColl.Init import Init
class Client():
    def __init__(self, sess, url, content, action, env, sso):
        self.url     =  url
        self.content =  content
        self.action     =  action
        self.session = sess
        self.responseCode = ""
        self.content = ""
        self.json_content = ""
        self.sso = sso
        self.env = env
    # Create based on class name:
    def call(self, data, anvandare, foretag):
        #return eval(type + "()")
        ####################START Getting the configuration######################
        initiator = Init("config.ini", self.env)
        initiator.load()
        loginvar = initiator.getloginvar()
#        req_open.post(loginvar[0], auth=(loginvar[1], loginvar[2]))
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
                req_open3.mount(loginvar[0], a)
                print("Ernesto")
                print(loginvar[0])
                req_open3.post(loginvar[0], auth=(loginvar[1], loginvar[2]))
                time.sleep(2)
                r = req_open3.post(self.url, data=data)
                self.responseCode = r.status_code
                if str(self.responseCode) == "200":
                    self.json_content = json.loads(r.content)
                req_open3.post(loginvar[0])

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
