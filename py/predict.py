import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import pytesseract

blackboard_model = load_model("blackboardYN_model.h5")
text_presence_model = load_model("txtYN_model.h5")
no_text_model = load_model("txtN_model.h5")
with_text_model = load_model("txtY_model.h5")

IMG_HEIGHT = 224
IMG_WIDTH = 224

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
    img = img / 255.0
    img = tf.expand_dims(img, axis=0)
    return img

def detect_blackboard(image_path):
    img = preprocess_image(image_path)
    prediction = blackboard_model.predict(img)
    return prediction[0][0] > 0.5

def detect_text_presence(image_path):
    img = preprocess_image(image_path)
    prediction = text_presence_model.predict(img)
    return prediction[0][0] > 0.5

def classify_no_text(image_path):
    img = preprocess_image(image_path)
    prediction = no_text_model.predict(img)
    classes = ['0_Good', '1_Bad']
    return classes[prediction.argmax()]

def classify_with_text(image_path):
    img = preprocess_image(image_path)
    prediction = with_text_model.predict(img)
    classes = ['0_Good', '1_Bad']
    return classes[prediction.argmax()]

def main(image_path):
    if not detect_blackboard(image_path):
        print("黒板が検出されませんでした。処理を終了します。")
        return

    print("黒板が検出されました。文字の有無を判定します...")
    if detect_text_presence(image_path):
        print("文字が検出されました。txtY_modelで分類します...")
        classification = classify_with_text(image_path)
    else:
        print("文字は検出されませんでした。txtN_modelで分類します...")
        classification = classify_no_text(image_path)

    print(f"分類結果: {classification}")

image_path = "/content/drive/MyDrive/SSH_Blackboard_AI/img_unknown/黒板1.jpeg"
main(image_path)
