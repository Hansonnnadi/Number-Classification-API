from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data.get('text', "No fact available.")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            return "No fact available due to HTTP error."
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            return "No fact available due to a request error."
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return "No fact available due to an unexpected error."

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    # Validate input number
    if not number.lstrip('-').isdigit() or number in ['-', '']:
        logger.error(f"Invalid number input: {number}")
        raise HTTPException(status_code=400, detail=f"Invalid number format: {number}. Please enter a valid integer.")

    try:
        number_int = int(number)
    except ValueError:
        logger.error(f"Failed to convert input to integer: {number}")
        raise HTTPException(status_code=400, detail=f"Invalid number: {number}. Please enter a valid integer.")

    # Proceed with classification logic
    try:
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
    except Exception as e:
        # Catch any unexpected errors and return a 500 status code
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
