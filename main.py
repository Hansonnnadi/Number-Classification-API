from fastapi import FastAPI, Query
import requests
from typing import Dict
from math import sqrt

app = FastAPI()

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Number to classify")) -> Dict:
    try:
        fun_fact_response = requests.get(f"http://numbersapi.com/{number}/math?json")
        fun_fact = fun_fact_response.json().get("text", "No fun fact available.")

        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("even" if number % 2 == 0 else "odd")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(number)),
            "fun_fact": fun_fact
        }
    except Exception as e:
        return {"number": number, "error": True}
