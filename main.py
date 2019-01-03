from configColl.Init import Init
from clients.Clients import Client
from clients.ClientsTest import ClientsTest
import argparse
import requests, json, unittest, logging
import threading, time, csv, sys

def isEmailMutated(content, email):
    for i in content['etAdministratorer']:
        if i['epost'] == email:
            return True
    return False

def runMainPost(ivAnvandare, ivForetag):
    ###########################Hamta Grunduppgifter##########################
    ##########################POST POST POST POST POST#######################
    uppPersInfo = initiator.gettargeturl("Z_UPPDATERA_PERSONINFO", ivAnvandare, "")
    content = ""
    action = "POST"
    ##########################POST POST POST POST POST#######################
    ########################Make nex call verify the results#################
    hamtaHuvAdmin = initiator.gettargeturl("ZIK_HAMTA_HUVUDADMINISTRATORER", "", "")
    it_foretag = [ivForetag]
    cContent = {"iv_anvandare" : ivAnvandare, 'it_orgbp' : it_foretag }
    jsData = json.dumps(cContent)
  #  print(jsData)
  #  print(hamtaHuvAdmin)
    # Statistic for Data format
    # ACTION, FM, HTTP-RESULT, BAPI_RETURN, DATA_CHECK
    log = ""

    try:
        cli = Client(req_open, uppPersInfo, content, action, args.enviroment, sso=False )
        # check the results of the call
      #  if ivAnvandare == '0012347285':
        cli.call("", ivAnvandare, ivForetag)
        if (str(cli.responseCode) == "200"):
            ##check content in the JSON message

            if not (cli.json_content['etRetur']):
                #write to the log application
                cli2 = Client(req_open, hamtaHuvAdmin,  jsData, "POST", args.enviroment, sso=False)  #Post
                cli2.call(jsData, ivAnvandare, ivForetag)
                if (str(cli2.responseCode) == "200"):
                    if cli2.json_content['etAdministratorer']:
                        emailToVerify = initiator.getEmail()
                        if isEmailMutated(cli2.json_content, emailToVerify):
                            log = 'Verified Result - ' + 'user: ' + ivAnvandare + ' foretag: ' + ivForetag + ' - GET - 200 - ZIK_HAMTA_HUVUDADMINISTRATORER - ' + \
                                 'N/A' + ' - SUCCESS!'
                        else:
                            log = 'Not Verified - ' + 'user: ' + ivAnvandare + ' foretag: ' + ivForetag + ' - GET - 200 - ZIK_HAMTA_HUVUDADMINISTRATORER - ' + \
                            'email not mutated check in SM37' + ' - Fail!'
                        logging.info(log)
                    else:
                        if cli2.json_content['etReturn']:
                            log = 'Not verified - ' + 'user: ' + ivAnvandare + ' foretag: ' + ivForetag  + ' - GET - 200 - ZIK_HAMTA_HUVUDADMINISTRATORER - ' + \
                                  cli2.json_content['etReturn'][0]['message'] + ' - FAIL!'
                        else:
                            log = 'Not verified - ' + 'user: ' + ivAnvandare + ' foretag: ' + ivForetag  + ' - GET - 200 - ZIK_HAMTA_HUVUDADMINISTRATORER - ' + \
                                  'BAPI RETURN EMPTY check in SM37!!: ' + ' - FAIL!'
                        logging.info(log)
                else:
                    log = 'Not Verified - ' + ivAnvandare + ' ' + ivForetag + ' - GET - ' + str(
                        cli2.responseCode) + '- ZIK_HAMTA_HUVUDADMINISTRATORER - ' + \
                          'N/A' + ' - FAIL!'
                    logging.info(log)
            else:
                # write to the file and make statistics, both test passed.
                #                logging.info('Fails, BAPI Return is not empty FM: Z_UPPDATERA_PERSONINFO')

                if cli.json_content['etRetur']:
                    log = 'Not Verified - ' + ivAnvandare + ' ' + ivForetag + ' - GET - ' + str(cli.responseCode) + '- Z_UPPDATERA_PERSONINFO - ' + \
                          cli.json_content['etRetur'][0]['message'] + ' - FAIL!'
                else:
                    log = 'Not Verified - ' + ivAnvandare + ' ' + ivForetag + ' - GET - ' + str(cli.responseCode) + '- Z_UPPDATERA_PERSONINFO - ' + \
                          'EMPTY BAPI RETURN' + ' - FAIL!'
                logging.info(log)
        else:
            log = 'Not Verified - ' + ivAnvandare + ' ' + ivForetag + ' - GET - ' + str(cli.responseCode) + '- Z_UPPDATERA_PERSONINFO - ' + \
                  'N/A' + ' - FAIL!'
            logging.info(log)
    except:
        print('user: ' + ivAnvandare + ' foretag: ' + ivForetag)
        print("Unexpected error:", sys.exc_info()[0])
        log = 'Not verified: EXCEPTION!  ' + sys.exc_info()[0] + 'user: ' + ivAnvandare + ' foretag: ' + ivForetag
        logging.info(log)


