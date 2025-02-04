import logging
import ExcelConverter as ec
import Values as v
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("reading data from excel")
    print(ec.parse_persons_data(v.excel_data))
