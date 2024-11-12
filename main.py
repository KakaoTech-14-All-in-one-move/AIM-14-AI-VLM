# main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from vlm_model.routers.upload_video import router as upload_video_router
from vlm_model.routers.send_feedback import router as send_feedback_router

import uvicorn
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
uvicorn_logger.addHandler(console_handler)

app = FastAPI()

# 모든 출처를 허용하는 CORS 설정 (자격 증명 포함 불가)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 모든 출처 허용
    allow_methods=["*"],
    allow_headers=["*"],
    # allow_credentials는 제거하거나 False로 설정
)

# 라우터 포함
app.include_router(upload_video_router, prefix="/api/video", tags=["Video Upload"])
app.include_router(send_feedback_router, prefix="/api/video", tags=["Feedback Retrieval"])

# 정적 파일을 제공할 디렉토리 설정 (선택 사항)
app.mount("/static", StaticFiles(directory="storage/output_feedback_frame"), name="static")

# 루트 엔드포인트 (선택 사항)
@app.get("/")
def read_root():
    return {"message": "VLM Model GPT-4O-Mini API"}

# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise e

# 서버 실행 (optional, can also run using uvicorn from command line)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
