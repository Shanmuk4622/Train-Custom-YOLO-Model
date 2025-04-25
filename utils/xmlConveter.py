import os
import xml.etree.ElementTree as ET

# Define class names (ensure they match exactly with XML annotation names)
CLASSES = ['bag']

# Input and Output directories (Update paths)
XML_DIR = r"../data/labels"
OUTPUT_DIR = r"../data/rawData2/images/training"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_bbox(size, box):
    """ Convert VOC bbox format to YOLO format (x_center, y_center, width, height). """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]

    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]

    return round(x * dw, 6), round(y * dh, 6), round(w * dw, 6), round(h * dh, 6)


def convert_annotation(xml_file):
    """ Convert a single XML file to YOLO format. """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    txt_filename = os.path.join(OUTPUT_DIR, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_filename, "w") as txt_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text.strip()
            if class_name not in CLASSES:
                continue  # Skip unknown classes

            class_id = CLASSES.index(class_name)
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            xmax = int(bbox.find("xmax").text)
            ymin = int(bbox.find("ymin").text)
            ymax = int(bbox.find("ymax").text)

            x, y, w, h = convert_bbox((width, height), (xmin, xmax, ymin, ymax))
            txt_file.write(f"{class_id} {x} {y} {w} {h}\n")


def convert_all():
    """ Convert all XML files in the folder. """
    xml_files = [f for f in os.listdir(XML_DIR) if f.endswith(".xml")]

    for xml_file in xml_files:
        convert_annotation(os.path.join(XML_DIR, xml_file))
        print(f"Converted: {xml_file}")


# Run the conversion
convert_all()
