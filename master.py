import logging
import pandas as pd
from extract_data import extractData
from extract_business_info import extractBusinessInfo, getAuthorizerName
import argparse
from pathlib import Path
import os

if __name__ == "__main__":

    # Set up the argument parser inside the if block
    parser = argparse.ArgumentParser(description="Process an Excel file.")
    parser.add_argument('file', type=str, help='The Excel file with addresses and business names.')
    
    # Parse the arguments
    args = parser.parse_args()
    inputFile = Path(args.file)

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Read in excel file as pandas dataframe
    df = pd.read_excel(inputFile)
    df = df.head(5)

    # Create data folder
    from pathlib import Path

    # Create data folder
    dataFolder = Path(inputFile.stem + "_data")
    dataFolder.mkdir(parents=True, exist_ok=True)

    # Extract business data
    for index, row in df.iterrows():
        recordedOwnerName = row['Recorded Owner Name']

        if pd.notna(recordedOwnerName):
            logging.info(f"Processing business: {recordedOwnerName}")
            try:
                extractData(recordedOwnerName, dataFolder)
            except Exception as e:
                logging.error(f"Error when processing: {e}")

    # Add new columns to the DataFrame
    df['Recorded Owner Email'] = ''
    df['Recorded Owner Phone Number'] = ''
    df['Recorded Owner Authorizer Name'] = ''

    # Extract business information
    for index, row in df.iterrows():
        recordedOwnerName = row['Recorded Owner Name']

        if pd.notna(recordedOwnerName):
            logging.info(f"Extracting info: {recordedOwnerName}")
            try:
                emails, phoneNumbers = extractBusinessInfo(recordedOwnerName, dataFolder)
                authorizerName = getAuthorizerName(recordedOwnerName, dataFolder)
                df.at[index, 'Recorded Owner Email'] = ', '.join(emails) if emails else 'emails not found'
                df.at[index, 'Recorded Owner Phone Number'] = ', '.join(phoneNumbers) if phoneNumbers else 'phone numbers not found'
                df.at[index, 'Recorded Owner Authorizer Name'] = authorizerName
            except Exception as e:
                logging.error(f"Error when processing: {e}")

    # Reorder the columns
    df = df[['Property Address','Recorded Owner Name', 'Recorded Owner Email', 'Recorded Owner Phone Number', 'Recorded Owner Authorizer Name']]
    
    # Save the updated DataFrame to a new Excel file
    updatedFile = inputFile.with_stem(inputFile.stem + "_business_info")
    df.to_excel(updatedFile, index=False)