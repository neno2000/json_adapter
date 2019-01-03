import configparser, os, sys
import sqlite3, shutil
import win32crypt #https://sourceforge.net/projects/pywin32/
class Init:
    def __init__(self, initFile, enviroment ):
        self.initFile = initFile
        self.enviroment = enviroment
        self.config = configparser.RawConfigParser()
    def _prepareParams(self, urlParams, param1, param2):
        varSub1 = '<anvandare>'
        varSub2 = '<foretag>'
        if param1 != '' and param2 != '':
            subUrl = urlParams.replace(varSub1, param1)
            urlParams = subUrl.replace(varSub2, param2)
            return urlParams
        elif param1 != '' and param2 == '':
            subUrl = urlParams.replace(varSub1, param1)
            return subUrl
        elif param2 != '' and param1 == '':
            subUrl = urlParams.replace(varSub2, param2)
            return subUrl

    def load(self):
        self.config.read(os.path.join(sys.path[0], self.initFile))

    def getloginvar(self):
        if self.enviroment == "DEP":

            url = self.config.get('COMMON_DEP', 'login_url')
            login = self.config.get('COMMON_DEP', 'sso_username')
            passw = self.config.get('COMMON_DEP', 'sso_password')

            param =(url, login, passw)
            return param

        elif self.enviroment == "BEP":
            url = self.config.get('COMMON_BEP', 'login_url')
            login = self.config.get('COMMON_BEP', 'sso_username')
            passw = self.config.get('COMMON_BEP', 'sso_password')

            param = (url, login, passw)
            return param


    def gettargeturl(self, identity, param1, param2):
        base = ""
        if self.enviroment == "DEP":
            base = self.config.get('COMMON_DEP', 'base_host') + self.config.get('COMMON', 'base_url') + self.config.get('JSON_ADAPTER', 'service')
            if identity == "HAMTA_ANV_GRUNDUPPG_API":
                url = base + self.config.get('HAMTA_ANV_GRUNDUPPG_API', 'path') + '?' + self.config.get('HAMTA_ANV_GRUNDUPPG_API', 'params') + '&sap-client=' +  self.config.get('COMMON_DEP', 'sap_client')
                return url
            elif identity == "Z_UPPDATERA_PERSONINFO":
                #check if param1=<anvandare> or param2 <foretag> are in the url
                url = base + self.config.get('Z_UPPDATERA_PERSONINFO', 'path') +  '?' +  self.config.get('Z_UPPDATERA_PERSONINFO', 'params') + '&sap-client=' +  self.config.get('COMMON_DEP', 'sap_client')
                return url
            elif identity == "ZIK_HAMTA_HUVUDADMINISTRATORER":
                url = base + self.config.get('ZIK_HAMTA_HUVUDADMINISTRATORER', 'path') + '?' + self.config.get('ZIK_HAMTA_HUVUDADMINISTRATORER', 'params') + '&sap-client=' + self.config.get('COMMON_DEP', 'sap_client')
                return url
        elif self.enviroment == "BEP":
            base = self.config.get('COMMON_BEP', 'base_host') + self.config.get('COMMON', 'base_url') + self.config.get('JSON_ADAPTER', 'service')
            if identity == "HAMTA_ANV_GRUNDUPPG_API":
                url = base + self.config.get('HAMTA_ANV_GRUNDUPPG_API', 'path') + '?' + self.config.get('HAMTA_ANV_GRUNDUPPG_API', 'params') + '&sap-client=' +  self.config.get('COMMON_BEP', 'sap_client')
                return url
            elif identity == "Z_UPPDATERA_PERSONINFO":
                p = self.config.get('Z_UPPDATERA_PERSONINFO', 'params')
                par = self._prepareParams(p, param1, param2)
                url = base + self.config.get('Z_UPPDATERA_PERSONINFO', 'path') + '?' + par + '&sap-client=' + self.config.get('COMMON_BEP', 'sap_client')
                return url
            elif identity == "ZIK_HAMTA_HUVUDADMINISTRATORER":
                url = base + self.config.get('ZIK_HAMTA_HUVUDADMINISTRATORER', 'path') + '?' + self.config.get('ZIK_HAMTA_HUVUDADMINISTRATORER', 'params') + '&sap-client=' + self.config.get('COMMON_BEP', 'sap_client')
                return url
    def getssoticket(self):
        shutil.copyfile(os.getenv("APPDATA") + "/../Local/Google/Chrome/User Data/Default/Cookies", './Cookies')
        conn = sqlite3.connect('./Cookies')
        cursor = conn.cursor()

        # Get the results
        cursor.execute('SELECT host_key, name, value, encrypted_value FROM cookies where name = "MYSAPSSO2"')
        sso = ''
        for host_key, name, value, encrypted_value in cursor.fetchall():
            # Decrypt the encrypted_value
            decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode(
                'utf-8') or value or 0
            sso = {name: decrypted_value}
        return sso
    def getLogoutUrl(self):

        if self.enviroment == "DEP":
            loginVar = self.config.get('COMMON_DEP', 'logout_url')
        elif self.enviroment == "BEP":
            loginVar = self.config.get('COMMON_BEP', 'logout_url')
        return loginVar
    def getEmail(self):
        eMailParams = self.config.get('Z_UPPDATERA_PERSONINFO', 'params')
        ## get email from string-
        a = str.split(eMailParams, "&")
        b = ""
        for str_1 in a:
            if 'iv_epost' in str_1 :
                b = str.split(str_1, "=")
                return b[1]

    def getUser(self):
        user = self.config.get('HAMTA_ANV_GRUNDUPPG_API', 'params')
        a = str.split(user, "&")
        b = ""
        for str_1 in a:
            if 'iv_anvandare' in str_1 :
                b = str.split(str_1, "=")
                return b[1]





