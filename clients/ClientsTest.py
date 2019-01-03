import unittest
from configColl.Init import Init
from clients.Clients import Client
import requests, unittest
import argparse
import logging

class ClientsTest(unittest.TestCase):

    def setUp(self):
        #########################get the enviroment as an input##################
        parser = argparse.ArgumentParser()
        parser.add_argument("enviroment", help="denotes the target portal serverid DEP or BEP")
        parser.add_argument("mode", help="unittest or running for fun")
        args = parser.parse_args()

        ####################START Getting the configuration######################
        initiator = Init("config.ini", args.enviroment)
        initiator.load()

        ###########################Start A Session###############################
        loginvar = initiator.getloginvar()
        req_open = requests.session()
        req_open.post(loginvar[0], auth=(loginvar[1], loginvar[2]))

        #########################Start Unit Test#################################
        ###########################Hamta Grunduppgifter##########################

        grundUppgUrl = initiator.gettargeturl("HAMTA_ANV_GRUNDUPPG_API")
        content = ""
        action = "GET"
        self.cli = Client(req_open, grundUppgUrl, content, action)
        self.cli.call()
    def test_get_http_code_200(self):
        self.assertEqual(str(self.cli.responseCode), '200')
        print(self.cli.json_content)
    def test_get_json_is_not_empty(self):
        self.assertNotEquals( "", self.cli.json_content["esAnvandare"]["anvandare"])
