import shutil
from flask import Flask, request, render_template, jsonify
from PyPDF2 import PdfMerger
import os
from flask_cors import CORS
import zipfile

if (os.path.exists("RJ")):
    shutil.rmtree("RJ")

# os.mkdir("RJ")

with zipfile.ZipFile("RJ.zip", 'r') as zip_ref:
    zip_ref.extractall("RJ")

root_dir = 'RJ/RJ'

level_1 = os.listdir(root_dir)
data_level_1 = []
for i in range (len(os.listdir(root_dir))):
    # print(os.path.join(root_dir, level_1[i]))
    data_level_1.append(os.path.join(root_dir, level_1[i]))
    # print(level_2)
    # print(os.listdir(level_2))
    # for j in range (len(os.listdir(level_2[i]))):
    #     level_3 = os.path.join(root_dir, level_1[i], level_2[j])
    #     print(level_3)
print(data_level_1)