def runMainGet():


    ###########################Hamta Grunduppgifter##########################
    ##########################GET GET GET GET GET GET########################
    grundUppgUrl = initiator.gettargeturl("HAMTA_ANV_GRUNDUPPG_API", "", "")
    content = ""
    action = "GET"
    cli = Client(req_open, grundUppgUrl, content, action, args.enviroment, sso=False)
    #check the results of the call
    cli.call("", "", "")
    #Statistic for Data format
    #ACTION, FM, HTTP-RESULT, BAPI_RETURN, DATA_CHECK
    log = ""
    try:
        if ( str(cli.responseCode) == "200"):
            ##check content in the JSON message
            if ( "" == cli.json_content["esAnvandare"]["anvandare"]  and not cli.json_content['etRetur']):
                log = 'Empty content - ' + initiator.getUser() + ' - GET - 200 - ZIK_HAMTA_ANV_GRUNDUPPG_API - ' + \
                      ['etRetur'][0]['- message'] + ' - FAIL!'
                logging.info(log)
            else:
                #write to the file and make statistics, both test passed.
                user = initiator.getUser()
                log = "verified result - " + initiator.getUser() + " - GET - 200 - ZIK_HAMTA_ANV_GRUNDUPPG_API - " + "EMPTY - SUCCESS!"
                logging.info(log)

        else:
            log = 'HTTP_ERROR - ' + initiator.getUser() + ' - GET - ' + str(cli.responseCode) + '- ZIK_HAMTA_ANV_GRUNDUPPG_API - ' + \
                  ['etRetur'][0]['- message'] + ' - FAIL!'
            logging.info(log)
    except:
        logging.info('Fail, exception triggered during the server call: first call FM: ZIK_HAMTA_ANV_GRUNDUPPG_API')

###########################Hamta Grunduppgifter##########################
##########################GET GET GET GET GET GET########################

###############################Logging set Upp###########################
logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)


#########################get the enviroment as an input##################
parser = argparse.ArgumentParser()
parser.add_argument("enviroment", help="denotes the target portal serverid DEP or BEP")
parser.add_argument("mode", help="unittest or running for fun")
parser.add_argument("thread", help="parallel or serial")
parser.add_argument("call", help="quantity of calls")
parser.add_argument("mSession", help="multiple session False/True")
#parser.add_argument("email", help="denotes the email to update personinfo")
#parser.add_argument("phoneNo", help="denotes the phone number to update personinfo")
args = parser.parse_args()
####################START Getting the configuration######################
initiator = Init("config.ini", args.enviroment)
initiator.load()
###########################Start A Session###############################
loginvar = initiator.getloginvar()
req_open = requests.session()                  #creating 2 sessions as a post will be needed
req_open2 = requests.session()                 #creating 2 sessions as a post will be needed
a = requests.adapters.HTTPAdapter(pool_connections = 2, pool_maxsize = 10, max_retries=10)
a2 = requests.adapters.HTTPAdapter(pool_connections = 2, pool_maxsize = 10, max_retries=10)
req_open.mount(loginvar[0], a)
req_open.post(loginvar[0], auth=(loginvar[1], loginvar[2]))
req_open2.mount(loginvar[0], a2)
req_open2.post(loginvar[0], auth=(loginvar[1], loginvar[2]))
qReq = int(args.call)

if bool(args.mSession):
    logging.info('Only GET Test: KEY - GET - MESSAGE - ACTION - HTTP_RESULT - FM - BAPI_RETURN - RESULT')

    #############Trigger Test for GET operation via JSON Adapter#############
    if args.mode != "test":
        if args.thread == "parallel":
            threads = []
            for i in range(qReq):
                t = threading.Thread(target=runMainGet)
                threads.append(t)
                t.start()
        else:
            for i in range(qReq):
                runMainGet()
    else:
        for i in range(10):
            suite = unittest.TestLoader().loadTestsFromTestCase(ClientsTest)
            unittest.TextTestRunner(verbosity=2).run(suite)
    time.sleep(10)

    logging.info('')
    logging.info('')

logging.info('POST adn GET Test: KEY - GET - LOGTIME - MESSAGE - ACTION - HTTP_RESULT - FM - BAPI_RETURN - RESULT')

#############Trigger Test for POST/PUT operation via JSON Adapter##########
######################## end the session !!###############################
#1. open the csv file and prepare the calls.

entries = set()
entry  = []

with open("users.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
          #  print(f'Column names are {", ".join(row)}') #header
            line_count += 1
        elif len(entry) == qReq:
            break
        else:
            key = (row[0])
            if key not in entries:
                entries.add(key)
                entry.append(row)
        line_count += 1

#now we have all the necessary object to make a call.

threads = []        #create an array of threads
for j in entry:
    if args.mode != "test":
        if args.thread == "parallel":
            t = threading.Thread(target=runMainPost, args=(j[0], j[1]))
            threads.append(t)
            t.start()
        else:
            runMainPost()
    else:
        for i in range(10):
            suite = unittest.TestLoader().loadTestsFromTestCase(ClientsTest)
            unittest.TextTestRunner(verbosity=2).run(suite)


logout_url = initiator.getLogoutUrl()

time.sleep(30)
req_open.post(logout_url)
req_open2.post(logout_url)

print("FINISH")







