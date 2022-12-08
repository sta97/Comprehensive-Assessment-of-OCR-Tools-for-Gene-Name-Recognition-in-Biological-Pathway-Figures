import csv
import json
import sys
from pathlib import Path
from rapidfuzz.distance import Levenshtein
from difflib import SequenceMatcher

filename = sys.argv[1]
resultsFile = Path(filename)

filename = resultsFile.stem

out = open(filename + " word diff.csv", "w")
writer = csv.writer(out)
writer.writerow(["model", "prediction", "ground truth", "1-NED", "difflib ratio"])

f = resultsFile.open('r')
data = json.loads(f.read())
f.close()

for m in data:
    for g in m['predictions']:
        ned = Levenshtein.normalized_distance(g['prediction'], g['ground truth'])
        diff = SequenceMatcher(None, g['prediction'], g['ground truth']).ratio()
        writer.writerow([m['model'], g['prediction'], g["ground truth"], str(1.0 - ned), str(diff)])

out.close()
