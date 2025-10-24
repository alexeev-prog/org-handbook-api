FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY ./pyproject.toml ./uv.lock ./
COPY ./orghandbookapi.toml ./
COPY ./orghandbookapi ./
COPY . .
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "orghandbookapi/app.py"]
