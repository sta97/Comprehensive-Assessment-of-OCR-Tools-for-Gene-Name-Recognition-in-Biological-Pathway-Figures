from mmocr.core.evaluation import eval_ocr_metric
import json
import pytesseract

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

def run(psm):
    predictions = []
    for i in img_paths:
        print('psm ' + str(psm) + ' ' + str(i))
        text = ''
        try:
            result = pytesseract.image_to_data(i, config='--psm ' + str(psm), output_type=pytesseract.Output.DICT)
            for t in result['text']:
                text += t
        except Exception as e:
            print(e)
        predictions.append(text)

    ocr_scores = eval_ocr_metric(predictions, gt)

    img_predictions = []
    for i in range(len(predictions)):
        img_predictions.append({"prediction": predictions[i], "ground truth": gt[i], "image path": img_paths[i]})

    results.append({"model": "tesseract psm " + str(psm), "score": ocr_scores, "predictions": img_predictions})

for i in range(14):
    run(i)

f = open("tesseract results.json", "w")
f.write(json.dumps(results))
f.close()
