from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def calculate_tax(income):
    # 간단한 세금 계산 로직 (실제 연말정산 계산과는 다를 수 있습니다)
    if income <= 12000000:
        tax = income * 0.06
    elif income <= 46000000:
        tax = 720000 + (income - 12000000) * 0.15
    else:
        tax = 5820000 + (income - 46000000) * 0.24
    return tax

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request, income: int = Form(...)):
    tax = calculate_tax(income)
    return templates.TemplateResponse("result.html", {"request": request, "income": income, "tax": tax})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
