import logging
from importlib.metadata import version

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse

from poetry_example.utils import init_logging
from poetry_example.data import CalculationRequest, CalculationResponse

init_logging()
logger = logging.getLogger("poetry_example")


app = FastAPI(
    title="Poetry Example REST API",
    description="Fields not marked with '*' or 'required' are optional.",
    version=version("poetry_example"),
    docs_url=None,
    redoc_url=None,
)


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Server starting..")


@app.get("/calculate_get", response_model=CalculationResponse, description="Calculates something using a GET request...")
async def calculate_get(x: int, y: float) -> CalculationResponse:  # pylint: disable=invalid-name
    logger.info("Calculating x=%s y=%s", x, y)
    return CalculationResponse(result=110)


@app.post(
    "/calculate_post", response_model=CalculationResponse, description="Calculates something using a POST request..."
)
async def calculate_post(request: CalculationRequest) -> CalculationResponse:
    logger.info("Processing request: %s...", str(request))
    result = CalculationResponse(result=10)
    logger.info("Finished result=%s", result)
    return result


# customized documentation pages


@app.get("/docs", include_in_schema=False)
def overridden_swagger() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")


@app.get("/redoc", include_in_schema=False)
def overridden_redoc() -> HTMLResponse:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="API Documentation",
    )


if __name__ == "__main__":
    # this main allows the application to also be started with python -m poetry_example.main
    import uvicorn  # type: ignore

    uvicorn.run("poetry_example.main:app", reload=True)
