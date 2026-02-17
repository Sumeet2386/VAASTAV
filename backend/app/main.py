from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware




from app.api.verify import router as verify_router

app = FastAPI(title="VAASTAV Verification API")

# 🔑 CORS CONFIG (THIS IS THE FIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(verify_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Backend running"}

