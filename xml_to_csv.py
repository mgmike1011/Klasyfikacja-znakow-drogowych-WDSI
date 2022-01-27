# 
# Program konwertujący pliki XML do plików CSV
# @author: Miłosz Gajewski
# 
import xml.etree.ElementTree as Xet
import pandas as pd
import glob, os
import csv
# Format danych
path = 'annotations/'
cols = ["Width", "Height", "Name","Roi.X1", "Roi.Y1", "Roi.X2" ," Roi.Y2","Filename"]
rows = []
# Plik CSV
csvfile = open("data.csv",'w',encoding='utf-8',newline='')
csvfile_writer = csv.writer(csvfile)
csvfile_writer.writerow(cols)
# Ekstrakcja danych
for filename in glob.glob(os.path.join(path, '*.xml')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
       # Parsing the XML file
        xmlparse = Xet.parse(f)
        root = xmlparse.getroot()
        file_name = xmlparse.find("filename").text
        for i in xmlparse.findall("size"):
            if(i):
                Width = i.find("width").text
                Height = i.find("height").text
        for i in xmlparse.findall("object"):
            if(i):
                Name = i.find("name").text
        for j in xmlparse.findall("object/bndbox"):
            if(j):
                Roi_X1 =  j.find("xmin").text
                Roi_Y1 =  j.find("ymin").text
                Roi_X2 =  j.find("xmax").text
                Roi_Y2 =  j.find("ymax").text
        csv_line = [Width,Height,Name,Roi_X1,Roi_Y1,Roi_X2,Roi_Y2,file_name]
        rows.append(csv_line)
# Zapis danych do pliku CSV
csvfile_writer.writerows(rows)
csvfile.close()