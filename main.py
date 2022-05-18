from pydantic import BaseModel
from fastapi import FastAPI
from image_processing.image_fusion import get_fused_image


app = FastAPI()


class ImageMerger(BaseModel):
    encoded_img1: str
    encoded_img2: str


@app.get("/")
def health_check():
    return {
        "data": "Hello world"
    }


@app.post("/merge_two_images")
def merge_two_images(images: ImageMerger):
    return {
        "merged_image": get_fused_image(images.encoded_img1, images.encoded_img2)
    }
