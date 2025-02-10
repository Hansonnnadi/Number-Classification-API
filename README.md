# Number Classification API

## Description
This API takes a number and returns interesting mathematical properties about it, along with a fun fact.

## How to Use
Make a **GET** request to the following URL:
[
https://number-classification-api-v2op.onrender.com/api/classify-number?number=371


### Example Response:
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
