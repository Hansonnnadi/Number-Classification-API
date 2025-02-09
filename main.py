from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
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

async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json=true"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['text']  # Extract the 'text' field for the fun fact
            return "No fact available."
        except httpx.RequestError:
            return "Failed to fetch fun fact."

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")

        fun_fact = await get_fun_fact(number)  # Asynchronously fetch the fun fact

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": fun_fact
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input. Please provide a valid integer.")
