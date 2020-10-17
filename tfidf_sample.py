from sklearn.feature_extraction.text import TfidfVectorizer
import os

def make_filenames():
    all_files = []
    path = "./where_the_txt_files_are"
    dirs = os.listdir(path)
    for file in dirs:
        all_files.append(path + "/" + file)
    return all_files

