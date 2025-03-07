import xml.etree.ElementTree as ET
import pandas as pd

# Funktion zum Parsen der XML-Datei und Extrahieren relevanter Daten
def parse_xml_to_dataframe(xml_file):
    # XML-Datei einlesen
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Datenliste vorbereiten
    data = []

    # Alle ep-appeal-decision Elemente durchgehen
    for decision in root.findall(".//ep-appeal-decision"):
        # Referenz aus ep-appeal-bib-data extrahieren
        bib_data = decision.find(".//ep-appeal-bib-data")
        reference = bib_data.attrib.get("reference", "None") if bib_data is not None else "None"

        # Verteilungs-Code extrahieren
        distribution_code = bib_data.find("ep-distribution-code") if bib_data is not None else None
        distribution_code_text = distribution_code.text.strip() if distribution_code is not None and distribution_code.text else "None"

        # Alle ep-headnote Elemente (verschiedene Sprachen möglich) finden und kombinieren
        headnotes = decision.findall(".//ep-headnote")
        headnote_texts = []
        headnote_languages = []
        for hn in headnotes:
            lang = hn.attrib.get("lang", "None").upper()
            headnote_languages.append(lang)
            text = " ".join(p.text.strip() for p in hn.findall("p") if p.text)
            headnote_texts.append(f"[{lang}] {text}")
        headnote_text = " | ".join(headnote_texts) if headnote_texts else None
        headnote_language = ", ".join(set(headnote_languages)) if headnote_languages else "None"

        # Alle ep-catchword Elemente (verschiedene Sprachen möglich) finden und kombinieren
        catchwords = decision.findall(".//ep-catchword")
        catchword_texts = []
        catchword_languages = []
        for cw in catchwords:
            lang = cw.attrib.get("lang", "None").upper()
            catchword_languages.append(lang)
            text = " ".join(p.text.strip() for p in cw.findall("p") if p.text)
            catchword_texts.append(f"[{lang}] {text}")
        catchword_text = " | ".join(catchword_texts) if catchword_texts else None
        catchword_language = ", ".join(set(catchword_languages)) if catchword_languages else "None"

        # Fallnummer-Daten extrahieren
        case_num = decision.find(".//ep-case-num")
        case_code = case_num.attrib.get("code", "None") if case_num is not None else "None"
        country = case_num.find("country").text.strip() if case_num is not None and case_num.find("country") is not None else "None"
        appeal_num = case_num.find("ep-appeal-num").text.strip() if case_num is not None and case_num.find("ep-appeal-num") is not None else "None"
        year = case_num.find("ep-year").text.strip() if case_num is not None and case_num.find("ep-year") is not None else "None"

        # Daten in Liste speichern
        data.append({
            "Reference": reference,
            "ep-distribution-code": distribution_code_text,
            "ep-headnote": headnote_text,
            "ep-headnote-language": headnote_language,
            "ep-catchword": catchword_text,
            "ep-catchword-language": catchword_language,
            "Case Code": case_code,
            "Country": country,
            "Appeal Number": appeal_num,
            "Year": year
        })

    # DataFrame erstellen
    df = pd.DataFrame(data)
    return df


# XML-Datei parsen und DataFrame erstellen
xml_file = "./EPDecisions_March2025/EPDecisions_March2025.xml"  # Dateipfad anpassen
df = parse_xml_to_dataframe(xml_file)

# Entscheidungen ohne Headnote ausgeben
df_missing_headnote = df[df["ep-headnote"].isna()]
print("Anzahl der Entscheidungen ohne Headnote:", len(df_missing_headnote))

# Entscheidungen mit Headnote oder Catchword filtern
filtered_df = df[df["ep-headnote"].notna() | df["ep-catchword"].notna()]
print("Anzahl der Entscheidungen mit Headnote oder Catchword:", len(filtered_df))
print(filtered_df)

# DataFrame speichern
filtered_df[["Reference", "ep-headnote", "ep-headnote-language", "ep-catchword", "ep-catchword-language", "Case Code", "Country", "Appeal Number", "Year"]].to_excel("ep_appeal_decisions.xlsx", index=False, encoding='ISO-8859-1')
filtered_df[["Reference", "ep-headnote", "ep-headnote-language", "ep-catchword", "ep-catchword-language", "Case Code", "Country", "Appeal Number", "Year"]].to_csv("ep_appeal_decisions.csv", index=False, encoding='ISO-8859-1')


'''next'''
# delete dublicates

# import pandas as pd

# # Function to parse the XML and extract relevant data
# def parse_xml_to_dataframe(xml_file):
#     # Parse the XML file
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     # Prepare data storage
#     data = []

#     # Loop through all `ep-appeal-decision` elements
#     for decision in root.findall(".//ep-appeal-decision"):
#         # Extract `reference` attribute from `ep-appeal-bib-data`
#         bib_data = decision.find(".//ep-appeal-bib-data")
#         reference = bib_data.attrib.get("reference", "") if bib_data is not None else "None"

#         # Extract <ep-distribution-code>
#         distribution_code = bib_data.find("ep-distribution-code") if bib_data is not None else None
#         distribution_code_text = distribution_code.text.strip() if distribution_code is not None and distribution_code.text else "None"

#         # Extract <ep-headnote>
#         headnote = decision.find(".//ep-headnote")
#         if headnote is not None:
#             headnote_text = " ".join(p.text.strip() for p in headnote.findall("p") if p.text)
#             headnote_exists = True
#         else:
#             headnote_text = "None"
#             headnote_exists = False
            
#         # Extract <ep-headnote>
#         catchword = decision.find(".//ep-catchword")
#         if catchword is not None:
#             catchword_text = " ".join(p.text.strip() for p in catchword.findall("p") if p.text)
#             catchword_exists = True
#         else:
#             catchword_text = "None"
#             catchword_exists = False

#         # Append the extracted data
#         data.append({
#             "Reference": reference,
#             "ep-headnote": headnote_text,
#             "ep-headnote-exists": headnote_exists,
#             "ep-catchword": catchword_text,
#             "ep-catchword-exists": catchword_exists
#         })

#     # Create a DataFrame
#     df = pd.DataFrame(data)
#     return df


# # Example usage
# xml_file = "./EPDecisions_March2025/EPDecisions_March2025.xml"  # Replace with the path to your XML file
# df = parse_xml_to_dataframe(xml_file)

# df_missing_headnote = df[df["ep-headnote-exists"] == False]
# print("Anzahl der Entscheidungen ohne Headnote:", len(df_missing_headnote))

# filtered_df = df[df["ep-headnote-exists"] == True]
# print("Anzahl der Entscheidungen mit Headnote:", len(filtered_df))

# # Display the DataFrame
# print(filtered_df)

# # Optionally save to CSV
# filtered_df[["Reference", "ep-headnote", "ep-catchword"]].to_excel("ep_appeal_decisions.xlsx", index=False)
# filtered_df[["Reference", "ep-headnote", "ep-catchword"]].to_csv("ep_appeal_decisions.csv", index=False, encoding='utf-8')
