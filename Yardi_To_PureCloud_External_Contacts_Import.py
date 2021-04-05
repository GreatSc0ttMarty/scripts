import json
import datetime
from datetime import date
import decimal
import pymssql
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import time


PropertyListJSONExec = "exec getPropertyListJSON;"
ResidentStatusUpdatesByDayExec = "exec getResidentStatusUpdatesByDay;"
ResidentsWithRoomatesByPropertyCodeExec = "exec getResidentsWithRoommatesByPropertyCode "


IP = '00.00.00.00'
username = 'User'
password = '**********'
DB = 'DB'


contact = {}
contact_remove = []
contact_add = []
contact_add_count = []
contact_remove_count = []


#Set Purecloud region
region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

#Get API Host for Purecloud region
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

#Create API Client and get client credentials with client ID and key
apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token("********************", "*********************")

#Create Outbound Api Client
api_instance = PureCloudPlatformClientV2.ExternalContactsApi(apiclient)


def log_data(action):
    # log_data will print action to screen and log in DATE log file
    
    print(action)
    with open(".\\logs\\" + date.today().isoformat().replace('-', '') + "_insertSet.log", 'a+') as f:
        f.write(str(datetime.datetime.now()) + f": {action}..." + '\n')
        return 1


def yardiConnect(IP, username, password, DB):
    # Uses the pymysql library to create and connect an SQL session

    log_data("Connecting to Yardi...")
    try:
        yardiConn = pymssql.connect(IP, username, password, DB)
        log_data("Connected Successfully to Yardi.")
        return yardiConn.cursor()
    except:
        log_data("Connection to Yardi failed.")


def getResidentStatusUpdatesByDay(yardiCur, SQL_Exec):
    # SQL query to grab daily resident updates

    log_data("Executing Yardi Query: 'getResidentStatusUpdatesByDay'")
    try:
        yardiCur.execute(SQL_Exec)
        result = yardiCur.fetchall()
        log_data("Query Successful: 'getResidentStatusUpdatesByDay'")
        return result
    except:
        log_data("Failed Query: 'getResidentStatusUpdatesByDay'")


def getPropertyListJSON(yardiCur, SQL_Exec):
    log_data("Executing Yardi Query: 'getPropertyListJSON'")
    try:
        yardiCur.execute(SQL_Exec)
        result = yardiCur.fetchall()
        log_data("Query Successful: 'getPropertyListJSON'")
        return result
    except:
        log_data("Failed Query: 'getPropertyListJSON'")


def getResidentsWithRoomatesByPropertyCode(yardiCur, SQL_Exec, contact_pc):
    log_data(f"Executing Yardi Query: 'getResidentsWithRoomatesByPropertyCode {contact_pc}'")
    SQL_Exec = "".join([SQL_Exec, contact_pc, ';'])
    try:
        yardiCur.execute(SQL_Exec)
        result = yardiCur.fetchall()
        log_data(f"Query Successful: 'getResidentsWithRoomatesByPropertyCode {contact_pc}'")
        return result[1:-1]
    except:
        log_data(" Failed Query: 'getResidentsWithRoomatesByPropertyCode'")


def unpackIntoJSONList(data):
    log_data("Unpacking JSON Data")
    rawData = []
    for raw in data:
        return json.loads(str(raw[0]).replace('},','}').replace('}{','},{'))


def future_past(data):
    log_data("Analyzing Daily Update Contact For Future/Past")
    if data["ResidentEvents"][0]["NewStatus"].lower() == "future" or data["ResidentEvents"][0]["NewStatus"].lower() == "past":
        name_propertyCode_newStatus = {}
        name_propertyCode_newStatus["FirstName"] = data["ResidentFirstName"]
        name_propertyCode_newStatus["LastName"] = data["ResidentLastName"]
        name_propertyCode_newStatus["CustomFields"] ={
            "propertyCode_text": data["PropertyCode"],
            "tenantNumber_text": data["ResidentCode"]
        }
        name_propertyCode_newStatus["NewStatus"] = data["ResidentEvents"][0]["NewStatus"]
        multistatus = []
        if len(data["ResidentEvents"][0]) > 1:
            
            for x in data["ResidentEvents"]:
                multistatus.append(x["ResidentHistoryId"])
            maxnum = max(multistatus)
            for x in data["ResidentEvents"]:
                if x["ResidentHistoryId"] == maxnum:
                    name_propertyCode_newStatus["NewStatus"] = x['NewStatus']
        else:
            name_propertyCode_newStatus["NewStatus"] = data["ResidentEvents"][0]['NewStatus']
        return name_propertyCode_newStatus
    else:
        return 0


