import json

f = open("mmocr results.json", 'r')
contents = f.read()
f.close()

genes_count = 0
match_count = 0
match_uppercase_count = 0
print("{:20}{:20}".format('prediction', 'ground truth'))
data = json.loads(contents)
for m in data:
    if m['model'] == 'mmocr SAR':
        for x in m['predictions']:
            print("{:20}{:20}".format(x['prediction'], x['ground truth']))
            genes_count += 1
            if x['prediction'] == x['ground truth']:
                match_count += 1

            if x['prediction'].upper() == x['ground truth'].upper():
                match_uppercase_count += 1

print("num genes: {}".format(genes_count))
print("% correct: {:.4}".format(match_count/genes_count))
print("% uppercase match: {:.4}".format(match_uppercase_count/genes_count))
