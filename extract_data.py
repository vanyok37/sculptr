from secretary_of_state import getBusinessSearchList, getBusinessFilingList, getTransactionDocumentsList, getFile, getBusinessId, getAnnualReports, getNameAndCorrespondence, getAuthorizerName
import pandas as pd
import json
import os
import logging


def extractData(businessName, folderName):
    # try to create subfolder and return if it already exists 
    # for this business name
    subfolder_path = os.path.join(folderName, businessName)
    files_subfolder_path = os.path.join(subfolder_path, "files")

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        os.makedirs(files_subfolder_path)
    else:
        return

    # get business search list and business id
    businessSearchList = getBusinessSearchList(businessName)
    businessId = getBusinessId(businessSearchList, businessName)

    # if business id doesn't save the reason and return
    if not businessId:
        notFound = {
            'name': businessName
        }
        with open(os.path.join(subfolder_path, 'NotFound.json'), 'w') as json_file:
            logging.info(f"No search results.")
            json.dump(notFound, json_file, indent=4)
        return

    # if business id exists save the business search list
    with open(os.path.join(subfolder_path, 'BusinessSearchList.json'), 'w') as json_file:
        json.dump(businessSearchList, json_file, indent=4)

    # get business filing list and save  
    businessFilingList = getBusinessFilingList(businessId)
    with open(os.path.join(subfolder_path, 'BusinessFilingList.json'), 'w') as json_file:
        json.dump(businessFilingList, json_file, indent=4)


    # get annual reports and initialize transaction doc list
    annualReports = getAnnualReports(businessFilingList)

    if annualReports == None:
        logging.info(f"Info stored.")
        return
    
    allTransactionDocuments = []

    # loop through the annual reports
    for report in annualReports:
        try:
            # get the transaction doc list and save it to the list
            transactionDocumentsList = getTransactionDocumentsList(report)
            allTransactionDocuments.append(transactionDocumentsList)

            # get the name and correspondence and continue if they aren't valid
            name, correspondence = getNameAndCorrespondence(transactionDocumentsList)
            if not name:
                continue

            # get the pdf file 
            file = getFile(name, correspondence)

            # ensure the directory for the file exists
            file_path = os.path.join(files_subfolder_path, correspondence)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # save the file to the files subfolder
            file_path += '.pdf'
            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(file)
        except Exception as e:
            logging.error(f"Error in annual report loop: {e}")
            continue

    # save the transaction document list
    with open(os.path.join(subfolder_path, 'TransactionDocumentsList.json'), 'w') as json_file:
        json.dump(allTransactionDocuments, json_file, indent=4)
    
    logging.info(f"Info stored.")
    return
