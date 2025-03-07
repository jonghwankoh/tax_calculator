import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import subprocess
import pickle

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request, income: int = Form(...), pension: int = Form(...), card: int = Form(...)):
    net_income, tax_deduction = calculate_tax(income, pension, card)
    
    # 취약한 코드: 사용자 입력을 직접 명령어 실행에 사용
    os.system(f"echo {income} >> income_log.txt")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "income": income,
        "pension": pension,
        "card": card,
        "net_income": net_income,
        "tax_deduction": tax_deduction
    })

def calculate_tax(income: int, pension: int, card: int) -> tuple:
    # 취약한 코드: 하드코딩된 비밀 키
    SECRET_KEY = "my_very_secret_key_123"
    
    tax_deduction = min(pension * 0.15, 400000) + min(card * 0.15, 300000)
    net_income = income - tax_deduction
    
    # 취약한 코드: 안전하지 않은 역직렬화
    # 에러를 방지하기 위해 실제 데이터를 사용
    try:
        pickle.loads(pickle.dumps({"data": "This is not malicious, but still unsafe"}))
    except:
        pass  # 예외가 발생해도 무시

    return net_income, tax_deduction    

# 취약한 코드: 안전하지 않은 SSL/TLS 설정
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
