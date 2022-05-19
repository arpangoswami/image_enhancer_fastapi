from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from image_processing.image_fusion import get_fused_image

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageMerger(BaseModel):
    grayscale_img: str
    blur_img: str


@app.get("/")
def health_check():
    return {
        "data": "Hello world"
    }


@app.post("/merge_two_images")
def merge_two_images(images: ImageMerger):
    return {
        "merged_image": get_fused_image(images.grayscale_img, images.blur_img)
    }
