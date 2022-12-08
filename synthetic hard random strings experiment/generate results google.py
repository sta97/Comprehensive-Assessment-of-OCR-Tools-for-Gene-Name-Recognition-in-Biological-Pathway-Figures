from mmocr.core.evaluation import eval_ocr_metric
import json

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    text = ""
    if len(texts) > 0:
        text = texts[0].description
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

predictions = []
for i in img_paths:
    predictions.append(detect_text(i))

ocr_scores = eval_ocr_metric(predictions, gt)

img_predictions = []
for i in range(len(predictions)):
    img_predictions.append({"prediction": predictions[i], "ground truth": gt[i], "image path": img_paths[i]})

results.append({"model": "google ocr", "score": ocr_scores, "predictions": img_predictions})

f = open("google results.json", "w")
f.write(json.dumps(results))
f.close()
