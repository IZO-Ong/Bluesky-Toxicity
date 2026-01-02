FROM python:3.11-slim

WORKDIR /app

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. PRE-DOWNLOAD THE MODEL
# This ensures the 418MB file is already in the image before it runs
RUN python -c "from detoxify import Detoxify; Detoxify('original')"

# 3. Copy source code
COPY . .

CMD ["python", "runner.py"]
