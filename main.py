from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact from Numbers API."""
    url = f"http://numbersapi.com/{n}/math?json=true"
    try:
        response = httpx.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['text']  # Get the fun fact text
        return "No fact available."
    except httpx.RequestError:
        return "Failed to fetch fun fact."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    """Classify the number and return mathematical properties and a fun fact."""
    try:
        # Determine properties based on number
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")

        # Return classification result
        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": get_fun_fact(number)
        }
    except Exception as e:
        return {"error": True, "message": str(e)}

