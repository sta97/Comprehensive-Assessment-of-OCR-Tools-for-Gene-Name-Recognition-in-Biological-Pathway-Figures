import csv
import json

out = open("summerized results.csv", "w")
writer = csv.writer(out)
writer.writerow(["model", "char_recall", "char_precision", "word_acc", "word_acc_ignore_case", "word_acc_ignore_case_symbol", "1-N.E.D"])

def addResults(filename):
    f = open(filename, "r")
    data = json.loads(f.read())
    f.close()
    for x in data:
        writer.writerow([x["model"], x["score"]["char_recall"], x["score"]["char_precision"], x["score"]["word_acc"], x["score"]["word_acc_ignore_case"], x["score"]["word_acc_ignore_case_symbol"], x["score"]["1-N.E.D"]])

addResults('tesseract results.json')
addResults('easyocr results.json')
addResults('google results.json')
addResults('keras results.json')
addResults('mmocr results.json')

out.close()
