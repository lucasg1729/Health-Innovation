import csv
import xml.etree.ElementTree as ET

def xml_to_csv(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Extract column headers from the XML file (assuming the first row contains headers)
        headers = []
        for child in root[0]:
            headers.append(child.tag)
        csvwriter.writerow(headers)

        # Write data rows to the CSV file
        for row in root:
            row_data = []
            for element in row:
                row_data.append(element.text)
            csvwriter.writerow(row_data)

if __name__ == "__main__":
    # Replace 'your_username' with your actual username
    desktop_path = "/Users/mitavnayak/Desktop/"

    input_xml_file = desktop_path + "secdata3.xml"  # Full path to your XML file on the desktop
    output_csv_file = desktop_path + "output2.csv"  # Full path for the CSV output file on the desktop

    xml_to_csv(input_xml_file, output_csv_file)
    print("XML to CSV conversion completed.")
