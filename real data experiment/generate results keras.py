from mmocr.core.evaluation import eval_ocr_metric
import json
import keras_ocr
pipeline = keras_ocr.pipeline.Pipeline()

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

predictions = []
for i in img_paths:
    print(i)
    try:
        predictions.append(pipeline.recognize([i])[0][0][0])
    except:
        predictions.append("")

ocr_scores = eval_ocr_metric(predictions, gt)

img_predictions = []
for i in range(len(predictions)):
    img_predictions.append({"prediction": predictions[i], "ground truth": gt[i], "image path": img_paths[i]})

results.append({"model": "keras", "score": ocr_scores, "predictions": img_predictions})

f = open("keras results.json", "w")
f.write(json.dumps(results))
f.close()
