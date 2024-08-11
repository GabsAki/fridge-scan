from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="fw0jtHtgqBNROCYOJtkM"
)

def process_image(image):
    result = CLIENT.infer(image, model_id="aicook-lcv4d/3")
    detections = result.get('predictions', [])
    detected_objects = [{'class': obj['class'], 'confidence': obj['confidence']} for obj in detections]

    return detected_objects