# Replace 'USERNAME' and 'PASSWORD' with your Autotask resource credentials and replace [ZONE] with 
# the database zone you are in. example: webservices3.autotask.net
# See the API documentation for information about which zone you are in.
from requests import Request, Session
import base64
import sys

username = "{USERNAME}"
password = "{PASSWORD}"
url = "https://webservices5.autotask.net/atservices/1.6/atws.asmx"

# *1 Available op attributes: values, Equals, NotEqual, GreaterThan, LessThan, GreaterThanorEquals, LessThanOrEquals, BeginsWith, EndsWith, Contains, IsNotNull, IsNull, 
# IsThisDay, Like, NotLike, SoundsLike

body = """<?xml version='1.0' encoding='utf-8'?>
<soap:Envelope xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema'>
    <soap:Header>
        <AutotaskIntegrations xmlns='http://autotask.net/ATWS/v1_6/'> 
            <IntegrationCode>DOYQOFP6ATYM4DY7ZN3T3A5ET4A</IntegrationCode>
		</AutotaskIntegrations>
    </soap:Header>
    <soap:Body>
        <query xmlns="http://autotask.net/ATWS/v1_6/">
            <sXML>
                <![CDATA[<queryxml>
                    <entity>contact</entity>
                        <query>
                            <condition>
                                <field>firstname<expression op="equals">Mike</expression></field>
                            </condition>
                        </query>
                </queryxml>]]>
            </sXML>
        </query>
    </soap:Body>
</soap:Envelope>"""

headers = {
        'Content-Type': "text/xml; charset=utf-8",
        'Content-Length': str(len(body)),
        'Authorization': "Basic " + bytes.decode(base64.b64encode(bytes(username + ":" + password, "utf-8"))),
        'SOAPAction': "http://autotask.net/ATWS/v1_6/query",
        'Accept': "application/json"
    }

print(headers)
s = Session()
req = Request('POST', url, data=body, headers=headers)
prepped = req.prepare()
response = resp = s.send(prepped)
print("response.status_code")
print(response.status_code)
print("response.status_code")
print(response.content)