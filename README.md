# Sculptr Secretary of State Script

## Overview

This tool extracts business data from the [Washington State Secretary of State Corporation Search](https://ccfs.sos.wa.gov/#/). It retrieves data for each unique business and stores it in a `data` folder. From this data, emails and phone numbers are extracted for further use.

## Usage
### Prerequisites 

- Python 3.6 or newer
- pip (Python package installer)
- git

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Install dependencies:**

    Run the following command to install the necessary Python libraries:

    ```bash
    python setup.py
    ```

    This command will check for Python and pip, and then install all required libraries.

3. **Run the script:**

    ```bash
    python master.py YOUR_EXCEL_FILE.xlsx
    ```
2. **Output:**

    After the script finishes running, which could take 10+ minutes depending on connection and excel size, a data folder named `YOUR_EXCEL_FILE_data` will be created along with a new excel file named `YOUR_EXCEL_FILE_business_info`.

## Files

### `secretary_of_state.py`
Contains functions to make API calls to the Washington Secretary of State website.

### `extract_data.py`
Pulls business data from the API and stores it in the `data` folder.

### `extract_business_info.py`
Extracts emails and phone numbers for each business and stores the results in an Excel file.

### `master.py`
Main script that takes an Excel file with business names and addresses as input, then returns an Excel file with contact information. This script utilizes `extract_data.py` and `extract_business_info.py`.
