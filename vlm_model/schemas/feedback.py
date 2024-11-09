# vlm_model/schemas/feedback.py

from pydantic import BaseModel
from typing import List

class FeedbackFrame(BaseModel):
    frame_index: int
    timestamp: str  # 예: "0m 0s"
    feedback_text: str
    image_base64: str  # Base64로 인코딩된 이미지 데이터

class FeedbackResponse(BaseModel):
    feedbacks: List[FeedbackFrame]
    message: str

class UploadResponse(BaseModel):
    video_id: str
    message: str