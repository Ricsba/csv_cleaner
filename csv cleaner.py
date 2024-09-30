import csv

format_dictionary = {
    "code_128": ["code 128", "code128", "CODE 128", "CODE128"],
    "ean_13": ["EAN13", "ean13", "ean 13", 'EAN-13', 'ean-13'],
    "gs1_128": ["gs1"],
    "qr_code": ["qr code", "qrcode", "qr"],
}
 
boolean_formats = ["TRUE", "True", "true", "FALSE", "False", "false"]

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

def check_barcode_correct_format(barcode_type_value, row_number):
    if barcode_type_value not in list(format_dictionary.keys()):
        print(barcode_type_value + " not found" + " in row " + str(row_number + 1))
        
def correct_barcode_wrong_format(row_data, barcodetype_column):
    # we have a dictionary that has the correct format as key and wrong formats as values.
    # Go key by key, and check if the value of the csv row is in the wrong formats values for this correct key.

    is_barcode_type_modified = False

    for correct_format, wrong_format_list in format_dictionary.items():
        if row_data[barcodetype_column] in wrong_format_list:
            # if yes I will change the csv row with the current key. and I won't look any further
            row_data[barcodetype_column] = correct_format
            is_barcode_type_modified = True
            print("format has been fixed with " + row_data[barcodetype_column])
            break

        # if no, go to the next key and repeat the steps.
        else:
            continue

    # if no keys left and no modification happened, I will print that the format is wrong and cannot be automatically fixed
        if not is_barcode_type_modified:
            print(
                "the format "
                + row_data[barcodetype_column]
                + " is wrong and cannot be fixed"
            )

def correct_weight_format(row_data, weight_column):
    #if the decimal part is separated with a comma, replace it with a dot
    if "," in row_data[weight_column] and row_data[weight_column].count(',') == 1:
        row_data[weight_column] = row_data[weight_column].replace(",", ".")
        print('weight format corrected')
    else:
        print('Sorry, unable to correct the format')

def check_weight_format(row_data, weight_column, is_float, row_number):
    if weight_column not in row_data:
        return

    weight = row_data[weight_column]
    if not weight:
        print('the weight in row ' + str(row_number + 1) + ' han an empty value')
    elif not is_float(weight):
        print('the weight '+ weight + ' in row ' + str(row_number + 1) + ' is not correct and we will try to convert it')
        correct_weight_format(row_data, weight_column)

#correct netvalue format
def correct_netvalue_format(row_data, netvalue_column):
    #if there is a curreny symbol, remove it
    currency_symbols = ['$', '€', '£']

    for symbol in currency_symbols:
        if symbol in row_data[netvalue_column]:
            row_data[netvalue_column] = row_data[netvalue_column].replace(symbol, '')
            print('Currency symbol removed')
        else:
            continue

    #if the decimal part is separated with a comma, replace it with a dot
    if "," in row_data[netvalue_column] and row_data[netvalue_column].count(',') == 1:
        row_data[netvalue_column] = row_data[netvalue_column].replace(",", ".")
        print('netvalue format corrected')
    elif "." in row_data[netvalue_column]:
        print('netvalue format is correct')
    else:
        print('Sorry, unable to correct the format')     

def check_netvalue_format(row_data, netvalue_column, is_float, row_number):
    netvalue = row_data[netvalue_column]

    if not netvalue:
        print('the netvalue in row ' + str(row_number +1) + ' han an empty value')
    
    
    elif not is_float(netvalue):
        print('the netvalue '+ netvalue + ' in row ' + str(row_number +1) + ' is not correct and we will try to convert it')
        correct_netvalue_format(row_data, netvalue_column)
             
# define a function able to create a corrected csv file, and divide the csv file for every 'n' products in it
# NOTE: rename to create_the_correct_csv_file
def create_the_corrected_csv_file(data_list, max_rows_allowed, name):
    total_products = len(data_list) - 1  # Subtract header row

    for i in range(0, total_products, max_rows_allowed):
        filename = name + str(i + 1) + "-" + str(i + max_rows_allowed) + ".csv"
        with open(filename, "w", newline="") as corrected_csv_file:
            writer = csv.writer(corrected_csv_file)
            writer.writerow(data_list[0].keys())  # Write the header
            for row_data in data_list[i : i + max_rows_allowed]:
                writer.writerow(row_data.values())

#check SKU function
def check_sku(row_data, sku_column, row_number):
    sku = row_data[sku_column]
    if not sku:
        print('the sku in row ' + str(row_number + 1) + ' has an empty value')

#check name function
def check_name(row_data, name_column, row_number):
    name = row_data[name_column]
    if not name:
        print('the name in row ' + str(row_number + 1) + ' han an empty value' )

# check organic, lotsEnabled, fragile - if the header is there, it should have a value
def check_boolean_format(row_data, header, row_number):
    if header in row_data:
        value = row_data[header]
        if value not in boolean_formats:
            print('the value ' + value + ' for ' + header+ ' in row ' + str(row_number+1) + ' is not supported or not found')

#remove empty columns
def remove_empty_columns(data_list):
    headers = data_list[0].keys()
    columns_to_remove = []

    for header in headers:
        column_values = [row[header] for row in data_list if header in row]
        if all(value == "" or value is None for value in column_values):
            columns_to_remove.append(header)

    for column in columns_to_remove:
        for row in data_list:
            row.pop(column, None)

    return data_list

#County Code function
def correct_origin_country_code(row_data, origin_country_code_column):
    if "originCountryCode" in row_data:
        origin_country_code = row_data["originCountryCode"]
        if origin_country_code.islower():
            row_data["originCountryCode"] = origin_country_code.upper()



        
# Open csv file

def main():
    file_name = input("What's the csv file name?")

    # read csv file
    # NOTE: Use CsvDictReader instead of the normal reader.
    # So that instead of getting the index of each row header,
    # you can easily do row['barcodeType']
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        data_list = []
        for row in csv_reader:
            data_list.append(row)


    # check mandatory fields in headers
    headers = data_list[0].keys()
    mandatory_fields = ["sku", "name", "netValue", "barcode", "barcodeType"]

    for mandatory_field in mandatory_fields:
        if mandatory_field in headers:
            continue
        else:
            print("Mandatory Field " + mandatory_field + " Not Found")



    #processing and correcting data    
    for row_number, row_data in enumerate(data_list):
        check_sku(row_data, "sku", row_number)
        check_name(row_data, "name", row_number)
        check_netvalue_format(row_data, "netValue", is_float, row_number)
        check_boolean_format(row_data, 'organic', row_number)
        check_boolean_format(row_data, 'lotsEnabled', row_number)
        check_boolean_format(row_data, 'fragile', row_number)
        #Checking barcodeType value and format
        check_barcode_correct_format(row_data["barcodeType"], row_number)
        correct_barcode_wrong_format(row_data, "barcodeType")
        #check customstariff number
        #check countrycode
        #Checking Weight value nad format
        check_weight_format(row_data, "weight", is_float, row_number)
        correct_origin_country_code(row_data, 'originCountryCode')
        remove_empty_columns(data_list)
           
        
        
    create_the_corrected_csv_file(data_list, max_rows_allowed=100, name="corrected")

    
    

# Invoke the main program
main()

# row_number: number of the current row being checked
# row_data: dict where keys are the "headers" and values are the corresponding "values" in the row



#rewrite print statements so that row number is listed at the beginning (row 1: blabla, row 2: blabla etc..)