def propertyList(data, contact):
    log_data("Extracting Data From PropertyListJSON")
    if data:
        for propertylist in data[1:-1]:
            for propertyl in propertylist:
                #try:
                propertyl = json.loads(propertyl.replace("},", "}").replace('\r', '').replace('\n', ''))
                
                if propertyl["code"] == contact["CustomFields"]["propertyCode_text"]:
                    address_dict = {
                        'AddressLine1': propertyl['AddressLine1'],
                        'City': propertyl['City'],
                        'State': propertyl['State'],
                        'PostalCode': propertyl['PostalCode']
                    }
                    return address_dict
                #except:
                #    return 0


def packageContact(contact):
    #Populate WDC with data from this row of Yardi query results
    log_data(f"Packaging Contact Data for PureCloud External Contacts:\n\t{' '.join([contact['FirstName'], contact['LastName']])}\n\n{contact}")
    data = {
        "firstName": contact['FirstName'].strip(),
        "lastName": contact['LastName'].strip(),
        "cellPhone": {
            'e164': contact['cellPhone']['e164'].strip(),
            'display': contact['cellPhone']['e164'].strip()
            },
        "address": {
            "address1": contact['Address']['AddressLine1'].strip(),
            "city": contact['Address']['City'].strip(),
            "state": contact['Address']['State'].strip(),
            "postalCode": contact['Address']['PostalCode'].strip(),
            },
        "personalEmail": contact['Email'].strip(),
        "customFields": {
            "propertyCode_text": contact["CustomFields"]["propertyCode_text"].strip(),
            "tenantNumber_text": contact["CustomFields"]["tenantNumber_text"].strip()
        },
        "NewStatus": contact["NewStatus"],
        "schema": { 
                "id": "53019cc0-029c-408b-b0f2-1a664b9a9d3a",
                "name": "Resident",
                "version": 3,
                "applies_to": "null",
                "enabled": "null",
                "created_by": "null",
                "date_created": "null",
                "json_schema": "null",
                "self_uri": "/api/v2/externalcontacts/contacts/schemas/53019cc0-029c-408b-b0f2-1a664b9a9d3a/versions/3"
            }
    }
    return data

        
def sortContact(contact):
    log_data("Sorting Past Future Contact")
    if contact['NewStatus'] == 'Past':
        contact_remove.append(packageContact(contact))
    elif contact['NewStatus'] == 'Future':
        contact_add.append(packageContact(contact))


def createJSONRecord(contact_add, contact_remove):
    log_data("Creating JSON Record Of Contacts Being Added and Removed From PureCloud")
    return_json = {
        str(datetime.datetime.now()): {
            'contact_add': contact_add,
            'contact_remove': contact_remove
        }
    }

    with open('.\\logs\\contact_record.json', 'a+') as f:
        json.dump(return_json, f)
        log_data("JSON Record Created")
        return 1
        

def checkContactExist(contact_list):
    contacts_ = []
    for contact_ in contact_list:
        if contact_:
            log_data("Checking if contact already in external contacts")
            q = ' '.join([contact_['firstName'], contact_['lastName']])
            api_response = api_instance.get_externalcontacts_contacts(q=q).to_dict()
            if not api_response["entities"] and contact_["NewStatus"].lower() == "future":
                contacts_.append(contact_)
            for count, results in enumerate(api_response['entities']):
                print(f"RESULTS: {results}")
                if results['custom_fields']:
                    log_data(f"{results['custom_fields']['tenantNumber_text']} == {contact_['customFields']['tenantNumber_text']}")
                    if str(results['custom_fields']['tenantNumber_text']) == str(contact_['customFields']['tenantNumber_text']):
                        log_data(f"{contact_['firstName']} {contact_['lastName']} in PureCloud External Contacts")
                        contact_['id'] = results['id']
                        contact_['exist'] = 'true'
                        print(f"CONTACT EXIST: {contact_['exist']}")

                        contacts_.append(contact_)

                    if count >= len(api_response['entities']) and not contact_exist == 0:
                        log_data(f"{contact_['firstName']} {contact_['lastName']} Not Found In PureCloud External Contacts")                
        else:
            pass
    with open('contact_list.txt', 'a+') as f:
        f.write(str(contacts_))
    yield contacts_


