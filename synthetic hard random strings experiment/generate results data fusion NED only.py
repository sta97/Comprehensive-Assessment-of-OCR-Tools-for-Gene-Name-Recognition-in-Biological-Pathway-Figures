from mmocr.core.evaluation import eval_ocr_metric
import json

def detect_text(mmocr_data, filename):
    predictions = []
    for x in mmocr_data:
        for i in x["predictions"]:
            if i["image path"] == filename:
                predictions.append({"text": i["prediction"], "weight": x["score"]["1-N.E.D"]})

    text = ""
    i = 0
    end = False
    while not end:
        end_score = 0
        letters = {}
        for x in predictions:
            if i < len(x["text"]):
                if x["text"][i] not in letters:
                    letters[x["text"][i]] = 0
                letters[x["text"][i]] += x["weight"]
            else:
                end_score += x["weight"]
        best_letter = ""
        best_letter_score = 0
        for x in letters:
            if letters[x] > best_letter_score:
                best_letter = x
                best_letter_score = letters[x]
        if best_letter_score > end_score:
            text += best_letter
        else:
            end = True
        i += 1
    return text

images = []

f = open("test_label.json","r")
for l in f:
    data = json.loads(l)
    images.append(data)
    # limit number of images for debugging
    #if len(images) >= 5:
    #    break
f.close()

img_paths = []
for i in images:
    img_paths.append("test_imgs/" + i["filename"])

gt = []
for i in images:
    gt.append(i["text"])

results = []

f = open("mmocr results.json","r")
mmocr_data = json.loads(f.read())
f.close()

predictions = []
for i in img_paths:
    predictions.append(detect_text(mmocr_data, i))

ocr_scores = eval_ocr_metric(predictions, gt)

img_predictions = []
for i in range(len(predictions)):
    img_predictions.append({"prediction": predictions[i], "ground truth": gt[i], "image path": img_paths[i]})

results.append({"model": "data fusion NED only", "score": ocr_scores, "predictions": img_predictions})

f = open("data fusion results NED only.json", "w")
f.write(json.dumps(results))
f.close()
