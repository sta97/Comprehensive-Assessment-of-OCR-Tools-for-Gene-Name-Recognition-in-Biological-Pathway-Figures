from mmocr.utils.ocr import MMOCR
from mmocr.core.evaluation import eval_ocr_metric
import json

models = ["ABINet","CRNN","CRNN_TPS","MASTER","NRTR_1/16-1/8","NRTR_1/8-1/4","RobustScanner","SAR","SATRN","SATRN_sm","SEG"]

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

for model in models:
    ocr = MMOCR(det=None, recog=model)
    batch = True
    if model == "CRNN" or model == "SEG":
        batch = False
    predictions_complex = ocr.readtext(img=img_paths,batch_mode=batch,single_batch_size=17)
    predictions = []
    for x in predictions_complex:
        predictions.append(x["text"])

    ocr_scores = eval_ocr_metric(predictions, gt)

    img_predictions = []
    for i in range(len(predictions)):
        img_predictions.append({"prediction": predictions[i], "ground truth": gt[i], "image path": img_paths[i]})

    results.append({"model": "mmocr " + model, "score": ocr_scores, "predictions": img_predictions})

f = open("mmocr results.json", "w")
f.write(json.dumps(results))
f.close()
