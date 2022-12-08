import csv
import json
import sys
from pathlib import Path
from rapidfuzz.distance import Levenshtein
from difflib import SequenceMatcher

difficultCases = []
f = open("difficult cases.txt", 'r')
for l in f:
    difficultCases.append(l.strip())
f.close()
print(difficultCases)

filename = sys.argv[1]
resultsFile = Path(filename)

filename = resultsFile.stem

out = open(filename + " word diff.csv", "w")
writer = csv.writer(out)
writer.writerow(["model", "image", "prediction", "ground truth", "1-NED", "difflib ratio", "difficult image"])

f = resultsFile.open('r')
data = json.loads(f.read())
f.close()

for m in data:
    for g in m['predictions']:
        ned = Levenshtein.normalized_distance(g['prediction'], g['ground truth'])
        diff = SequenceMatcher(None, g['prediction'], g['ground truth']).ratio()
        image = Path(g['image path']).stem
        difficult = ""
        if image in difficultCases:
            difficult = "yes"
        writer.writerow([m['model'], image, g['prediction'], g["ground truth"], str(1.0 - ned), str(diff), difficult])

out.close()
