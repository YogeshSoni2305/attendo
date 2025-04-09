# from deepface import DeepFace
# import os

# # print("Current Directory:", os.getcwd())
# # print("Files in Directory:", os.listdir())
# # verification = DeepFace.verify(img1_path = "img1.jpeg", img2_path = "img2.jpeg")
# # analysis = DeepFace.analyze(img_path = "img2.jpeg", actions = ["age", "gender", "emotion", "race"])
# # print(analysis)from deepface import DeepFace

# from deepface import DeepFace

# verification = DeepFace.verify(img1_path="img4.jpg", img2_path="img5.jpg", enforce_detection=False)
# analysis = DeepFace.analyze(img_path="img4.jpg", actions=["age", "gender", "emotion", "race"], enforce_detection=False)

# print(verification)
# print(analysis)
from deepface import DeepFace

result = DeepFace.verify(
    img1_path="img1.jpeg",
    img2_path="img2.jpeg",
    model_name="ArcFace",  # Use "Facenet" for lighter version
    detector_backend="retinaface",  # Better face detection
    enforce_detection=False  # To avoid error if face detection fails
)

print(result)

