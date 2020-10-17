import pdftotext
import os

def convert_pdfs(in_dir="pdfs/", out_dir="txts/"):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)



