import tabula
import pandas as pd

# Replace 'file_path.pdf' with the path to your PDF file
file_path = 'Wards.pdf'

# Iterate through each page
for page in range(1, len(tabula.read_pdf(file_path, pages='all')) + 1):
    # Read the data for the current page
    dfs = tabula.read_pdf(file_path, pages=page)
    
    # Save the DataFrame for the current page to a CSV file
    for idx, df in enumerate(dfs):
        df.to_csv(f'page_{page}_df_{idx+1}.csv', index=False)

        print(f"CSV file for page {page}, DataFrame {idx+1} saved successfully.")
