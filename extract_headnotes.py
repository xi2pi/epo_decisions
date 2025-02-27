import xml.etree.ElementTree as ET
import pandas as pd

# Function to parse the XML and extract relevant data
def parse_xml_to_dataframe(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Prepare data storage
    data = []

    # Loop through all `ep-appeal-decision` elements
    for decision in root.findall(".//ep-appeal-decision"):
        # Extract `reference` attribute from `ep-appeal-bib-data`
        bib_data = decision.find(".//ep-appeal-bib-data")
        reference = bib_data.attrib.get("reference", "") if bib_data is not None else "None"

        # Extract <ep-distribution-code>
        distribution_code = bib_data.find("ep-distribution-code") if bib_data is not None else None
        distribution_code_text = distribution_code.text.strip() if distribution_code is not None and distribution_code.text else "None"

        # Extract <ep-headnote>
        headnote = decision.find(".//ep-headnote")
        if headnote is not None:
            headnote_text = " ".join(p.text.strip() for p in headnote.findall("p") if p.text)
            headnote_exists = True
        else:
            headnote_text = "None"
            headnote_exists = False

        # Append the extracted data
        data.append({
            "Reference": reference,
            "ep-headnote": headnote_text,
            "ep-headnote-exists": headnote_exists
        })

    # Create a DataFrame
    df = pd.DataFrame(data)
    return df


# Example usage
xml_file = "./EPDecisions_Sept2024/EPDecisions_Sept2024.xml"  # Replace with the path to your XML file
df = parse_xml_to_dataframe(xml_file)

df_missing_headnote = df[df["ep-headnote-exists"] == False]
print("Anzahl der Entscheidungen ohne Headnote:", len(df_missing_headnote))

filtered_df = df[df["ep-headnote-exists"] == True]
print("Anzahl der Entscheidungen mit Headnote:", len(filtered_df))

# Display the DataFrame
print(filtered_df)

# Optionally save to CSV
filtered_df[["Reference", "ep-headnote"]].to_excel("ep_appeal_decisions.xlsx", index=False)
filtered_df[["Reference", "ep-headnote"]].to_csv("ep_appeal_decisions.csv", index=False)
