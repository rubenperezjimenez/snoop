"""FastAPI calculator app with JSON API and static UI."""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Calculator API", version="1.0.0")


class CalcRequest(BaseModel):
    """Request model for calculator operations."""

    a: float
    b: float
    operation: str


class CalcResponse(BaseModel):
    """Response model for calculator results."""

    result: float
    operation: str
    a: float
    b: float


@app.post("/api/calc", response_model=CalcResponse)
def calculate(request: CalcRequest) -> CalcResponse:
    """Perform a calculation and return result as JSON.

    Args:
        request: CalcRequest with two numbers and an operation

    Returns:
        CalcResponse with the result

    Raises:
        HTTPException: If operation is invalid or division by zero
    """
    a, b = request.a, request.b
    op = request.operation.lower()

    if op == "add":
        result = a + b
    elif op == "subtract":
        result = a - b
    elif op == "multiply":
        result = a * b
    elif op == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = a / b
    elif op == "power":
        result = a ** b
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown operation: {request.operation}. "
            f"Valid operations: add, subtract, multiply, divide, power",
        )

    return CalcResponse(result=result, operation=op, a=a, b=b)


# Mount static files (HTML, CSS, JS) from the static/ folder
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
