from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request, income: int = Form(...), pension: int = Form(...), card: int = Form(...)):
    net_income, tax_deduction = calculate_tax(income, pension, card)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "income": income,
        "pension": pension,
        "card": card,
        "net_income": net_income,
        "tax_deduction": tax_deduction
    })

def calculate_tax(income: int, pension: int, card: int) -> tuple:
    # 간단한 계산 로직 (실제 세금 계산은 더 복잡할 수 있습니다)
    tax_deduction = min(pension * 0.15, 400000) + min(card * 0.15, 300000)
    net_income = income - tax_deduction
    return net_income, tax_deduction