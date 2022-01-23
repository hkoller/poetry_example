FROM --platform=linux/arm64 python:3.9-slim

COPY dist/*.whl /

RUN pip install --no-cache-dir /*.whl  && rm -rf /*.whl

CMD ["uvicorn", "--host", "0.0.0.0", "poetry_example.main:app"]

