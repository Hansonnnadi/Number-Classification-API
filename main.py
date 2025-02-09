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

# Asynchronous function to fetch fun fact
async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json=true"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['text']  # Extract the 'text' field for the fun fact
            return "No fact available."
        except httpx.RequestError as e:
            return f"Request error: {e}"

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        # Try to convert the number from string to integer
        number_int = int(number)
    except ValueError:
        # If conversion fails, return the error in the required format
        return {"number": number, "error": True}

    # Proceed with classification logic
    properties = []
    if is_armstrong(number_int):
        properties.append("armstrong")
    properties.append("odd" if number_int % 2 else "even")

    fun_fact = await get_fun_fact(number_int)  # Asynchronously fetch the fun fact

    return {
        "number": number_int,
        "is_prime": is_prime(number_int),
        "is_perfect": is_perfect(number_int),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number_int)),
        "fun_fact": fun_fact
    }
