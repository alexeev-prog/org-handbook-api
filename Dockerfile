FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY ./pyproject.toml ./uv.lock ./
COPY ./orghandbookapi.toml ./
COPY . .
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "main.py"]
