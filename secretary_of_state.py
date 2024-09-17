import requests
import json
import logging
from Levenshtein import distance
import heapq
from urllib.parse import quote

# functions for api data extraction

def getBusinessSearchList(business_name):
    # Replace spaces with '%20' and capitalize the whole string
    formatted_name = quote(business_name)
    url = "https://ccfs-api.prod.sos.wa.gov/api/BusinessSearch/GetBusinessSearchList"

    # Prepare the payload with the formatted business name
    payload = f"Type=BusinessName&SearchType=BusinessName&SearchEntityName={formatted_name}&SortType=ASC&SortBy=Entity%20Name&SearchValue={formatted_name}&SearchCriteria=Contains&IsSearch=true&PageID=1&PageCount=25"
    
    # Define the headers
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ccfs.sos.wa.gov',
        'priority': 'u=1, i',
        'referer': 'https://ccfs.sos.wa.gov/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    # print(business_name)
    try:
        response = requests.request("POST", url=url, headers=headers, data=payload)
        return response.json()
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        logging.info("getBusinessSearchList() retry")
        return getBusinessSearchList(business_name)
    except requests.exceptions.RequestException as e:
        raise Exception(f"getBusinessSearchList(): Request error: {e}")
    except Exception as e:
        raise Exception(f"getBusinessSearchList(): Unexpected error: {e}")

def getBusinessFilingList(business_id):
    url = f"https://ccfs-api.prod.sos.wa.gov/api/BusinessSearch/GetBusinessFilingList?IsOnline=true&businessId={business_id}"
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Mon, 26 Jul 1997 05:00:00 GMT',
    'origin': 'https://ccfs.sos.wa.gov',
    'priority': 'u=1, i',
    'referer': 'https://ccfs.sos.wa.gov/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        response = requests.request("GET", url, headers=headers)
        return response.json()
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        logging.info("getBusinessFilingList() retry")
        return getBusinessFilingList(business_id)
    except requests.exceptions.RequestException as e:
        raise Exception(f"getBusinessFilingList(): Request error: {e}")
    except Exception as e:
        raise Exception(f"getBusinessFilingList(): Unexpected error: {e}")

def getTransactionDocumentsList(filing):
    url = "https://ccfs-api.prod.sos.wa.gov/api/Common/GetTransactionDocumentsList"
    payload = f"ID={filing[0]}&FilingNumber={filing[1]}"
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://ccfs.sos.wa.gov',
    'priority': 'u=1, i',
    'referer': 'https://ccfs.sos.wa.gov/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        logging.info("getTransactionDocumentsList() retry")
        return getTransactionDocumentsList(filing)
    except requests.exceptions.RequestException as e:
        raise Exception(f"getTransactionDocumentsList(): Request error: {e}")
    except Exception as e:
        raise Exception(f"getTransactionDocumentsList(): Unexpected error: {e}")

def getFile(name, correspondence):
    url = f"https://ccfs-api.prod.sos.wa.gov/api/Common/DownloadOnlineFilesByNumber?fileName={name}&CorrespondenceFileName={correspondence}"

    headers = {
      'accept': 'application/octet-stream',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': 'https://ccfs.sos.wa.gov',
      'priority': 'u=1, i',
      'referer': 'https://ccfs.sos.wa.gov/',
      'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        response = requests.request("POST", url, headers=headers)
        if response.status_code != 200:
            return None
    
        return response.content
    except requests.exceptions.RequestException as e:
        raise Exception(f"getFile(): Request error: {e}")
    except IndexError as e:
        return f"getFile(): No value found for name {name} and correspondence {correspondence}."
    except Exception as e:
        raise Exception(f"getFile(): Unexpected error: {e}")

# functions to extract fields from json

def getBusinessId(businessList, businessName): 
    if len(businessList) == 1:
        return businessList[0]['BusinessID']
    elif len(businessList) == 0:
        return None
    else:
        min_distance = float('inf')
        closest_business_id = None
        
        for business in businessList:
            checkName = business['BusinessName']
            dist = distance(checkName, businessName)
            
            # Update if this business has a smaller distance
            if dist < min_distance:
                min_distance = dist
                closest_business_id = business['BusinessID']
        
        # Return the business with the smallest distance
        return closest_business_id

def getAnnualReports(filingList):
    filingTypeName = "ANNUAL REPORT"
    validFilings = []
    for filing in filingList:
        if filing['FilingTypeName'] == filingTypeName:
            validFilings.append((filing['Transactionid'], filing['FilingNumber']))
    
    if not validFilings:
        return None
    
    return validFilings

def getNameAndCorrespondence(documentList):
    annualReportId = 4

    for document in documentList:
        if document["DocumentTypeID"] == annualReportId:
            return document["FileLocationCorrespondence"], document["CorrespondenceFileName"]
        
    return None, None

def getAuthorizerName(business_id):
    url = f"https://ccfs-api.prod.sos.wa.gov/api/BusinessSearch/GetBusinessFilingList?IsOnline=true&businessId={business_id}"
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Mon, 26 Jul 1997 05:00:00 GMT',
    'origin': 'https://ccfs.sos.wa.gov',
    'priority': 'u=1, i',
    'referer': 'https://ccfs.sos.wa.gov/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        response = requests.request("GET", url, headers=headers)
        return response.json()[0]['AuthorizerName']
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        logging.info("getAuthorizerName() retry")
        return getAuthorizerName(business_id)
    except IndexError as e:
        return None
    except requests.exceptions.RequestException as e:
        raise Exception(f"getAuthorizerName(): Request error: {e}")
    except Exception as e:
        raise Exception(f"getAuthorizerName(): Unexpected error: {e}")

def getNumberOfSearchResults(business_name):
    # Replace spaces with '%20' and capitalize the whole string
    formatted_name = business_name.replace(' ', '%20').upper()
    
    # Prepare the payload with the formatted business name
    payload = f"Type=BusinessName&SearchType=BusinessName&SearchEntityName={formatted_name}&SortType=ASC&SortBy=Entity%20Name&SearchValue={formatted_name}&SearchCriteria=Contains&IsSearch=true&PageID=1&PageCount=25"
    
    # Define the headers
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ccfs.sos.wa.gov',
        'priority': 'u=1, i',
        'referer': 'https://ccfs.sos.wa.gov/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.request("POST", "https://ccfs-api.prod.sos.wa.gov/api/BusinessSearch/GetBusinessSearchList", headers=headers, data=payload)
        return len(response.json())
    except requests.exceptions.RequestException as e:
        raise f"getNumberOfSearchResults(): Request error: {e}"
    except IndexError as e:
        return f"getNumberOfSearchResults(): No value found for name {business_name}."
    except Exception as e:
        return f"getNumberOfSearchResults(): Unexpected error: {e}"

