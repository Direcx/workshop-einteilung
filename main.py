import logging
import ExcelConverter as ec
from ExcelConverter import excel_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    print(ec.parse_persons_data(excel_data))
