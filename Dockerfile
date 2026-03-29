FROM python:3.14-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml /app/
COPY .python-version /app/
RUN uv sync
COPY ./*.py /app/
COPY .env /app/
CMD ["uv","run","main.py"]
