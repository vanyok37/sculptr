import os
import pandas as pd
from pdfminer.high_level import extract_text
import re
import logging
import json


def getPhoneAndEmail(file):
    try:
        text = extract_text(file)
    except Exception as e:
        logging.error(f"Error extracting text from file: {e}")
        return None, None
    
    phoneNumber = re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)

    phoneNumber = phoneNumber.group() if phoneNumber else None
    email = email.group() if email else None

    if phoneNumber:
        phoneNumber = re.sub(r'\D', '', phoneNumber)

    return email, phoneNumber

def getAuthorizerName(businessName, folderName):
    try:
        businessPath = os.path.join(folderName, businessName)
        businessFolder = os.listdir(businessPath)
        if 'NotFound.json' in businessFolder:
            return "business name not found"
        
        businessFilingListPath = os.path.join(businessPath, 'BusinessFilingList.json')

        with open(businessFilingListPath, 'r') as file:
            businessFilingList = json.load(file)
        
        for filing in businessFilingList:
            if 'AuthorizerName' in filing and filing['AuthorizerName'].strip() != "":
                return filing['AuthorizerName']
        
        return "authorizer name not found"
    
    except Exception as e:
        return {'error': str(e)}

def extractBusinessInfo(businessName, folderName):
    try:
        businessPath = os.path.join(folderName, businessName)
        businessFolder = os.listdir(businessPath)
        if 'NotFound.json' in businessFolder:
            return {'business name not found'}, {'business name not found'}
        
        filesPath = os.path.join(businessPath, 'files')
        filesFolder = os.listdir(filesPath)

        emails = set()
        phoneNumbers = set()
        for fileName in filesFolder:
            filePath =  os.path.join(filesPath, fileName)
            email, phoneNumber = getPhoneAndEmail(filePath)
            if email:
                emails.add(email)
            if phoneNumber:
                phoneNumbers.add(phoneNumber)
        return emails, phoneNumbers
    except Exception as e:
        logging.error(f"Error when processing businees {businessName}: {e}")
