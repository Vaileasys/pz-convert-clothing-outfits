import os
import xml.etree.ElementTree as ET

# get item name from guid
def guid_item_mapping(guid_table):
    guid_mapping = {}
    tree = ET.parse(guid_table)
    root = tree.getroot()
    for file_entry in root.findall('files'):
        path = file_entry.find('path').text
        guid = file_entry.find('guid').text
        filename = os.path.splitext(os.path.basename(path))[0]
        guid_mapping[guid] = filename
    return guid_mapping

# get the outfit, associated items and write to the output
def get_outfits(xml_file, guid_mapping):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    output = ""
    female_heading_added = False
    male_heading_added = False
    for outfit in root.findall('.//m_FemaleOutfits') + root.findall('.//m_MaleOutfits'):
        if outfit.tag == 'm_FemaleOutfits' and not female_heading_added:
            output += "##############################\n"
            output += "##      Female Outfits      ##\n"
            output += "##############################\n\n"
            female_heading_added = True
        elif outfit.tag == 'm_MaleOutfits' and not male_heading_added:
            output += "##############################\n"
            output += "##       Male Outfits       ##\n"
            output += "##############################\n\n"
            male_heading_added = True

        outfit_name = None
        outfit_guid = None
        items = []
        subitems = []

        for child in outfit:
            if child.tag == 'm_Name':
                outfit_name = child.text
            elif child.tag == 'm_Guid':
                outfit_guid = child.text
            elif child.tag == 'm_items':
                for item in child.findall('.//itemGUID'):
                    item_guid = item.text
                    if item_guid in guid_mapping:
                        item_name = guid_mapping[item_guid]
                    else:
                        item_name = item_guid
                    items.append(item_name)
                for subitem in child.findall('.//subItems/itemGUID'):
                    subitem_guid = subitem.text
                    if subitem_guid in guid_mapping:
                        subitem_name = guid_mapping[subitem_guid]
                    else:
                        subitem_name = subitem_guid
                    subitems.append(subitem_name)

        output += f"outfit: {outfit_name}\n"
        output += f"guid: {outfit_guid}\n"
        if items:
            output += f"items: {', '.join(items)}\n"
        if subitems:
            output += f"subitems: {', '.join(subitems)}\n"
        output += "\n"

    return output

def main():
    input_folder = "resources"
    output_file = "outfits.txt"
    guid_table = os.path.join(input_folder, "fileGuidTable.xml")
    guid_mapping = guid_item_mapping(guid_table)

    with open(output_file, "w") as f_out:
        for filename in os.listdir(input_folder):
            if filename.endswith(".xml"):
                xml_file = os.path.join(input_folder, filename)
                output = get_outfits(xml_file, guid_mapping)
                f_out.write(output)

if __name__ == "__main__":
    main()