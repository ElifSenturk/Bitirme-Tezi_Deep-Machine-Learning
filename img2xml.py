"Author: Elif ŞENTÜRK"

import xml.etree.cElementTree as ET
from xml.dom import minidom
import os 

# DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/with_mask"
# DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/without_mask"
DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/mask_weared_incorrect"

CATEGORIES = ["with_mask", "without_mask", "mask_weared_incorrect"]


paths = []
for dirname, _, filenames in os.walk( DIRECTORY ):
    for filename in filenames:
        # print(os.path.join(dirname,"\t", filename))

        annotation = ET.Element("annotation")


        ET.SubElement(annotation, "folder").text = "mask_weared_incorrect"
        ET.SubElement(annotation, "filename").text = filename
        ET.SubElement(annotation, "path").text = os.path.join(dirname, filename)

        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = "Unknown"


        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = "128"
        ET.SubElement(size, "height").text = "128"
        ET.SubElement(size, "depth").text = "3"


        ET.SubElement(annotation, "segmented").text = "0"

        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = "mask_weared_incorrect"
        ET.SubElement(object, "pose").text = "Unspecified"
        ET.SubElement(object, "truncated").text = "0"
        ET.SubElement(object, "difficult").text = "0"

        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = "1"
        ET.SubElement(bndbox, "ymin").text = "1"
        ET.SubElement(bndbox, "xmax").text = "126"
        ET.SubElement(bndbox, "ymax").text = "126"



        dom = minidom.parseString(ET.tostring(annotation))
        # print (dom.toprettyxml(indent='\t'))

        # tree = ET.ElementTree(annotation)
        # tree.write("/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/with_mask/with_mask01.xml")

        sourceFile = open(DIRECTORY+'/'+filename[:-4]+'.xml', 'w')
        print(dom.toprettyxml(indent='\t'), file = sourceFile)
        sourceFile.close()
