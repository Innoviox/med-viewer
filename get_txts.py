import pdftotext
import os
import tqdm

def convert_pdfs(in_dir="pdfs/", out_dir="txts/"):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for file in tqdm.tqdm(os.listdir(in_dir)):
        if not file.endswith(".pdf"):
            continue

        with open(in_dir + file, "rb") as f:
            pdf = pdftotext.PDF(f)
            text = "\n".join(pdf)

            filename = file[:-4] + ".txt"

            open(out_dir + filename, "w").write(text)

convert_pdfs()