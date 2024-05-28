""" FastAPI application for calculating projected losses based on building data.
"""
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
import loss_calc.exercise1_losses_calculator as normal
import tempfile

app = FastAPI(
    title="API",
    description="An API for calculating projected losses based on building data."
)

@app.post("/calculate_normal")
async def calculate_losses(
    file: UploadFile = File(...),
    years: int = Query(1, ge=1, description="Number of years for projection"),
    discount_rate: float = Query(0.05, ge=0.0, description="Discount rate"),
    maintenance_rate: float = Query(50, ge=0.0, description="Maintenance rate"),
):
    """Calculates both simple and complex projected losses."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

        data = normal.load_data(temp_file_path)

        total_loss = normal.calculate_projected_losses(
            data, years, discount_rate, maintenance_rate
        )

        return JSONResponse(
            content={
                "total_projected_loss": round(total_loss, 2),
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}') from e

@app.post("/calculate_complex")
async def calculate_losses_complex(
    file: UploadFile = File(...),
    years: int = Query(1, ge=1, description="Number of years for projection"),
    discount_rate: float = Query(0.05, ge=0.0, description="Discount rate"),
):
    """Calculates both simple and complex projected losses."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

        data = normal.load_data(temp_file_path)

        complex_total_loss = normal.calculate_complex_projected_losses(
            data, years, discount_rate
        )

        return JSONResponse(
            content={
                "complex_total_projected_loss": round(complex_total_loss["total"], 2),
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}') from e
