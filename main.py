from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = httpx.get(url, timeout=5)
        return response.text if response.status_code == 200 else "No fact available."
    except httpx.RequestError:
        return "Failed to fetch fun fact."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": get_fun_fact(number)
        }
    except Exception:
        return {"number": str(number), "error": True}