def addExternalContacts(contact_add):
    contact_add_ = checkContactExist(contact_add)
    if contact_add_:
        for count, contact_ in enumerate(contact_add_):
            print(str(contact_add_))
            print(type(contact_))
            print(dir(contact_))
            print(contact_)
            if contact_[count]:
                try:
                    api_response = api_instance.post_externalcontacts_contacts(body=contact_[count])
                    log_data(f"{contact_[count]['firstName']} {contact_[count]['lastName']} added to external contacts")
                except Exception as e:
                    log_data(f"Failed to add {contact_[count]['firstName']} {contact_[count]['lastName']} to external contact: {e}")


                    
def removeExternalContacts(contact_remove):
    contact_remove_ = checkContactExist(contact_remove)
    if contact_remove_:
        print(f"CONTACTS REMOVE: {str(contact_remove)}")
        print(str(contact_remove_))
        for contact_ in contact_remove_:
            print(f"number of contacts to remove {len(contact_)}")
            print(f"number of contacts_Remove to remove {len(contact_remove)}")
            print("contact_}")
            for cont in contact_:
                print(cont)
                if cont['id']:
                    try:
                        api_response = api_instance.delete_externalcontacts_contact(cont['id'])
                        log_data(f"{cont['id']} - {cont['firstName']} {cont['lastName']} has been removed from external contacts")
                    except Exception as e:
                        log_data(f"Failed to remove {cont['firstName']} {cont['lastName']} from external contact: {e}")
                else:
                    log_data(f"{cont['firstName']} {cont['lastName']} not In external contacts")


def main():
    yardiCur = yardiConnect(IP, username, password, DB)
    ResidentStatusUpdatesByDay = getResidentStatusUpdatesByDay(yardiCur, ResidentStatusUpdatesByDayExec)
    if ResidentStatusUpdatesByDay:
        PropertyListJSON = getPropertyListJSON(yardiCur, PropertyListJSONExec)
        for ResidentStatus in ResidentStatusUpdatesByDay[1:-1]:
            for Resident in ResidentStatus:
                contact = future_past(json.loads(Resident))
                if contact:
                    contact['Address'] = propertyList(PropertyListJSON, contact)
                    ResidentsWithRoomatesByPropertyCodeJSON = unpackIntoJSONList(getResidentsWithRoomatesByPropertyCode(yardiCur, ResidentsWithRoomatesByPropertyCodeExec, contact["CustomFields"]['propertyCode_text']))
                    if ResidentsWithRoomatesByPropertyCodeJSON:
                        try:
                            contact['cellPhone'] = {
                                "display": "+1" + str(ResidentsWithRoomatesByPropertyCodeJSON['Phone']).replace('(', '').replace(')', '').replace('-', '').replace(' ', ''),
                                "e164": "+1" + str(ResidentsWithRoomatesByPropertyCodeJSON['Phone']).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                                }
                        except:
                            log_data(f"Problem adding phone number for: \n\t{contact}")

                        contact['Email'] = ResidentsWithRoomatesByPropertyCodeJSON['Email']
                        contact['PropertyId'] = ResidentsWithRoomatesByPropertyCodeJSON['PropertyId']

                        sortContact(contact)
                    else:
                        with open('null_query_returns.txt', 'w+') as f:
                            f.write(f"Null Query: getResidentsWithRoomatesByPropertyCode {contact['CustomFields']['propertyCode_text']}")

        createJSONRecord(contact_add, contact_remove)
        addExternalContacts(contact_add)
        removeExternalContacts(contact_remove)
    else:
        log_data("No ResidentStatusUpdatesByDay Results")


if __name__ == '__main__':
    main()